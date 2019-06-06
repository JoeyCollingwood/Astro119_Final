#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 22:19:17 2019

@author: lukewaldschmidt
"""

import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

file_in = 'data/hygdata_v3.csv'
mData = np.genfromtxt(file_in, delimiter = ',',skip_header = 1, usecols=[6,9,12,14,16,17,18,19,33]
                      ).T
name   = mData[0]
dist   = mData[1]
radvel = mData[2]
absmag = mData[3]
color  = mData[4]
xpos   = mData[5]
ypos   = mData[6]
zpos   = mData[7]
lumin  = mData[8]

t_sun = 5800


def temp(color):
    return 4600 * ((1/((.92*color)+1.7))+(1/((.92*color)+0.62)))

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

a_x = np.log10(temp(color)/t_sun)
a_y = np.log10(lumin) 
xmin = -1
xmax = 1  
slope, f_a = lin_LS( np.log10(temp(color)), np.log10(lumin) )
# extent fitting range by half order mag on both sides
aX_fit = np.linspace( xmin*.5, xmax*5, 100)
aPLfit = 10**(f_a)*aX_fit**slope
print(slope)


#==============================================================
#                  plotting
#==============================================================

plt.figure(1)
ax1 = plt.subplot(211)
ax2 = plt.subplot(212)
ax1.scatter(a_x,a_y,s=.05,c = 'b')
plt.gca().invert_xaxis()
#ax2.loglog(temp(color),lumin)
ax2.loglog(aX_fit,aPLfit,c = 'r')
plt.show()
