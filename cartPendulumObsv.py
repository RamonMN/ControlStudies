#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 01:15:13 2020

@author: ramon

In the last script (cartPendulumPlacement.py) we have considered that the output
of the system was a full-state representation. However, it is not always possible
to have all of our states measured, and thus we need to know if there is a way
to determine the full-state representation of the system with the states that
we have as outputs.

First of all, we will calculate the observability matrix, which represents if a
system is observable given the outputs it has. With observable we mean that this
system is capable of estimate his own full-state representation.


x = [theta, theta', x, x']
"""

import control
import numpy as np


# System variables
M = 1000.0  #Kg
m = 100.0   #Kg
g = 9.8     #m/s^2
L = 10.0    #m

# State space matrix representation
A = [[0.,            1.,  0.,  0.],
     [(M+m)*g/M*L,   0.,  0.,  0.],
     [0.,            0.,  0.,  1.],
     [-(m+M)*g,      0.,  0.,  0.]]

B = [[0.],
     [-1./M*L],
     [0.],
     [1./M]]

C = [[1., 0., 0., 0.],
     [0., 0., 1., 0.]]

D = 0.

# In this case, by looking at C, the output of the system (y=Cx) is the measure
# of theta and x. So, we will see if this is an observable system.
O = control.obsv(A,C)
# If rank(O) = n = 4, then the system is observable.
print(np.linalg.matrix_rank(O))
