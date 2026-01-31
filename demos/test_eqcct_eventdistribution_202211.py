import os
#pyseistr can be installed by pip install pyseistr
def create_catalog(eids,fincatalog=None,foutcatalog=None):
	"""
	Create TexNet style catalog from event list eids
	Written by Yangkang Chen
	Oct, 19, 2022
	
	INPUT
	eids:
	fcatalog: Input (complete) Texas Catalog
	
	OUTPUT
	foutcatalog: a csv catalog file written on the disk
	
	Example
	from pylib.texnet import create_catalog
	eids=['texnet2020galz']
	create_catalog(eids)
	"""
	from pyseistr import asciiwrite
	
	if fincatalog is None:
		fincatalog='../data/texnet_events_20221220.csv';
	
	if foutcatalog is None:
		foutcatalog='./newcatalog.csv'
	
	f=open(fincatalog);
	lines=f.readlines();
	
	lines2=[]
	lines2.append(lines[0])
	for ii in range(len(lines)-1):
		if lines[ii+1].split(',')[0] in eids:
			lines2.append(lines[ii+1])
	asciiwrite(foutcatalog,lines2,withnewline=True)
	
import numpy as np
import sys,os
from pyseistr import asciiread,asciiwrite
import obspy.core.utcdatetime as utc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

if3month=False

if if3month==True: #three-month version or one-month version
	## Read EQCCT result
	f=open('../data/catalogs/delaware_11140_events.csv') #202008
	lines1=f.readlines()
	f=open('../data/catalogs/delaware_10867_events.csv') #202009
	lines2=f.readlines()
	f=open('../data/catalogs/delaware_11687_events.csv') #202010
	lines3=f.readlines()
	lines1=lines1[1:]
	lines2=lines2[1:]
	lines3=lines3[1:]
	lines=lines1+lines2+lines3;
else:
# 	f=open('../data/catalogs/delaware_11687_events.csv') #202010
	f=open('../data/delaware202211_10746.csv') #202011
	lines=f.readlines()[1:]
	
## Read reported events
fname='../data/texnet__20170101-20230315_on20230315.asc'

lons1=[float(ii.split(',')[9]) for ii in lines]
lats1=[float(ii.split(',')[8]) for ii in lines]
deps1=[float(ii.split(',')[10]) for ii in lines]
ids1=[ii.split(',')[0].split('/')[-1] for ii in lines]

mags1=[float(ii.split(',')[7]) for ii in lines]
rmss1=[float(ii.split(',')[-1]) for ii in lines]

utcs1=[utc.UTCDateTime(ii.split(',')[6].split(' ')[0]+'T'+ii.split(',')[6].split('+')[0].split(' ')[1]) for ii in lines]

t=[]
for ii in rmss1:
	if ii<1.0:
		t.append(ii)

x=[];
y=[];

mag1=1.0
for ii in range(len(lons1)):
	if mags1[ii] >= mag1:
		x.append(lons1[ii])
		y.append(lats1[ii])

for ii in range(len(lons1)):
	if rmss1[ii] <= 0.2:
		x.append(lons1[ii])
		y.append(lats1[ii])

# if if3month == True:
# 	nmonths=[12, 6, 1, 3]
# else:
# 	nmonths=[12, 6, 3, 1]
nmonths=[1]

for nmonth in nmonths:
    #Midland: -102.0779,31.9973
    xM=-102.0779
    yM=31.9973
    #Odessa: 
    # xO=-102.3676
    # yO=31.8457
    #Pecos:
    xP=-103.4932;
    yP=31.4229;
    #Van Horn
    xV=-104.8308
    yV=31.0399
    #Orla
    xO_Orla=-103.9085
    yO_Orla=31.8248
    
    f=open(fname)
    lines=f.readlines()
    lines=lines[1:-8]
    lats=[float(ii.split()[8]) for ii in lines]
    lons=[float(ii.split()[9]) for ii in lines]
    deps=[float(ii.split()[-1]) for ii in lines]
    eid0=[ii.split()[0] for ii in lines]
    flags=[ii.split()[3] for ii in lines]
    utcs=[utc.UTCDateTime(ii.split('  ')[1]) for ii in lines]
    
    if nmonth == 12:
        t1=utc.UTCDateTime(2021, 12, 1, 00, 00, 00, 000000)
        t2=utc.UTCDateTime(2022, 12, 1, 00, 00, 00, 000000)
    if nmonth == 1:
        t1=utc.UTCDateTime(2022, 11, 1, 00, 00, 00, 000000)
        t2=utc.UTCDateTime(2022, 12, 1, 00, 00, 00, 000000)  
    if nmonth == 6:
        t1=utc.UTCDateTime(2022, 6,  1, 00, 00, 00, 000000)
        t2=utc.UTCDateTime(2022, 12, 1, 00, 00, 00, 000000)   
    if nmonth == 3:
        t1=utc.UTCDateTime(2022, 8,  1, 00, 00, 00, 000000)
        t2=utc.UTCDateTime(2022, 11, 1, 00, 00, 00, 000000) 
        
    lon1=-104.7
    lon2=-103.7
    
    lat1=31.3
    lat2=31.9
    
    eids=[]
    lines3=[]
    for ii in range(len(lines)):
        if utcs[ii]>=t1 and utcs[ii]<=t2 and lons[ii]>=lon1 and lons[ii]<=lon2 and lats[ii]>=lat1 and lats[ii]<=lat2:
            eids.append(eid0[ii])
            lines3.append(lines[ii])
    print('Number of Reported events in AOI is',len(eids))
    
    ### plot Reported events
    lats3=[float(ii.split()[8]) for ii in lines3]
    lons3=[float(ii.split()[9]) for ii in lines3]
    deps3=[float(ii.split()[-1]) for ii in lines3]
    mags3=[float(ii.split()[7]) for ii in lines3]
    utcs3=[utc.UTCDateTime(ii.split('  ')[1]) for ii in lines3]
    
    eids=[]
    lines2=[]
    for ii in range(len(lines)):
        if utcs[ii]>=t1 and utcs[ii]<=t2 and lons[ii]>=lon1 and lons[ii]<=lon2 and lats[ii]>=lat1 and lats[ii]<=lat2 and (flags[ii] != 'REPORTED'):
            eids.append(eid0[ii])
            lines2.append(lines[ii])
    print('Number of Catalog events in AOI is',len(eids))
    create_catalog(eids,fincatalog='../data/texnet_events_20221220.csv',foutcatalog='texnet_events_tmp.csv');
    
    ### plot Catalog events
    f=open('texnet_events_tmp.csv')
    lines=f.readlines()
    lines=lines[1:]
    lats2=[float(ii.split(',')[6]) for ii in lines]
    lons2=[float(ii.split(',')[8]) for ii in lines]
    deps2=[float(ii.split(',')[10]) for ii in lines]
    mags2=[float(ii.split(',')[4]) for ii in lines]
    rmss2=[float(ii.split(',')[13]) for ii in lines]
    utcs2=[utc.UTCDateTime(ii.split(',')[2]+'T'+ii.split(',')[3]) for ii in lines]
        
    #%% compute the density of EQCCT events
    elon_p=x
    elat_p=y
    
    gridsize=0.025
    lons=np.arange(np.floor(min(elon_p)),np.ceil(max(elon_p)),gridsize)
    lats=np.arange(np.floor(min(elat_p)),np.ceil(max(elat_p)),gridsize)
    
    [LON,LAT]=np.meshgrid(lons,lats)
    V=np.nan*np.ones_like(LON)
    S=np.nan*np.ones_like(LON)
    index_hv=[]
    radii=gridsize*.5
    

#Midland: -102.0779,31.9973
xM=-102.0779
yM=31.9973


#Odessa: 
xO=-102.3676
yO=31.8457
#%% Plot Figure 10
#AOI
lon1=-104.7
lon2=-103.7

lat1=31.5
lat2=31.9


if if3month == True:
	period='Three months'
else:
	period='One month'

fig=plt.figure(figsize=(14,10))   
ax2=fig.add_subplot(221)
print("mags1:",len(mags1),"mags2",len(mags2),"mags3",len(mags2))
plt.hist(mags1,30,range=(np.min(mags1),np.max(mags2)),label='EQCCT',color='gray',edgecolor='black',alpha=0.5,log=True)
plt.hist(mags3,30,range=(np.min(mags1),np.max(mags2)),label='Reported',color='yellow',edgecolor='black',alpha=0.5,log=True)
plt.hist(mags2,30,range=(np.min(mags1),np.max(mags2)),label='TexNet',color='red',edgecolor='black',alpha=0.5,log=True)
plt.gca().set_xlim(xmin=0,xmax=5.6);
plt.gca().legend(loc='upper right');
plt.gca().set_ylabel("Count",fontsize='large', fontweight='normal')
plt.gca().set_xlabel("Magnitude (Ml)",fontsize='large', fontweight='normal')
ax2.text(-0.15,1,'(a)',transform=ax2.transAxes,size=20,weight='normal')

utcs1=[float(ii) for ii in utcs1]
utcs2=[float(ii) for ii in utcs2]
utcs3=[float(ii) for ii in utcs3]

ax4=fig.add_subplot(222)
print("utcs1:",len(utcs1),"utcs2",len(utcs2))
plt.hist(utcs1,31,range=(np.min(utcs1),np.max(utcs1)),label='EQCCT',color='gray',edgecolor='black',alpha=0.5,log=True)
plt.hist(utcs3,31,range=(np.min(utcs1),np.max(utcs1)),label='Reported',color='yellow',edgecolor='black',alpha=0.5,log=True)
plt.hist(utcs2,31,range=(np.min(utcs1),np.max(utcs1)),label='TexNet',color='red',edgecolor='black',alpha=0.5,log=True)
# plt.gca().set_xlim(xmin=0,xmax=30);
plt.gca().legend(loc='upper right');
plt.gca().set_ylabel("Number of earthquakes per day",fontsize='large', fontweight='normal')
plt.gca().set_xlabel("Date",fontsize='large', fontweight='normal')

# plt.gca().set_xlabel("Time",fontsize='large', fontweight='normal')
plt.gca().set_xlim(xmin=min(utcs1),xmax=max(utcs1))

x1,x2=plt.gca().get_xlim()
if if3month == True:
	plt.xticks([x1, (x1+x2)/2, x2], ['Aug 1 2022', 'Sep 16 2022', 'Oct 31 2022'])
else:
	plt.xticks([x1, (x1+x2)/2, x2], ['Nov 1 2022', 'Nov 16 2022', 'Nov 30 2022'])
ax4.text(-0.15,1,'(b)',transform=ax4.transAxes,size=20,weight='normal')

ax4=fig.add_subplot(212)
utcs2=[float(ii) for ii in utcs2]
plt.scatter(utcs1,mags1,s=mags1,facecolor='gray',edgecolor='gray',alpha=0.9,label='EQCCT')#c=
plt.scatter(utcs3,mags3,s=mags3,facecolor='yellow',edgecolor='yellow',alpha=0.9,label='Reported')#c=
plt.scatter(utcs2,mags2,s=mags2,facecolor='red',edgecolor='red',alpha=0.9,label='TexNet')#c=
plt.gca().legend(loc='upper right');
plt.gca().set_ylabel("Magnitude (Ml)",fontsize='large', fontweight='normal')
plt.gca().set_xlim(xmin=min(utcs1),xmax=max(utcs1))
plt.xticks([x1, (x1+x2)/2, x2], ['Nov 1 2022', 'Nov 16 2022', 'Nov 30 2022'])
plt.gca().set_xlabel("Date",fontsize='large', fontweight='normal')

ax4.text(-0.05,1,'(c)',transform=ax4.transAxes,size=20,weight='normal')


plt.savefig('test_eqcct_eventdistribution_202211.png',format='png',dpi=300,bbox_inches='tight')
plt.show()

