#to create lognorm distributions that will be used for run_bin
from numpy import *
import matplotlib.pyplot as plt
from math import erf

#create number concentration lognorm size distribution
def bins(num, sigmag, dpg, plot=False):
    num = num
    sigmag=sigmag
    dpg = dpg
    plot = plot
    #dps is very important to decide bins lower and upper bound
    #here we choose -4 to 3 to represent 10**-4 and 10**3 mu dp range
    dps = logspace(-4,3,num)
    lower = dps[:-1]
    upper = dps[1:]
    interval = [i for i in zip(lower,upper)]
    Ndp = [num/2. * (erf(log(dp[1]/dpg)/(sqrt(2)*log(sigmag))) - erf(log(dp[0]/dpg)/(sqrt(2)*log(sigmag)))) for dp in interval]
    wt = [i/num for i in Ndp]
    dpmedian = [median(interval[i]) for i in arange(0,len(interval))]

    if plot:
        plt.close()
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_axes([.15,.15,.75,.75])
        ax.plot(dpmedian,wt,marker='o')
        ax.set_xscale('log')
        plt.show()

    return [(dpmedian[i], wt[i]) for i in arange(0,len(interval))]

#create mass concentration lognorm size distribution
def mbins(num, sigmag, dpg, dens, plot=False):
    num = num
    sigmag=sigmag
    dpg = dpg
    dens = dens
    plot = plot
    dps = logspace(-4,3,num)
    lower = dps[:-1]
    upper = dps[1:]
    interval = [i for i in zip(lower,upper)]
    Ndp = [num/2. * (erf(log(dp[1]/dpg)/(sqrt(2)*log(sigmag))) - erf(log(dp[0]/dpg)/(sqrt(2)*log(sigmag)))) for dp in interval]
    dpmedian = [median(interval[i]) for i in arange(0,len(interval))]
    massmedian = [dpmedian[i] ** 3 * pi / 6 * dens * Ndp[i] for i in arange(0, len(Ndp))]
    totalmass = sum(massmedian)
    wt = [i/totalmass for i in massmedian]

    if plot:
        plt.close()
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_axes([.15,.15,.75,.75])
        ax.plot(dpmedian,wt, marker='o')
        ax.set_xscale('log')
        plt.show()

    return [(dpmedian[i], wt[i]) for i in arange(0,len(interval))]
