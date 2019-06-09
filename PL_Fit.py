#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 10:46:14 2019
@author: lukewaldschmidt
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#import scipy.stats



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


file_in = 'hygdata_v3.csv'
df = pd.read_csv(file_in)
mData = np.genfromtxt(file_in, dtype=None, delimiter = ',',skip_header = 1, usecols=[9,12,16,17,18,19,33]
                      ).T

median = df['ci'].median()
df['ci'].fillna(method='backfill', inplace=True)

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

temp_cond = [np.log10(temp)>-0.3,np.log10(temp)<4]
lum_cond  = [np.log10(lum_new)<3]

#temp_choice = [temp, temp]
#lum_choice  = [lum_new]

temp_ms = np.ones(10000)
lum_ms = np.ones(10000)
#temp_select = np.select(temp_cond,temp_ms)
#lum_select  = np.select(lum_cond,lum_new)

for i in range(len(temp_ms)):
    if np.log10(temp[i]) > -0.2 and np.log10(temp[i]) < 0.4:
        temp_ms[i] = temp[i]
    if np.log10(lum_new[i]) > -1 and np.log10(lum_new[i]) < 1:
        lum_ms[i] = lum_new[i]

#print(temp_ms)
#print(lum_ms)
slope, f_a = lin_LS( temp_ms, lum_ms)
print('slope: ' + str(slope) + 'intercept: ' + str(f_a))
a_x = np.linspace(-0.6,0.6,10000)
y_Fit = slope*a_x + f_a

# extent fitting range by half order mag on both sides
#aX_fit = np.linspace( -0.6, 0.6, 100)
#aPLfit = 10**(f_a)*aX_fit**slope

log_lum  = np.log10(lumin)            #log luminosity in solar units
log_temp = np.log10(temp)

fig1 = plt.figure(1)
plt.scatter(log_temp,log_lum,s=.05,c = 'black')
plt.plot(a_x, y_Fit, c = 'red')
plt.gca().invert_xaxis()
plt.title('Hertzsprung-Russell Diagram')
plt.xlabel('Temperature')
plt.ylabel('Luminosity')
plt.grid(True, linestyle = 'dotted', c = 'black')
