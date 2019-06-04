# -*- coding: utf-8 -*-
"""
Final project question 3(b)
Group members: Joey C & Luke W
"""

import os
import matplotlib.pyplot as plt
import numpy as np

data_dir = 'C:\\Users\\Joey\\Desktop\\aapython\\Final'
star_data = 'hygdata_v3.csv'

#===========================LOAD DATA================================
os.chdir(data_dir)
stars = np.loadtxt(star_data).T

#===========================PLOTTING=================================
plt.figure(1)
ax = plt.subplot(111)
