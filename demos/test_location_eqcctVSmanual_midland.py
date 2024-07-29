import matplotlib.pyplot as plt
import numpy as np
import os

f=open('../data/midland_eqcct_locations.csv')
lines=f.readlines()
lines=lines[2:]
lons=[float(ii.split(',')[6]) for ii in lines]
lats=[float(ii.split(',')[5]) for ii in lines]
deps=[float(ii.split(',')[7]) for ii in lines]
ids=[ii.split(',')[0].split('/')[-1] for ii in lines]
# lons=np.float(lons)
# lats=np.float(lats)

f=open('../data/midland_manual_locations.csv')
lines=f.readlines()
lines=lines[2:]
lons0=[float(ii.split(',')[6]) for ii in lines]
lats0=[float(ii.split(',')[5]) for ii in lines]
deps0=[float(ii.split(',')[7]) for ii in lines]
ids0=[ii.split(',')[0].split('/')[-1] for ii in lines]
# lons0=np.float(lons0)
# lats0=np.float(lats0)


iis=[]
iis0=[]
x=[]
y=[]
z=[]
x0=[]
y0=[]
z0=[]
for ii in range(len(ids)):
	
	if ids[ii] in ids0:
		ii0=ids0.index(ids[ii])
		iis.append(ii)
		iis0.append(ii0)
		if ids[ii] == ids0[ii0]:
			print(ii,'id matches')
		else:
			print(ii,'id does not match')
		x.append(lons[ii])
		y.append(lats[ii])
		z.append(deps[ii])
		x0.append(lons0[ii0])
		y0.append(lats0[ii0])
		z0.append(deps0[ii0])
	else:
		print(ids[ii]+' is not in manual catalog')

print('NO of events is ',len(iis))




## Analyze the accuracy
import numpy as np
x=np.array(x)
y=np.array(y)
z=np.array(z)

x0=np.array(x0)
y0=np.array(y0)
z0=np.array(z0)

print('MAEs in X (deg),Y(deg),Z(km) are ',abs(x-x0).sum()/len(x),abs(y-y0).sum()/len(y),abs(z-z0).sum()/len(z))
print('Median AEs in X (deg),Y(deg),Z(km) are ',np.median(abs(x-x0)),np.median(abs(y-y0)),np.median(abs(z-z0)))

fig = plt.figure(figsize=(6, 11))
ax = plt.subplot(3,1,1)
plt.plot(x,y,color='k', marker='o', markersize=6, linestyle='None', markerfacecolor="red",alpha=0.5,label='EQCCT');
plt.plot(x0,y0,color='k', marker='o', markersize=6, linestyle='None', markerfacecolor="silver",alpha=0.5,label='Manual');

for ii in range(len(x)):
	plt.plot([x[ii],x0[ii]],[y[ii],y0[ii]],'-',color='g',linewidth=2)
# 
# ii=0;plt.plot([x[ii],y[ii]],[x0[ii],y0[ii]],'-',color='g',linewidth=2,label='Error');

lon1=-103.28;#lon1=-104.2
lon2=-101.43;#lon2=-103.9
lat1=30.8;
lat2=33.3;
# lat1=31.3-0.05;lat1=31.5;
# lat2=31.9+0.05;lat2=31.7;
# plt.gca().set_ylim(ymin=lat1,ymax=lat2);
plt.gca().set_xlim(xmin=lon1,xmax=lon2);
plt.gca().set_ylabel("latitude (deg)",fontsize='medium', fontweight='normal')
plt.gca().set_xlabel("Longitude (deg)",fontsize='medium', fontweight='normal')
# 
## add scale
plt.plot([0.025+lon1,0.025+lon1+20/111.0],[0.025+lat1,0.025+lat1],color='k',linewidth=4)
plt.text(0.035+lon1,0.08+lat1,'20 km')
plt.gca().set_xticks(np.linspace(plt.gca().get_xlim()[0],plt.gca().get_xlim()[1],5));
plt.title('Midland',fontsize='large', fontweight='normal')
plt.gca().text(-0.18,1.05,'(a)',transform=plt.gca().transAxes,size=20,weight='normal')
# 
ax = plt.subplot(3,1,2)
# df_delaware = df_delaware[df_delaware['mag_eqcct']>=1.9]
plt.plot(x,z,color='k', marker='o', markersize=6, linestyle='None', markerfacecolor="red",alpha=0.5,label='EQCCT');
plt.plot(x0,z0,color='k', marker='o', markersize=6, linestyle='None', markerfacecolor="silver",alpha=0.5,label='Manual');
# 
for ii in range(len(x)):
	plt.plot([x[ii],x0[ii]],[z[ii],z0[ii]],'-',color='g',linewidth=2)
# 
# ii=0;plt.plot([list(df_delaware['lon_eqcct'])[ii],list(df_delaware['lon_pref'])[ii]],[list(df_delaware['dep_eqcct'])[ii],list(df_delaware['dep_pref'])[ii]],'-',color='g',linewidth=2,label='Error');
# 
# lon1=-104.7-0.1;lon1=-104.2
# lon2=-103.7+0.1;lon2=-103.9
# lat1=31.3-0.05;lat1=31.5;
# lat2=31.9+0.05;lat2=31.7;
# # plt.gca().set_ylim(ymin=lat1,ymax=lat2);
plt.gca().set_xlim(xmin=lon1,xmax=lon2);
plt.gca().set_ylabel("Depth (km)",fontsize='medium', fontweight='normal')
plt.gca().set_xlabel("Longitude (deg)",fontsize='medium', fontweight='normal')
# # plt.gca().legend(loc='lower right');
plt.gca().invert_yaxis()
plt.gca().set_xticks(np.linspace(plt.gca().get_xlim()[0],plt.gca().get_xlim()[1],5));
plt.gca().text(-0.18,1.05,'(b)',transform=plt.gca().transAxes,size=20,weight='normal')
# 
ax = plt.subplot(3,1,3)
plt.plot(y,z,color='k', marker='o', markersize=6, linestyle='None', markerfacecolor="red",alpha=0.5,label='EQCCT');
plt.plot(y0,z0,color='k', marker='o', markersize=6, linestyle='None', markerfacecolor="silver",alpha=0.5,label='Manual');
# 
for ii in range(len(x)):
	plt.plot([y[ii],y0[ii]],[z[ii],z0[ii]],'-',color='g',linewidth=2)
ii=0;plt.plot([y[ii],y0[ii]],[z[ii],z0[ii]],'-',color='g',linewidth=2,label='Error')
# # plt.gca().set_ylim(ymin=lat1,ymax=lat2);
plt.gca().set_xlim(xmin=lat1,xmax=lat2);
plt.gca().set_ylabel("Depth (km)",fontsize='medium', fontweight='normal')
plt.gca().set_xlabel("Latitude (deg)",fontsize='medium', fontweight='normal')
plt.gca().legend(loc='lower right');
plt.gca().invert_yaxis()
plt.gca().set_xticks(np.linspace(plt.gca().get_xlim()[0],plt.gca().get_xlim()[1],5));
# plt.savefig('location1.png',format='png',dpi=300,bbox_inches='tight', pad_inches=0)
plt.gca().text(-0.18,1.05,'(c)',transform=plt.gca().transAxes,size=20,weight='normal')


plt.savefig('location_eqcctVSmanual_midland.png',format='png',dpi=300)
plt.show()

