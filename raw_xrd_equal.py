
from glob import iglob
import pickle
import numpy as np
import os
from scipy.optimize import minimize
import time
from copy import deepcopy
########################


########## Scale and broaden
#
def broaden(xrd,sigma=0.5,scale=1.):
    """
    function that scales and returns gaussian broadened 
    and normalized (integral=1) XRD pattern
    """

    xrd = deepcopy(xrd)

    two_theta_range=(0, 90.)

    for ii in range(len(xrd)):
        xrd[ii][0] = 2*np.arcsin(np.sin(0.5*xrd[ii][0]/180*np.pi)/scale)/np.pi*180


    # just a gaussian
    def gauss(x,x0,sigma):
        return 1./np.sqrt(2*np.pi*sigma**2) * np.e**( - (x-x0)**2/(2*sigma**2)   )
    
    # grid on the 2theta axis
    delta = sigma/float(10)
    angles = np.arange(two_theta_range[0], two_theta_range[1]+delta, delta)
        
    # placing a gaussian on every XRD peak
    data = np.zeros(len(angles))
        
    for xd in xrd:
        data = data + float(xd[1])*gauss(angles,xd[0],sigma)

    data = data/np.sum(data)/delta

    return np.array([[angles[ii],data[ii]] for ii in range(len(angles))])

########## Distance metric between two broadened xrd patterns
def distance(brd1,brd2):
    """
    Distance function between the two broadened xrd patterns
    """

    step=brd1[1,0]-brd1[0,0]
    return np.sum(np.abs(brd1[:,1]-brd2[:,1]))*step


##
def minimize_xrd_diff(key1,key2):

    xrd1=pickle.load(open(key1+'/raw_xrd.p','rb'))
    xrd1=[xx for xx in xrd1 if xx[1]>=0.05 and xx[0]<=90.]

    xrd2=pickle.load(open(key2+'/raw_xrd.p','rb'))
    xrd2=[xx for xx in xrd2 if xx[1]>=0.05 and xx[0]<=90.]

    brd1=broaden(xrd1,sigma=0.5,scale=1.)

    def opt_xrds(scale):
        brd2 = broaden(xrd2,sigma=0.5,scale=scale[0])
        return distance(brd1,brd2)

    x0=[1.]

    res = minimize(opt_xrds, x0, bounds=[(0.7071067811865475, None)])

    return res.x,opt_xrds(res.x)
########################################
