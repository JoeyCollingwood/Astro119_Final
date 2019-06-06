#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 22:19:17 2019

@author: lukewaldschmidt
"""

import numpy as np
import matplotlib.pyplot as plt

file_in = 'data/hygdata_v3.csv'
mData = np.genfromtxt(file_in, delimiter = ',',skip_header = 1, usecols=[6,9,12,14,16,17,18,19,33]
                      )
name   = mData[0]
dist   = mData[1]
radvel = mData[2]
absmag = mData[3]
color  = mData[4]
xpos   = mData[5]
ypos   = mData[6]
zpos   = mData[7]
lumin  = mData[8]

#==============================================================
#                  plotting
#==============================================================

plt.figure(1)
ax = plt.subplot(111)
ax.scatter(color,absmag)
plt.show()