#!/usr/bin/env python3
import numpy as np
import fileinput
import scipy.stats as stats
import sys
import argparse

#***********************************************************************
# Parsing arguments
#***********************************************************************
parser = argparse.ArgumentParser(description='Bin data into specified range.')
parser.add_argument('min_x', type=float, nargs='?', help='Starting value of x.', default=-4.0)
parser.add_argument('max_x', type=float, nargs='?', help='Stop value of x.', default=8.0)
parser.add_argument('step_x', type=float, nargs='?', help='Increment of x.', default=0.02)
parser.add_argument('files', type=str, nargs='*', help='Files with data to be binned.')
args = parser.parse_args()
#***********************************************************************
# reading data as argument or std input
data = np.loadtxt(fileinput.input(args.files), dtype=np.float)
#***********************************************************************

# preparing the bins
bin_x = np.linspace( args.min_x, args.max_x, int(abs(args.max_x - args.min_x)/args.step_x) )

# binning with scipy
ret = stats.binned_statistic(data[:,0], data[:,1], 'mean', bins=[bin_x])

# preparing new yvalues, with 0s in empty bins
ynew = ret.statistic
ynew[np.isnan(ynew)] = 0.0

# getting bin centers as new x values
xnew = (bin_x[1:] + bin_x[:-1])/2

# printing the result to std out
np.savetxt(sys.stdout, np.c_[xnew, ynew], newline='\n')

