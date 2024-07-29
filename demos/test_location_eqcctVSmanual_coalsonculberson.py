import pandas as pd
from geopy.distance import geodesic # pip install geopy
#import sqlalchemy as sql
# import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
# sns.set(style="whitegrid", font_scale=1.8)
import os
#import sqlalchemy as sql
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
# plt.axvline(df['mag_diff'].mean(), color='k', linestyle='dashed', linewidth=1)
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

df_delaware = df_delaware[df_delaware['mag_eqcct']>=1.9]
print('MAE of magnitude is',np.mean(np.abs(df_delaware['mag_eqcct']-df_delaware['mag_pref'])))
print('MAE of epiceter is',np.mean(np.sqrt(np.power(np.abs(df_delaware['lon_eqcct']-df_delaware['lon_pref']),2)+np.power(np.abs(df_delaware['lat_eqcct']-df_delaware['lat_pref']),2))*111.0))
df2=df_delaware[df_delaware['dep_eqcct']<10]
print('MAE of depth is',np.mean(np.abs(df2['dep_eqcct']-df2['dep_pref'])))


# Plot location
fig = plt.figure(figsize=(12, 12))
ax = plt.subplot(3,2,1)
plt.plot(df_delaware['lon_eqcct'],df_delaware['lat_eqcct'],color='k', marker='o', markersize=6, linestyle='None', markerfacecolor="red",alpha=0.5,label='EQCCT');
plt.plot(df_delaware['lon_pref'],df_delaware['lat_pref'],color='k', marker='o', markersize=6, linestyle='None', markerfacecolor="silver",alpha=0.5,label='Manual');

for ii in range(len(df_delaware)):
	plt.plot([list(df_delaware['lon_eqcct'])[ii],list(df_delaware['lon_pref'])[ii]],[list(df_delaware['lat_eqcct'])[ii],list(df_delaware['lat_pref'])[ii]],'-',color='g',linewidth=2)

ii=0;plt.plot([list(df_delaware['lon_eqcct'])[ii],list(df_delaware['lon_pref'])[ii]],[list(df_delaware['lat_eqcct'])[ii],list(df_delaware['lat_pref'])[ii]],'-',color='g',linewidth=2,label='Error');

lon1=-104.7-0.1;lon1=-104.2
lon2=-103.7+0.1;lon2=-103.9
lat1=31.3-0.05;lat1=31.5;
lat2=31.9+0.05;lat2=31.7;
plt.gca().set_ylim(ymin=lat1,ymax=lat2);
plt.gca().set_xlim(xmin=lon1,xmax=lon2);
plt.gca().set_ylabel("latitude (deg)",fontsize='medium', fontweight='normal')
plt.gca().set_xlabel("Longitude (deg)",fontsize='medium', fontweight='normal')

## add scale
plt.plot([0.025+lon1,0.025+lon1+5/111.0],[0.025+lat1,0.025+lat1],color='k',linewidth=4)
plt.text(0.03+lon1,0.03+lat1,'5 km')
plt.gca().set_xticks(np.linspace(plt.gca().get_xlim()[0],plt.gca().get_xlim()[1],5));
plt.title('Coalson',fontsize='large', fontweight='normal')
plt.gca().text(-0.18,1.05,'(a)',transform=plt.gca().transAxes,size=20,weight='normal')

ax = plt.subplot(3,2,3)
df_delaware = df_delaware[df_delaware['mag_eqcct']>=1.9]
plt.plot(df_delaware['lon_eqcct'],df_delaware['dep_eqcct'],color='k', marker='o', markersize=6, linestyle='None', markerfacecolor="red",alpha=0.5,label='EQCCT');
plt.plot(df_delaware['lon_pref'],df_delaware['dep_pref'],color='k', marker='o', markersize=6, linestyle='None', markerfacecolor="silver",alpha=0.5,label='Manual');

for ii in range(len(df_delaware)):
	plt.plot([list(df_delaware['lon_eqcct'])[ii],list(df_delaware['lon_pref'])[ii]],[list(df_delaware['dep_eqcct'])[ii],list(df_delaware['dep_pref'])[ii]],'-',color='g',linewidth=2)

ii=0;plt.plot([list(df_delaware['lon_eqcct'])[ii],list(df_delaware['lon_pref'])[ii]],[list(df_delaware['dep_eqcct'])[ii],list(df_delaware['dep_pref'])[ii]],'-',color='g',linewidth=2,label='Error');

lon1=-104.7-0.1;lon1=-104.2
lon2=-103.7+0.1;lon2=-103.9
lat1=31.3-0.05;lat1=31.5;
lat2=31.9+0.05;lat2=31.7;
# plt.gca().set_ylim(ymin=lat1,ymax=lat2);
plt.gca().set_xlim(xmin=lon1,xmax=lon2);
plt.gca().set_ylabel("Depth (km)",fontsize='medium', fontweight='normal')
plt.gca().set_xlabel("Longitude (deg)",fontsize='medium', fontweight='normal')
# plt.gca().legend(loc='lower right');
plt.gca().invert_yaxis()
plt.gca().set_xticks(np.linspace(plt.gca().get_xlim()[0],plt.gca().get_xlim()[1],5));
plt.gca().text(-0.18,1.05,'(c)',transform=plt.gca().transAxes,size=20,weight='normal')

ax = plt.subplot(3,2,5)
df_delaware = df_delaware[df_delaware['mag_eqcct']>=1.9]
plt.plot(df_delaware['lat_eqcct'],df_delaware['dep_eqcct'],color='k', marker='o', markersize=6, linestyle='None', markerfacecolor="red",alpha=0.5,label='EQCCT');
plt.plot(df_delaware['lat_pref'],df_delaware['dep_pref'],color='k', marker='o', markersize=6, linestyle='None', markerfacecolor="silver",alpha=0.5,label='Manual');

for ii in range(len(df_delaware)):
	plt.plot([list(df_delaware['lat_eqcct'])[ii],list(df_delaware['lat_pref'])[ii]],[list(df_delaware['dep_eqcct'])[ii],list(df_delaware['dep_pref'])[ii]],'-',color='g',linewidth=2)

ii=0;plt.plot([list(df_delaware['lat_eqcct'])[ii],list(df_delaware['lat_pref'])[ii]],[list(df_delaware['dep_eqcct'])[ii],list(df_delaware['dep_pref'])[ii]],'-',color='g',linewidth=2,label='Error');

lon1=-104.7-0.1;lon1=-104.2
lon2=-103.7+0.1;lon2=-103.9
lat1=31.3-0.05;lat1=31.5;
lat2=31.9+0.05;lat2=31.7;
# plt.gca().set_ylim(ymin=lat1,ymax=lat2);
plt.gca().set_xlim(xmin=lat1,xmax=lat2);
plt.gca().set_ylabel("Depth (km)",fontsize='medium', fontweight='normal')
plt.gca().set_xlabel("Latitude (deg)",fontsize='medium', fontweight='normal')
plt.gca().legend(loc='lower right');
plt.gca().invert_yaxis()
plt.gca().set_xticks(np.linspace(plt.gca().get_xlim()[0],plt.gca().get_xlim()[1],5));
# plt.savefig('location1.png',format='png',dpi=300,bbox_inches='tight', pad_inches=0)
plt.gca().text(-0.18,1.05,'(e)',transform=plt.gca().transAxes,size=20,weight='normal')

#conda activate daniel

import pandas as pd
from geopy.distance import geodesic  # pip install geopy
#import sqlalchemy as sql
# import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
# sns.set(style="whitegrid", font_scale=1.8)
# %matplotlib inline

import os

#import sqlalchemy as sql
# import mysql.connector  # pip install mysql-connector-python
# 
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
# lats = [31.4, 31.844]
# lons = [-104.718, -104.095]
# 
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
# pref_o.time_value between '2021-12-15 00:00:00' AND '2023-02-09 23:59:59'
# #and pref_o.evaluationStatus in ('final', 'rejected', 'reported', 'preliminary','not existing')
# and pref_o.evaluationStatus in ('final', 'reported', 'preliminary')
# and mag_eqcct.type = 'ML(TexNet)'
# and mag_pref.type = 'ML(TexNet)'
# and eqcct_o.latitude_value between '{min_lat}' and '{max_lat}'
# and eqcct_o.longitude_value between '{min_lon}' and '{max_lon}'
# group by POE.publicID
# having phase_count_eqcct = max_phases
# '''.format(author=author, min_lat=min(lats), max_lat=max(lats), min_lon=min(lons), max_lon=max(lons))
# 
# df = pd.read_sql(query, mydb)
# df.to_csv('culberson20221128_20221231.csv')

df=pd.read_csv('../data/culberson20221128_20221231.csv')


# df['time_pref'] = pd.to_datetime(df['time_pref'])
# # sorting the dataframe by time
# df = df.sort_values(by='time_pref')
# # compute the difference between the two magnitudes
# df['mag_diff'] = df['mag_eqcct'] - df['mag_pref']
# # check if the depth (m) is less than 30 km and lon, lat and depth (m) uncertainties are less than 20 km
# df['good_quality'] = (df['dep_eqcct'] < 30000) & (df['lat_unc_eqcct'] < 20) & (df['lon_unc_eqcct'] < 20) & (df['dep_unc_eqcct'] < 20)
# # analyzed column contains sta_pref preliminary or final
# # df['analized'] = df['sta_pref'].isin(['preliminary', 'final'])
# # computing the epicentral distance between the eqcct origin and the preferred origin using Vincenty's formula
# df['epicentral_distance'] = df.apply(lambda x: geodesic(
#     (x['lat_eqcct'], x['lon_eqcct']), (x['lat_pref'], x['lon_pref'])).km, axis=1)
# # Creating lat_unc, lon_unc and depth_unc columns and assigning high if the uncertainty is greater than 15 and normal otherwise
# df['lat_unc'] = df['lat_unc_eqcct'].apply(
#     lambda x: 'high' if abs(x) > 15 else 'normal')
# df['lon_unc'] = df['lon_unc_eqcct'].apply(
#     lambda x: 'high' if abs(x) > 15 else 'normal')
# df['depth_unc'] = df['dep_unc_eqcct'].apply(
#     lambda x: 'high' if abs(x) > 15 else 'normal')
# df['depth_type'] = df['dep_eqcct'].apply(
#     lambda x: 'shallow' if x < 15 else 'deep')

df['mag_diff'] = df['mag_eqcct'] - df['mag_pref']
# computing the epicentral distance between the eqcct origin and the preferred origin using Vincenty's formula
df['epicentral_distance'] = df.apply(lambda x: geodesic((x['lat_eqcct'], x['lon_eqcct']), (x['lat_pref'], x['lon_pref'])).km, axis=1)
# Creating the region column and assigning 'midland' if the longitude is greater than -102.3 and 'delaware' otherwise 
df['region'] = df['lon_pref'].apply(lambda x: 'midland' if x > -102.3 else 'delaware')
# Creating lat_unc, lon_unc and depth_unc columns and assigning high if the uncertainty is greater than 15 and normal otherwise
df['lat_unc'] = df['lat_unc_eqcct'].apply(lambda x: 'high' if abs(x) > 15 else 'normal')
df['lon_unc'] = df['lon_unc_eqcct'].apply(lambda x: 'high' if abs(x) > 15 else 'normal')
df['depth_unc'] = df['dep_unc_eqcct'].apply(lambda x: 'high' if abs(x) > 15 else 'normal')


print(df.head())

df = df[df['mag_eqcct']>=1.9]
print('MAE of magnitude is',np.mean(np.abs(df['mag_eqcct']-df['mag_pref'])))
print('MAE of epiceter is',np.mean(np.sqrt(np.power(np.abs(df['lon_eqcct']-df['lon_pref']),2)+np.power(np.abs(df['lat_eqcct']-df['lat_pref']),2))*111.0))
df2=df[df['dep_eqcct']<10]
print('MAE of depth is',np.mean(np.abs(df2['dep_eqcct']-df2['dep_pref'])))


ax = plt.subplot(3,2,2)
plt.plot(df['lon_eqcct'],df['lat_eqcct'],color='k', marker='o', markersize=6, linestyle='None', markerfacecolor="red",alpha=0.5,label='EQCCT');
plt.plot(df['lon_pref'],df['lat_pref'],color='k', marker='o', markersize=6, linestyle='None', markerfacecolor="silver",alpha=0.5,label='Manual');

for ii in range(len(df)):
	plt.plot([list(df['lon_eqcct'])[ii],list(df['lon_pref'])[ii]],[list(df['lat_eqcct'])[ii],list(df['lat_pref'])[ii]],'-',color='g',linewidth=2)

ii=0;plt.plot([list(df['lon_eqcct'])[ii],list(df['lon_pref'])[ii]],[list(df['lat_eqcct'])[ii],list(df['lat_pref'])[ii]],'-',color='g',linewidth=2,label='Error');

lon1=-104.7-0.1;#lon1=-104.2
lon2=-103.7+0.1;#lon2=-103.9
lat1=31.3-0.05;#lat1=31.5;
lat2=31.9+0.05;#lat2=31.7;
plt.gca().set_ylim(ymin=lat1,ymax=lat2);
plt.gca().set_xlim(xmin=lon1,xmax=lon2);
plt.gca().set_ylabel("latitude (deg)",fontsize='medium', fontweight='normal')
plt.gca().set_xlabel("Longitude (deg)",fontsize='medium', fontweight='normal')

## add scale
plt.plot([0.1+lon1,0.1+lon1+20/111.0],[0.075+lat1,0.075+lat1],color='k',linewidth=4)
plt.text(0.125+lon1,0.1+lat1,'20 km')
plt.gca().set_xticks(np.linspace(plt.gca().get_xlim()[0],plt.gca().get_xlim()[1],5));
plt.title('Culberson',fontsize='large', fontweight='normal')
plt.gca().text(-0.18,1.05,'(b)',transform=plt.gca().transAxes,size=20,weight='normal')

ax = plt.subplot(3,2,4)
df = df[df['mag_eqcct']>=1.9]
plt.plot(df['lon_eqcct'],df['dep_eqcct'],color='k', marker='o', markersize=6, linestyle='None', markerfacecolor="red",alpha=0.5,label='EQCCT');
plt.plot(df['lon_pref'],df['dep_pref'],color='k', marker='o', markersize=6, linestyle='None', markerfacecolor="silver",alpha=0.5,label='Manual');

for ii in range(len(df)):
	plt.plot([list(df['lon_eqcct'])[ii],list(df['lon_pref'])[ii]],[list(df['dep_eqcct'])[ii],list(df['dep_pref'])[ii]],'-',color='g',linewidth=2)

ii=0;plt.plot([list(df['lon_eqcct'])[ii],list(df['lon_pref'])[ii]],[list(df['dep_eqcct'])[ii],list(df['dep_pref'])[ii]],'-',color='g',linewidth=2,label='Error');

# plt.gca().set_ylim(ymin=lat1,ymax=lat2);
plt.gca().set_xlim(xmin=lon1,xmax=lon2);
plt.gca().set_ylabel("Depth (km)",fontsize='medium', fontweight='normal')
plt.gca().set_xlabel("Longitude (deg)",fontsize='medium', fontweight='normal')
# plt.gca().legend(loc='lower right');
plt.gca().invert_yaxis()
plt.gca().set_xticks(np.linspace(plt.gca().get_xlim()[0],plt.gca().get_xlim()[1],5));
plt.gca().text(-0.18,1.05,'(d)',transform=plt.gca().transAxes,size=20,weight='normal')

ax = plt.subplot(3,2,6)
df = df[df['mag_eqcct']>=1.9]
plt.plot(df['lat_eqcct'],df['dep_eqcct'],color='k', marker='o', markersize=6, linestyle='None', markerfacecolor="red",alpha=0.5,label='EQCCT');
plt.plot(df['lat_pref'],df['dep_pref'],color='k', marker='o', markersize=6, linestyle='None', markerfacecolor="silver",alpha=0.5,label='Manual');

for ii in range(len(df)):
	plt.plot([list(df['lat_eqcct'])[ii],list(df['lat_pref'])[ii]],[list(df['dep_eqcct'])[ii],list(df['dep_pref'])[ii]],'-',color='g',linewidth=2)

ii=0;plt.plot([list(df['lat_eqcct'])[ii],list(df['lat_pref'])[ii]],[list(df['dep_eqcct'])[ii],list(df['dep_pref'])[ii]],'-',color='g',linewidth=2,label='Error');

# plt.gca().set_ylim(ymin=lat1,ymax=lat2);
plt.gca().set_xlim(xmin=lat1,xmax=lat2);
plt.gca().set_ylabel("Depth (km)",fontsize='medium', fontweight='normal')
plt.gca().set_xlabel("Latitude (deg)",fontsize='medium', fontweight='normal')
plt.gca().legend(loc='lower right');
plt.gca().invert_yaxis()
plt.gca().set_xticks(np.linspace(plt.gca().get_xlim()[0],plt.gca().get_xlim()[1],5));
plt.gca().text(-0.18,1.05,'(f)',transform=plt.gca().transAxes,size=20,weight='normal')

plt.savefig('location_eqcctVSmanual_coalsonculberson.png',format='png',dpi=300,bbox_inches='tight', pad_inches=0)
plt.show()

# Coalson
# MAE of magnitude is 0.15137931034482754
# MAE of epiceter is 2.0368436047179066
# MAE of depth is 1.338398258566038
# Culberson
# MAE of magnitude is 0.11423076923076926
# MAE of epiceter is 2.5915773616087496
# MAE of depth is 2.26465474854902
