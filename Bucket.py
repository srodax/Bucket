#!/usr/bin/env python3
import numpy as np
import fileinput
import scipy.stats as stats
import sys
import argparse

#***********************************************************************
# Parsing arguments
#***********************************************************************
parser = argparse.ArgumentParser(description='Bin data into specified range. If the input has more than 2 columns, the 1st one is treated as x and the remaining as different y values.')
parser.add_argument('min_x', type=float, nargs='?', help='Starting value of x.', default=-4.0)
parser.add_argument('max_x', type=float, nargs='?', help='Stop value of x.', default=8.0)
parser.add_argument('step_x', type=float, nargs='?', help='Increment of x.', default=0.02)
parser.add_argument('files', type=str, nargs='*', help='Files with data to be binned.')
args = parser.parse_args()
#***********************************************************************
# reading data as argument or std input
data = np.loadtxt(fileinput.input(args.files), dtype=float)
#***********************************************************************

# preparing the bins
bin_x = np.linspace( args.min_x, args.max_x, int(abs(args.max_x - args.min_x)/args.step_x) )

# binning with scipy
datanew=[]
# getting bin centers as new x values, which we keep as first column of our data
datanew.append((bin_x[1:] + bin_x[:-1])/2)

for i in range(1,len(data[0,:])):
    ret = stats.binned_statistic(data[:,0], data[:,i], 'mean', bins=[bin_x])

    # preparing new yvalues, with 0s in empty bins
    datanew.append(ret.statistic)
    datanew[i][np.isnan(datanew[i])] = 0.0

# printing the result to std out
np.savetxt(sys.stdout, np.stack(datanew,axis=1), newline='\n')

