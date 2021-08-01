import math
import random as rand
import pdb

def triangle_response(s, t, tail=-0.7, width=1/3):
    x = t - s

    return max(1-abs(tail*x+1-x**width),0)

def abs_threshold(s, t, base_thresh, abs_refrac, rel_refrac):
    x = min(rel_refrac, t - s)
    if x < abs_refrac:
        return 999
    elif x < rel_refrac:
        return base_thresh * 10
    else:
        return base_thresh

def inv_exp_threshold(s, t, base_thresh, abs_refrac, rel_refrac, roof=0.1, slope=-10,):
    # rel_refrac marks the maximum interesting distance from the threshold
    x = min(rel_refrac, t - s)
    # calculate the exponent for the sigmoid
    exp = (abs_refrac-x)*slope
    # retun the position on the slope
    return (1 / (roof + math.exp(exp)) + base_thresh)

def abs_spike(potential, threshold):
    if potential > threshold:
        return True
    else:
        return False

def lin_rand_spike(potential, threshold):
    p = min(0, threshold-potential)
    s = rand.random()
    if s < 1-p:
        return True
    else:
        return False

def exp_rand_spike(potential, threshold, offset=-0.9, slope=50):
    # x is the proportion of the way that the potential is to the threshold (max 1)
    x = min(1, potential/threshold)
    exp = min(10, (-x-offset)*slope)
    p = 1 / (1 + math.exp(exp))
    s = rand.random()
    if s < p:
        return True
    else:
        return False
