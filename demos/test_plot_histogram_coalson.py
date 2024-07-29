import pandas as pd
from geopy.distance import geodesic # pip install geopy

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os
# sns.set(style="whitegrid", font_scale=1.8)


## OPTION 1 (real-time data extraction)
# import sqlalchemy as sql
# import mysql.connector # pip install mysql-connector-python
# mydb = mysql.connector.connect(host="sc3primary.beg.utexas.edu",
#                                user="sysop",
#                                passwd="sysop",
#                                database="seiscomp3")
# 
# '''connect_string = 'mysql://sysop:sysop@sc3primary.beg.utexas.edu/seiscomp3'
# mydb = sql.create_engine(connect_string)'''
# 
# #author = 'lN3screloc@sc3primary.beg.utexas.edu'
# author = 'EQCCT'
# query = '''
# select POE.publicID as id,
# pref_o.creationInfo_author AS 'author pref',
# pref_o.evaluationStatus as 'sta_pref',
# eqcct_o.creationInfo_author AS 'author eqcct',
# eqcct_o.evaluationStatus as 'sta_eqcct',
# Event.type as 'event type',
# DATE_FORMAT(pref_o.time_value, '%Y/%m/%d %H:%i:%S') AS 'time_pref',
# ROUND(mag_pref.magnitude_value,2) AS 'mag_pref',
# ROUND(mag_eqcct.magnitude_value,2) AS 'mag_eqcct',
# mag_eqcct.stationCount as 'mag_sta_count_eqcct',
# mag_eqcct.magnitude_uncertainty as 'mag_unc_eqcct',
# mag_pref.type AS 'type_mag_pref',
# eqcct_o.quality_usedPhaseCount as 'phase_count_eqcct',
# eqcct_o.quality_minimumDistance as 'min_dist_eqcct',
# eqcct_o.quality_maximumDistance as 'max_dist_eqcct',
# max(eqcct_o.quality_usedPhaseCount) AS max_phases,
# ROUND(pref_o.latitude_value, 2) AS 'lat_pref',
# ROUND(pref_o.longitude_value, 2) AS 'lon_pref',
# ROUND(eqcct_o.latitude_value, 2) AS 'lat_eqcct',
# ROUND(eqcct_o.longitude_value, 2) AS 'lon_eqcct',
# pref_o.depth_value AS 'dep_pref',
# eqcct_o.depth_value AS 'dep_eqcct',
# eqcct_o.latitude_uncertainty as 'lat_unc_eqcct',
# eqcct_o.longitude_uncertainty as 'lon_unc_eqcct',
# eqcct_o.depth_uncertainty as 'dep_unc_eqcct',
# ROUND(eqcct_o.quality_standardError,3) AS 'eqcct_rms'
# from
# Event inner join OriginReference on Event._oid=OriginReference._parent_oid
# inner join PublicObject as POE on Event._oid=POE._oid
# inner join PublicObject as POOeqcct on POOeqcct.publicID=OriginReference.originID
# inner join PublicObject as POOpref  on POOpref.publicID=Event.preferredOriginID
# inner join Origin as eqcct_o on POOeqcct._oid=eqcct_o._oid and eqcct_o.creationInfo_author = '{author}'
# inner join Origin as pref_o on POOpref._oid=pref_o._oid
# left join Magnitude as mag_eqcct ON mag_eqcct.originID = OriginReference.originID
# left join PublicObject as POMag_pref on Event.preferredMagnitudeID=POMag_pref.publicID
# left join Magnitude as mag_pref ON mag_pref._oid = POMag_pref._oid
# left join EventDescription ON Event._oid=EventDescription._parent_oid  
# where
# pref_o.time_value between '2022-11-28 00:00:00' AND '2022-12-31 23:59:59'
# #and pref_o.evaluationStatus in ('final', 'rejected', 'reported', 'preliminary','not existing')
# and pref_o.evaluationStatus in ('final', 'reported', 'preliminary')
# and mag_eqcct.type = 'ML(TexNet)'
# and mag_pref.type = 'ML(TexNet)'
# group by POE.publicID
# having phase_count_eqcct = max_phases
# '''.format(author=author)
# 
# df = pd.read_sql(query, mydb)
# df.to_csv('coalson20221128_20221231.csv')

## OPTION 2 (Read saved data)
#another PATH on local repository
#df=pd.read_csv(os.getenv('HOME')+'/chenyk.data2/various/cyksmall/texnet/realtime/coalson20221128_20221231.csv')
df=pd.read_csv('../data/coalson20221128_20221231.csv')

# compute the difference between the two magnitudes
df['mag_diff'] = df['mag_eqcct'] - df['mag_pref']
# computing the epicentral distance between the eqcct origin and the preferred origin using Vincenty's formula
df['epicentral_distance'] = df.apply(lambda x: geodesic((x['lat_eqcct'], x['lon_eqcct']), (x['lat_pref'], x['lon_pref'])).km, axis=1)
# Creating the region column and assigning 'midland' if the longitude is greater than -102.3 and 'delaware' otherwise 
df['region'] = df['lon_pref'].apply(lambda x: 'midland' if x > -102.3 else 'delaware')
# Creating lat_unc, lon_unc and depth_unc columns and assigning high if the uncertainty is greater than 15 and normal otherwise
df['lat_unc'] = df['lat_unc_eqcct'].apply(lambda x: 'high' if abs(x) > 15 else 'normal')
df['lon_unc'] = df['lon_unc_eqcct'].apply(lambda x: 'high' if abs(x) > 15 else 'normal')
df['depth_unc'] = df['dep_unc_eqcct'].apply(lambda x: 'high' if abs(x) > 15 else 'normal')

# keeping only midland earthquakes
# df_midland = df[df['region'] == 'midland']
# 
# # plot histogram of the difference between origin_creation_time and pick_creation_time
# df['mag_diff'].plot.hist(bins=20, figsize=(15, 7), color='steelblue', alpha=0.9)
# # add a vertical line at the mean and text at the same height of the highest bar
# plt.axvline(df['mag_diff'].mean(), color='k', linestyle='dashed', linewidth=2)
# plt.text(df['mag_diff'].mean() + df['mag_diff'].std(), 400, 'Mean: {:.2f} +/- {:.2f}'.format(df['mag_diff'].mean(), df['mag_diff'].std()))
# plt.xlabel('Magnitude difference')
# plt.title('Delaware and Midland')
# plt.ylabel('Number of earthquakes')
# 
# plt.show()
# 
# df_midland = df[df['region'] == 'midland']
df_delaware = df[df['region'] == 'delaware']

df['region'].value_counts()
print(df['region'].value_counts())

#


# plot histogram of the difference between origin_creation_time and pick_creation_time with bins every 0.1
#df_delaware['mag_diff'].plot.hist(bins=np.arange(-1, 1, 0.1), figsize=(15, 7), color='steelblue', alpha=0.9)
# df_delaware['mag_diff'].plot.hist(bins=20, figsize=(15, 7), color='steelblue', alpha=0.9)
# # adding a legend
# #plt.legend(['Midland', 'Delaware'])
# 
# plt.xlabel('Magnitude difference',fontsize='large', fontweight='normal')
# plt.title('Coalson',fontsize='large', fontweight='normal')
# plt.ylabel('Number of origins',fontsize='large', fontweight='normal')
# # plt.savefig('coalson1.png',format='png',dpi=300,bbox_inches='tight', pad_inches=0)
# plt.show()


fig = plt.figure(figsize=(8, 8))
ax = plt.subplot(2,1,1)

plt.hist(df_delaware['mag_diff'],20,label='EQCCT',color='blue',edgecolor='black')
plt.gca().set_xlim(xmin=-1.5,xmax=1.5);
plt.gca().legend(loc='lower right');
plt.gca().set_ylabel("Count",fontsize='large', fontweight='normal')
plt.gca().set_xlabel("Magnitude difference",fontsize='large', fontweight='normal')
plt.title('Coalson',fontsize='large', fontweight='normal')
plt.axvline(df_delaware['mag_diff'].mean(), color='r', linestyle='dashed', linewidth=2)
plt.text(df_delaware['mag_diff'].mean() + df_delaware['mag_diff'].std(), 400, 'Mean: {:.2f} +/- {:.2f}'.format(df_delaware['mag_diff'].mean(), df_delaware['mag_diff'].std()),color='r',fontsize='large', fontweight='normal')
#df_delaware['mag_diff'].plot.hist(bins=20, figsize=(15, 7), color='red', alpha=0.2)
plt.gca().text(-0.15,1,'(a)',transform=plt.gca().transAxes,size=20,weight='normal')

ax = plt.subplot(2,1,2)


max_eqcct = df_delaware['mag_eqcct'].max()
max_pref = df_delaware['mag_pref'].max()

# the above plot but with editing the legend tittle to "event status" instead of "sta_pref"
# g = sns.relplot(x='mag_pref', y='mag_eqcct', data=df_delaware, kind='scatter', color='steelblue', height=8, aspect=1.8, hue='sta_pref', alpha=0.5)


df1=df_delaware[df_delaware['sta_pref']=='reported']
df2=df_delaware[df_delaware['sta_pref']=='preliminary']
df3=df_delaware[df_delaware['sta_pref']=='final']

plt.plot(df1['mag_pref'],df1['mag_eqcct'], color='blue', marker='o',
     linewidth=2, markersize=12, alpha=0.5, fillstyle='full', linestyle='none', label='Reported')
plt.plot(df2['mag_pref'],df2['mag_eqcct'], color='green', marker='o',
     linewidth=2, markersize=12, alpha=0.5, fillstyle='full', linestyle='none', label='Preliminary')
plt.plot(df3['mag_pref'],df3['mag_eqcct'], color='red', marker='o',
     linewidth=2, markersize=12, alpha=0.5, fillstyle='full', linestyle='none', label='Final')
plt.gca().legend(loc='lower right', fontsize = 10, title='Event status')
# 
# # plot a red dotted line at mag_eqcct = 1.9
plt.axhline(1.9, color='red', linestyle='dashed', linewidth=2)
# # plot a green dashed line at mag_pref = 2
plt.axvline(2, color='green', linestyle='dashed', linewidth=2)
plt.text(2.01, 2.7, 'M=2.0',fontsize='large', fontweight='normal')
# # plot a black dotted line at mag_pref = mag_eqcct
plt.plot([0, max_eqcct], [0, max_eqcct], color='black', linestyle='dotted', linewidth=2)
# # add a text box with the mean and standard deviation of the magnitude difference
plt.text(2.5, 1.95, 'M=1.9',fontsize='large', fontweight='normal')
# # plt.gca()._legend.set_title('Event status')
plt.xlabel('Preferred magnitude',fontsize='large', fontweight='normal')
plt.ylabel('Magnitude from EQCCT',fontsize='large', fontweight='normal')
plt.gca().text(-0.15,1,'(b)',transform=plt.gca().transAxes,size=20,weight='normal')

plt.savefig('coalson_fig.png',format='png',dpi=300,bbox_inches='tight', pad_inches=0)
plt.show()


dff=df_delaware[df_delaware['mag_pref']>=2.0]
print('M2 events are',dff.shape)
dff[dff['mag_eqcct']<1.9]['mag_eqcct']









