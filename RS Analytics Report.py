#!/usr/bin/env python
# coding: utf-8

# In[1]:


#imports
import pandas as pd
import seaborn as sns
import numpy as np
import calendar
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium import plugins
from folium.plugins import HeatMap


# In[2]:


#read in 2019 csv to dataframe
df = pd.read_csv("Metro_Nashville_Police_Department_Calls_for_Service__2019_.csv", index_col='Event Number')


# In[3]:


df.head()


# In[4]:


#view row, col counts for full dataframe
df.shape


# In[5]:


#view total instance counts for each column
df.count()


# In[6]:


#filter dataset to new dataframe for theft analysis
df_new = df[['Call Received', 'Tencode Description','Disposition Description','Mapped Location','Latitude','Longitude']]
#sort in ascending order by date
df_new = df_new.sort_values(by='Call Received') 
df_new.head(5)


# In[7]:


df_new.shape


# In[8]:


#view counts for all NaN values
df_new.isna().sum()


# In[9]:


#convert date and time of call received column to pandas datetime type
df_new['Call Received'] =  pd.to_datetime(df_new['Call Received'])


# In[10]:


#add new column "Call Time" listing call time in HH:MM:SS format
df_new['Call Time'] = [d.time() for d in df_new['Call Received']]


# In[11]:


#add new column "Call Day" listing call day as 'Monday', 'Tuesday', etc.
df_new['Call Day'] = df_new['Call Received'].dt.day_name()


# In[12]:


#add new column "Call Month" listing call time in HH:MM:SS format
df_new['Call Month'] = pd.DatetimeIndex(df_new['Call Received']).month


# In[13]:


#abbreviate call month
df_new['Call Month'] = df_new['Call Month'].apply(lambda x: calendar.month_abbr[x])


# In[14]:


#add new column indicting the time of day the call was received based on 6 bins of time
df_new = df_new.assign(
    timeOfDay=pd.cut(
        df_new['Call Received'].dt.hour, #denote the hour of the call
        [-1, 4, 8, 12, 16, 20, 24],     #range of times for labels below to fall under
        labels=['Late Night', 'Early Morning', 'Morning', 'Afternoon', 'Evening', 'Night'])) #labels


# In[15]:


#rename column
df_new.rename(columns = {'timeOfDay':'Call Time of Day'}, inplace = True)


# In[17]:


#add new "Call Week" column indicting numerically the week the call occurred, 1-52
df_new['Call Week'] = df_new['Call Received'].dt.week


# In[16]:


df_new.head(3)


# In[18]:


#Should only be 51 weeks for call week since dataframe is missing data from jan 1-12
df_new.apply(lambda x: len(x.unique()))


# In[19]:


test1 = df_new[(df_new['Call Week'] == 1)]
test1.shape


# In[21]:


test1.head(3)


# In[22]:


test1.tail(3)


# In[23]:


df_new['Call Week'].value_counts()


# In[24]:


#December 30 and 31 are being counted as week 1, need to change them to week 52
df_new.loc[df_new['Call Week'] == 1, "Call Week"] = 52


# In[25]:


#re-order columns in dataframe
df_new = df_new[['Call Received', 'Call Month', 'Call Week', 'Call Day', 'Call Time', 'Call Time of Day', 'Tencode Description','Disposition Description','Mapped Location','Latitude','Longitude']]


# In[26]:


#view all unique values of column
df_new['Tencode Description'].unique()


# In[27]:


#create dictionary of values to be replaced for "Tencode Description" column
td_replacements = {
    '3': 'Administrative/Special Assignment',
    '50': 'Theft',
    '57': 'Fight / Assault',
    '53': 'Holdup / Robbery',
    '44': 'Disorderly Person',
    '64': 'Corpse / D. O. A.',
    '54': 'Person with Weapon',
    '70': 'Burglary - Residence',
    '96': 'Business Check',
    '43': 'Want Officer for Investigation / Assistance',
    '95': 'Meal Break',
    '83': 'Shots Fired',
    '92': 'Fixed Post',
    '40': 'Suspicious Person',
    '93': 'Traffic Violation',
    '15': 'Community Policing Activity',
    '71': 'Burglary - Non-Residence',
    '88': 'Investigate 911 Hang-Up Call',
    '58': 'Prowler',
    '49': 'Vehicle Blocking Right of Way',
    '87': 'Safety Hazard',
    '75': 'Missing Person',
    '62': 'Person Screaming',
    '16': 'Transport Prisoner / Suspect',
    '45': 'Vehicle Accident - Property Damage',
    '42': 'Intoxicated Person',
    '73': 'Hazardous Liquid / Gas Leak',
    '46': 'Vehicle Accident - Personal Injury',
    '59': 'Person Indecently Exposed',
    '63': 'Suicidal Person',
    '65': 'Dangerous / Injured Animal',
    '35': 'Mentally ILL Person',
    '52': 'Shooting',
    '61': 'Fire',
    '51': 'Cutting / Stabbing',
    '14': 'Escort / Convoy',
    '8000': 'Explosion',
    '94': 'Personal Relief',
    '66': 'Bomb Threat',
    '85': 'Prisoner Escapee'
}


# In[28]:


#use python .map() function to replace values in column using dictionary above
df_new['Tencode Description'] = df_new['Tencode Description'].map(td_replacements).fillna(df_new['Tencode Description'])


# In[29]:


#check that mapping was done correctly
df_new['Tencode Description'].unique()


# In[30]:


df_new.head()


# In[31]:


#plot frequency of calls by month
plt.figure(figsize=(16, 8))
sns.set(style="darkgrid")
ax = sns.countplot(x="Call Month", data=df_new, palette='hot', order = df_new['Call Month'].value_counts().index)


# In[32]:


#plot frequency of calls by day
plt.figure(figsize=(16, 8))
sns.set(style="darkgrid")
ax = sns.countplot(x="Call Day", data=df_new, palette='hot', order = df_new['Call Day'].value_counts().index)


# In[33]:


#plot frequency of calls by time of day
plt.figure(figsize=(16, 8))
sns.set(style="darkgrid")
ax = sns.countplot(x="Call Time of Day", data=df_new, palette='hot', order = df_new['Call Time of Day'].value_counts().index)


# In[34]:


#view unique values for all reasons for a call and their asssociated frequencies
df_new['Tencode Description'].value_counts()


# In[36]:


#percent of total calls that are labeled as "theft"
(df_new['Tencode Description'] == 'Theft').value_counts(normalize=True)


# In[37]:


#group and view the percentage of all calls for each day and time
df_time = df_new.groupby('Call Day')['Call Time of Day'].value_counts(normalize=True).to_frame()
df_time


# In[38]:


#unstack for easier view
df_time.unstack()


# In[39]:


#create new dataframe filtered by only calls for theft
df_theft_calls = df_new[df_new['Tencode Description'] == 'Theft']


# In[40]:


df_theft_calls.shape


# In[41]:


df_theft_calls.head(10)


# In[42]:


#create color palette to be red for specified summer and fall months, grey for all others
pal = {month: "r" if ((month == "Oct") or
                     (month == "Jun") or
                     (month == "Aug") or
                     (month == "Jul") or
                     (month == "Sep"))  else "grey" for month in df_theft_calls['Call Month'].unique()}

#plot theft calls by month
plt.figure(figsize=(16, 8))
sns.set(style="darkgrid")
ax = sns.countplot(y="Call Month", data=df_theft_calls, 
                   palette=pal, 
                   order = df_theft_calls['Call Month'].value_counts().index)


# In[43]:


df_theft_calls['Call Month'].value_counts(normalize=True)


# In[44]:


#new dataframe for theft calls only in these summer and fall months
top_theft_calls = df_theft_calls[(df_theft_calls['Call Month'] == 'Jun') | 
                                (df_theft_calls['Call Month'] == 'Jul') |
                                (df_theft_calls['Call Month'] == 'Aug') |
                                (df_theft_calls['Call Month'] == 'Sep') |
                                (df_theft_calls['Call Month'] == 'Oct')]


# In[45]:


top_theft_calls['Call Day'].value_counts(normalize=True)


# In[46]:


#plot all theft calls by day
plt.figure(figsize=(8, 6))
sns.set(style="darkgrid")
ax = sns.countplot(x="Call Day", data=df_theft_calls, 
                   palette='summer', order = df_theft_calls['Call Day'].value_counts().index)


# In[48]:


#plot all theft calls by time of day
plt.figure(figsize=(8, 6))
sns.set(style="darkgrid")
ax = sns.countplot(x="Call Time of Day", data=df_theft_calls, 
                   palette='summer', order = df_theft_calls['Call Time of Day'].value_counts().index)


# In[49]:


df_theft_calls['Call Time of Day'].value_counts(normalize=True)


# In[50]:


#count unique results of each call for theft
df_theft_calls['Disposition Description'].value_counts()


# In[51]:


#generate a folium map to view locations of theft calls
def generateBaseMap(default_location=[36.16863, -86.7850], default_zoom_start=11):
    base_map = folium.Map(location=default_location, control_scale=True, zoom_start=default_zoom_start)
    return base_map


# In[52]:


#use a sample of 10,000 calls (out of 37,715) for increased rendering speed
theft = df_theft_calls.sample(10000)
#drop NaN values to graph properly
theft = theft.dropna()


# In[53]:


#create an instance of the map
basemap = generateBaseMap()


# In[54]:


#render map with popups labeling the day, month, and call time of each point in blue
theft.apply(lambda row: folium.Circle(location=[row['Latitude'], row['Longitude']],
                                         popup=('Day: {}, Month: {}, Time: {}'.format(row['Call Day'], 
                                                row['Call Month'], row['Call Time of Day'])),
                                    radius=100, color='Blue', fill_color='Blue').add_to(basemap), axis=1)

basemap


# In[56]:


#generate a folium heat map to differentiate between areas of higher call volume
map_heatmap = folium.Map([36.16863, -86.7850], zoom_start=11)

theft_heat = theft[['Latitude', 'Longitude']]
theft_heat = [[row['Latitude'],row['Longitude']] for index, row in theft_heat.iterrows()]

HeatMap(theft_heat, min_opacity=0.2).add_to(map_heatmap)

map_heatmap


# In[57]:


#create new df filtered by most popular theft call times of morning and afternoon (8a - 4p)
theft_business = df_theft_calls[(df_theft_calls['Call Time of Day'] == 'Morning') |
                               (df_theft_calls['Call Time of Day'] == 'Afternoon')]


# In[58]:


theft_business.head()


# In[59]:


theft_business.shape


# In[60]:


map_heatmap = folium.Map([36.16863, -86.7850], zoom_start=11)

theft_heat_business = theft_business[['Latitude', 'Longitude']].sample(5000).dropna()
theft_heat_business = [[row['Latitude'],row['Longitude']] for index, row in theft_heat_business.iterrows()]

HeatMap(theft_heat_business, min_opacity=0.2).add_to(map_heatmap)

map_heatmap


# In[61]:


theft_business['Disposition Description'].value_counts()


# In[62]:


#create new df filtered by all hours outside of morning and afternoon 
theft_non_business = df_theft_calls[~((df_theft_calls['Call Time of Day'] == 'Morning') |
                               (df_theft_calls['Call Time of Day'] == 'Afternoon'))]


# In[63]:


theft_non_business.shape


# In[64]:


theft_non_business['Disposition Description'].value_counts()


# In[65]:


map_heatmap = folium.Map([36.16863, -86.7850], zoom_start=11)

theft_heat_non = theft_non_business[['Latitude', 'Longitude']].sample(5000).dropna()
theft_heat_non = [[row['Latitude'],row['Longitude']] for index, row in theft_heat_non.iterrows()]

HeatMap(theft_heat_non, min_opacity=0.2).add_to(map_heatmap)

map_heatmap


# In[66]:


#create new df filtered by weekend days of saturday and sunday
theft_calls_weekend = df_theft_calls[(df_theft_calls['Call Day'] == 'Saturday') |
                               (df_theft_calls['Call Day'] == 'Sunday')]
theft_calls_weekend.shape


# In[67]:


#create new df filtered by non-weekend days of monday through friday
theft_calls_week = df_theft_calls[~((df_theft_calls['Call Day'] == 'Saturday') |
                               (df_theft_calls['Call Day'] == 'Sunday'))]
theft_calls_week.shape


# In[68]:


theft_calls_weekend['Call Time of Day'].value_counts()


# In[69]:


theft_calls_week['Call Time of Day'].value_counts()


# In[74]:


#heatmap for weekend theft calls
map_heatmap = folium.Map([36.16863, -86.7850], zoom_start=15)

theft_heat_weekend = theft_calls_weekend[['Latitude', 'Longitude']].sample(5000).dropna()
theft_heat_weekend = [[row['Latitude'],row['Longitude']] for index, row in theft_heat_weekend.iterrows()]

HeatMap(theft_heat_weekend, min_opacity=0.2).add_to(map_heatmap)

map_heatmap


# In[75]:


#heatmap for weekday theft calls
map_heatmap = folium.Map([36.16863, -86.7850], zoom_start=15)

theft_heat_weekday = theft_calls_week[['Latitude', 'Longitude']].sample(5000).dropna()
theft_heat_weekday = [[row['Latitude'],row['Longitude']] for index, row in theft_heat_weekday.iterrows()]

HeatMap(theft_heat_weekday, min_opacity=0.2).add_to(map_heatmap)

map_heatmap


# In[76]:


theft_calls_week['Call Day'].value_counts()


# In[77]:


#plot frequency of calls by day during the week days (excluding weekend)
plt.figure(figsize=(8, 6))
sns.set(style="darkgrid")
ax = sns.countplot(x="Call Day", data=theft_calls_week, 
                   palette='cividis', order = theft_calls_week['Call Day'].value_counts().index)


# In[213]:


#color bars for months between May 20 and November 3 (Highest call months)
pal = {week: "r" if (((week >= 21) & 
                     (week <= 44)) |
                     (week == 52)) else "blue" for week in df_theft_calls['Call Week'].unique()}

#plotting theft calls by week number
plt.figure(figsize=(16, 6))
sns.set(style="darkgrid")
ax = sns.countplot(x="Call Week", data=df_theft_calls, 
                   palette=pal).set_title('Theft Calls by Week')


# In[89]:


#create new df filtered by the top summer - fall weeks for theft calls using graph above
top_week_calls = df_theft_calls[(df_theft_calls['Call Week'] >= 21) & (df_theft_calls['Call Week'] <= 44)]


# In[90]:


top_week_calls.shape


# In[222]:


top_week_calls['Call Week'].value_counts().head(5)


# In[93]:


top_week_calls['Call Week'].value_counts(normalize=True).head(5)


# In[138]:


#create new df representing weekend of octoberfest 2019
oktober_fest = top_week_calls[(top_week_calls['Call Received'] >= '2019-10-10') &
                             (top_week_calls['Call Received'] <= '2019-10-13')]
oktober_fest.head(10)


# In[140]:


oktober_fest.shape


# In[145]:


#heatmap for oktoberfest theft calls
map_heatmap = folium.Map([36.176637, -86.788732], zoom_start=14)

oktober_fest_heat = oktober_fest[['Latitude', 'Longitude']].dropna()
oktober_fest_heat = [[row['Latitude'],row['Longitude']] for index, row in oktober_fest_heat.iterrows()]

HeatMap(oktober_fest_heat, min_opacity=0.6).add_to(map_heatmap)

map_heatmap


# In[146]:


#create new df representing 4 days of Vanderbilt University's 2019 homecoming weekend
vandy_homecoming = top_week_calls[(top_week_calls['Call Received'] >= '2019-10-17') &
                             (top_week_calls['Call Received'] <= '2019-10-20')]
vandy_homecoming.head(10)


# In[147]:


vandy_homecoming.shape


# In[148]:


map_heatmap = folium.Map([36.176637, -86.788732], zoom_start=11)

vandy_homecoming_heat = vandy_homecoming[['Latitude', 'Longitude']].dropna()
vandy_homecoming_heat = [[row['Latitude'],row['Longitude']] for index, row in vandy_homecoming_heat.iterrows()]

HeatMap(vandy_homecoming_heat, min_opacity=0.6).add_to(map_heatmap)

map_heatmap


# In[149]:


vandy_homecoming['Call Time of Day'].value_counts(normalize=True)


# In[153]:


#create new df representing saturday and sunday of homecoming weekend
vandy_concert = vandy_homecoming[(vandy_homecoming['Call Received'] >= '2019-10-18') &
                                (vandy_homecoming['Call Received'] <= '2019-10-19')]
vandy_concert.head()


# In[154]:


vandy_concert['Call Time of Day'].value_counts(normalize=True)


# In[223]:


df_theft_calls['Call Week'].value_counts()


# In[159]:


#create new df filtered by the last week of the year, which includes Christmas and New Years Eve
final_week = df_theft_calls[(df_theft_calls['Call Week'] == 52)]
final_week.shape


# In[162]:


final_week['Call Time of Day'].value_counts(normalize=True)


# In[165]:


final_week['Disposition Description'].value_counts()


# In[169]:


#heatmap of theft calls during week 52 of  2019
map_heatmap = folium.Map([36.176637, -86.788732], zoom_start=11)

final_week_heat = final_week[['Latitude', 'Longitude']].dropna()
final_week_heat = [[row['Latitude'],row['Longitude']] for index, row in final_week_heat.iterrows()]

HeatMap(final_week_heat, min_opacity=0.5).add_to(map_heatmap)

map_heatmap


# In[175]:


#create new df filtered to include only christmas eve and christmas day
christmas = df_theft_calls[(df_theft_calls['Call Received'] >= '2019-12-24') &
                                (df_theft_calls['Call Received'] <= '2019-12-25')]
christmas.shape


# In[180]:


christmas['Call Time of Day'].value_counts(normalize=True)


# In[184]:


pie = (christmas['Call Time of Day'].value_counts(normalize=True)).values


# In[186]:


pie


# In[187]:


labels = ['Morning','Afternoon','Evening','Night','Early Morning','Late Night']


# In[199]:


plt.pie(pie, labels=labels,
        autopct='%1.1f%%', shadow=True)
        
#draw a circle at the center of pie to make it look like a donut
centre_circle = plt.Circle((0,0),0.8,color='white', fc='white',linewidth=1.5)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)


# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')
plt.show()  


# In[200]:


christmas['Disposition Description'].value_counts()


# In[202]:


#heatmap of theft calls on christmas eve and christmas day
map_heatmap = folium.Map([36.176637, -86.788732], zoom_start=11)

christmas_heat = christmas[['Latitude', 'Longitude']].dropna()
christmas_heat = [[row['Latitude'],row['Longitude']] for index, row in christmas_heat.iterrows()]

HeatMap(christmas_heat, min_opacity=0.6).add_to(map_heatmap)

map_heatmap


# In[204]:


#create new df for new years eve
nye = df_theft_calls[(df_theft_calls['Call Received'] >= '2019-12-31')]
nye.shape


# In[207]:


nye['Call Time of Day'].value_counts(normalize=True)


# In[206]:


nye['Disposition Description'].value_counts()


# In[208]:


nye.head()


# In[209]:


#heatmap of theft calls on new years eve
map_heatmap = folium.Map([36.176637, -86.788732], zoom_start=11)

nye_heat = nye[['Latitude', 'Longitude']].dropna()
nye_heat = [[row['Latitude'],row['Longitude']] for index, row in nye_heat.iterrows()]

HeatMap(nye_heat, min_opacity=0.6).add_to(map_heatmap)

map_heatmap


# In[215]:


#import and read 2018 Calls for Service
df_2018 = pd.read_csv("Metro_Nashville_Police_Department_Calls_for_Service__2018_.csv", index_col='Event Number')
df_2018.head()


# In[216]:


#check for any incorrect values
df_2018['Tencode Description'].unique()


# In[218]:


#count total number of 2018 calls for theft
(df_2018['Tencode Description'] == 'Theft').value_counts()


# In[219]:


df_theft_calls['Call Time of Day'].value_counts(normalize=True)


# In[ ]:




