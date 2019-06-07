# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 15:37:18 2019

@author: Joey
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#from mpl_toolkits import mplot3d
#from mpl_toolkits.mplot3d import Axes3D

file_in = 'hygdata_v3.csv'
df = pd.read_csv(file_in)
mData = np.genfromtxt(file_in, dtype=None, delimiter = ',',skip_header = 1, usecols=[9,12,16,17,18,19,33]
                      ).T

median = df['ci'].median()
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

#def temp(ci):
#    return 4600 * ((1/((.92*ci)+1.7))+(1/((.92*ci)+0.62)))
#def radius(lumin):
#    return np.sqrt(((lumin) * (l_sun)) /(4*np.pi*(5.67*(10**(-27))*temp(ci)**4)))

def lin_LS( aX, aY):
    """
    - linear least squares assuming normal distributed errors in Y, no errors in X
    :param aX: - independent variable
    :param aY: - measured dependent variable
    :return: float(<slope>)
    """
    meanX = aX.mean()
    meanY = aY.mean()
    # variance and co-variance - 1./N term omitted because it cancels in the following ratio
    VarX  = ( (aX - meanX)**2).sum()
    #VarY  = ( (aY - meanY)**2).sum()
    CovXY = ( (aY-meanY)*(aX-meanX)).sum()
    slope = CovXY/VarX
    a     = meanY - meanX*slope
    return slope, a


log_lum  = np.log10(lumin)            #log luminosity in solar units
log_temp = np.log10(temp)   #log temperature in solar units

slope,f_a = lin_LS(log_lum[0:1000],log_temp[0:1000])
#R_fit = np.linspace(np.median(radius)-1e10,np.median(radius)+1e10,100)
aPLfit = 10**(f_a)*temp[::]**slope
print(slope)
#print(aPLfit)

def func(r, alpha, t, beta):
    return (r**alpha)*t**beta

#fig1 = plt.figure(1)
#plt.scatter(log_temp,log_lum,s=.05,c = 'black')
#plt.gca().invert_xaxis()
#plt.title('Hertzsprung-Russell Diagram')
#plt.xlabel('Temperature')
#plt.ylabel('Luminosity')
#plt.grid(True, linestyle = 'dotted', c = 'black')
#fig2 = plt.figure(2)
#plt.loglog(temp,aPLfit,c = 'r')

#==============================3D PLOTTING=====================================
fig2 = plt.figure(2)
ax = fig2.add_subplot(111,projection='3d')
ax.scatter3D(x_pos,y_pos,z_pos,c=color,s=np.exp(color))
cbar = plt.colorbar(ax, orientation = 'horizontal')
cbar.set_label("Color Index")
#c = ax.colorbar(ax, orientation = 'horizontal')
#c.set_label('Color Index')
