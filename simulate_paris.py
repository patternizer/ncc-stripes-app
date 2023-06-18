#! /usr/bin python

#------------------------------------------------------------------------------
# PROGRAM: simulate_paris.py
#------------------------------------------------------------------------------
# Version 0.1
# 17 June, 2023
# Michael Taylor
# https://patternizer.github.io
# michael DOT a DOT taylor AT uea DOT ac DOT uk
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# IMPORT PYTHON LIBRARIES
#------------------------------------------------------------------------------

import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------
# METHODS
#------------------------------------------------------------------------------

def set_threshold(x,y,threshold):
    xv=[]
    yv=[]
    for i in range(len(y)-1):
    	xv += [x[i]]
    	yv += [y[i]]
    	if y[i] > threshold > y[i+1] or y[i] < threshold < y[i+1]:
    		Xi = x[i] + ((threshold-y[i])*(x[i+1]-x[i]) / (y[i+1]-y[i]))
    		xv += [Xi]
    		yv += [threshold]
    xv += [x[-1]]
    yv += [y[-1]]
    
    xv = np.array(xv)
    yv = np.array(yv)

    return xv,yv

#------------------------------------------------------------------------------
# GENERATE: noisy Sine (4 cycles, minmax=5, noise=Gaussian)
#------------------------------------------------------------------------------

x = np.linspace(0, 8*np.pi, 100)
y = 5*np.sin(x) + 5*(np.random.rand(100)-0.5)

#------------------------------------------------------------------------------
# PLOT
#------------------------------------------------------------------------------

fig,ax = plt.subplots()
plt.plot(x,y,'k')

# FILL: betweeen "Paris" thresholds 1.5 and 2.0 and also below 0
    
for threshold in [0,1.5,2]:
        
    X,Y = set_threshold(x,y,threshold)
    mask_above = Y >= threshold
    mask_below = Y <= threshold
    plt.fill_between(X[mask_above],Y[mask_above],y2=threshold)

    if threshold == 0.0:
        plt.fill_between(X[mask_below],Y[mask_below],y2=0)

plt.savefig('thresholds.png', dpi=300, bbox_inches='tight')

#------------------------------------------------------------------------------
print('** END')
