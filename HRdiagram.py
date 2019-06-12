#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 13:18:52 2019

@author: lukewaldschmidt
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
#from mpl_toolkits.mplot3d import Axes3D

#================================reading in the data================================
file_in = 'hygdata_v3.csv'
df = pd.read_csv(file_in)
mData = np.genfromtxt(file_in, dtype=None, delimiter = ',',skip_header = 1, usecols=[9,12,16,33]
                      ).T
#===================filling in missing values======================================
median = df['ci'].median()
df['ci'].fillna(method='backfill', inplace=True)
#print(df.isnull().sum()['ci'])

ci = df[['ci']].values  #using pandas to replace NaN values in ci column, then replacing them with backfilled values
dist   = mData[0]
radvel = mData[1]
#ci  = mData[2]
lumin  = mData[3]

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

#===========================HR DIAGRAM=======================================================
fig = plt.figure(figsize=(10,10))
ax = plt.subplot(111)
ax.scatter(np.log10(temp),np.log10(lum_new),s=.07,c = 'k')
ax.set_xlabel('Temperature (Solar Units)')
ax.set_ylabel('Luminosity (Solar Units)')
plt.gca().invert_xaxis()
rect = patches.Rectangle((-.05,-4.5),.3,1.5,linewidth=2,edgecolor='b',facecolor='none',label='white dwarfs')
rect2 = patches.Rectangle((-0.25,5.3),.6,1.9,linewidth=2,edgecolor='r',facecolor='none',label='supergiants')
rect3 = patches.Rectangle((-0.25,.4),.25,2.2,linewidth=2,edgecolor='g',facecolor='none',label='giants')
ax.add_patch(rect)
ax.add_patch(rect2)
ax.add_patch(rect3)
ax.scatter(0,0,s=3,c='orange')
ax.annotate(
    'main sequence', xy=(0.3, 1), xycoords='data',
    fontsize='14', color='purple',
    xytext=(-40, -40), textcoords='offset points',
    arrowprops=dict(
        arrowstyle="->",
        connectionstyle="arc3,rad=-2.0",
        color='purple'))
ax.annotate(
    'Sol', xy=(.01, -.05), xycoords='data',
    fontsize='14', color='orange',
    xytext=(-40, -40), textcoords='offset points',
    arrowprops=dict(
        arrowstyle="->",
        connectionstyle="arc3,rad=0",
        color='orange'))
plt.legend()
ax.set_title('H-R diagram',fontsize=19)
plt.show()

