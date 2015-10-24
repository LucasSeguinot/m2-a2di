#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy

def phi(n, x):
    return x**n

def phi_str(n, a):
    if n == 0:
        return "{:.2f}".format(a)
    elif n == 1:
        if a < 0:
            return " - {:.2f} x".format(-a)
        else:
            return " + {:.2f} x".format(a)
    else:
        if a < 0:
            return " - {:.2f} x^{{{}}}".format(-a, n)
        else:
            return " + {:.2f} x^{{{}}}".format(a, n)

def f(theta, x=None):
    f = lambda x: (numpy.matrix([phi(d, x) for d in range(0, theta.shape[0])]) * theta)[0,0]
    if x == None:
        return f
    else:
        return f(x)

def f_str(theta):
    return "".join([phi_str(k, t[0,0]) for k, t in enumerate(theta)])
