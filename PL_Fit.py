import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#Least squares method used to fit the data
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

#Reads the data file and replaces NaN values
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

#Initializes arrays to fill with limited data
temp_ms = np.ones(20000)
lum_ms = np.ones(20000)

#Limits the data to stars near the solar values
for i in range(len(temp_ms)):
    if np.log10(temp[i]) > -0.2 and np.log10(temp[i]) < 0.4:
        temp_ms[i] = temp[i]
    if np.log10(lum_new[i]) > -1 and np.log10(lum_new[i]) < 1:
        lum_ms[i] = lum_new[i]

#Determines the least sqaures fit for limited data
slope, f_a = lin_LS( temp_ms, lum_ms)
print('slope: ' + str(slope) + 'intercept: ' + str(f_a))
a_x = np.linspace(-0.6,0.6,10000)
y_Fit = slope*a_x + f_a

#Log-transformed data in solar units
log_lum  = np.log10(lumin)            
log_temp = np.log10(temp)

#Initializing a text box to display LS fit
props = dict(boxstyle='round',facecolor='grey',alpha=0.5)
txt = 'Y= ' + str(round(slope, 3)) + 'x + ' + str(round(f_a, 3))

#PLOTTING
fig1 = plt.figure(1)
plt.scatter(log_temp,log_lum,s=.05,c = 'black')
plt.plot(a_x, y_Fit, c = 'red')
plt.gca().invert_xaxis()
plt.title('HR Diagram Least Squares Fit')
plt.xlabel('Temperature')
plt.ylabel('Luminosity')
plt.text(-0.25,4.2,txt,bbox=props)
plt.grid(True, linestyle = 'dotted', c = 'black')
