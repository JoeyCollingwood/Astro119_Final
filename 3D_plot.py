# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 15:37:18 2019
@author: Joey
"""

#=================modules/packages===============================

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#==================reading in data file==========================
file_in = 'hygdata_v3.csv'
df = pd.read_csv(file_in)
mData = np.genfromtxt(file_in, dtype=None, delimiter = ',',skip_header = 1, usecols=[9,12,16,17,18,19,33]
                      ).T

#====================filling in missing values=====================
df['ci'].fillna(method='backfill', inplace=True)
#print(df.isnull().sum()['ci'])

ci = df[['ci']].values  #using pandas to replace NaN values in ci column, then replacing them with backfilled values
dist   = mData[0]
radvel = mData[1]
color  = mData[2]
x_pos = mData[3]
y_pos = mData[4]
z_pos = mData[5]
lumin  = mData[6]


#====================calculating temp/radius========================
t_sun = 5800
l_sun = 3.85 * 10**26
temp    = []
radius  = []
lum_new = []
for i in range (len(ci)):
    
    t = 4600*((1/(.92*ci[i]+1.7))+1/(.92*ci[i]+.62))
    r = np.sqrt(((lumin[i]) * (l_sun)) /(4*np.pi*(5.67*(10**(-27))*t**4)))
    temp.append(t/t_sun)
    radius.append(r)
    lum_new.append(lumin[i])


#==============================3D PLOTTING=====================================
fig = plt.figure(1,figsize=[8,8])
ax = fig.add_subplot(111,projection='3d')
plot = ax.scatter(x_pos[0::10],y_pos[0::10],z_pos[0::10],c=np.reshape(ci,119614)[0::10],s=4,cmap='RdYlBu',vmin=0,vmax=1.5)
cbar = plt.colorbar(plot, orientation = 'horizontal')
cbar.set_label("Color Index (B-V)")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.title('3D position')
plt.show()
