#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 23:22:13 2020

@author: ramon

Now that we have our system model and we know that the system is unstable under
those conditions, is possible to build a controller since it is controllable.

First of all, we will feedback our output signal y through a gain of -K.So if we
consider that we have all the states being outputed by the system (y = x), then the
input will be equal to u = -Ky = -Kx, and since x' = Ax + Bu => x' = (A - BK)x 
Therefore, we can make our system stable by selecting a proper K that the
eigenvalues of (A-BK) are in the left half plane. Below will be shown two methods
of doing so.

x = [theta, theta', x, x']
"""

import control
import numpy as np
import matplotlib.pyplot as plt 

# Description of our system

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


# The first method is using the function place, that allows you to simply choose
# the eigenvalues that you want and will return the K that makes A-B*K have those.
K = control.place(A,B,[-1., -1.1, -1.2, -1.3])
print(np.linalg.eigvals(A-B*K))
# Howhever this method makes possible to give stability to the system, it isn't 
# the best way, since we have to choose for ourselves by trial and error which
# eigenvalus makes a good stable system and which eigenvalues doesn't make good a 
# stable system.

# That leads us to the second method of finding a K, which is the Linear Quadratic
# Regulator. The LQR is a method to find the optimal value to K, given two parameters
# Q and R. The parameter Q is a matrix that defines the weights on the states and
# R is a matrix that defines the weights on the control input.
# For example, let Q = [[100],[10],[1],[1]] and R = [0.01]
Q = [[100., 0., 0., 0.],[0., 10., 0., 0.],[0., 0., 1., 0.],[0., 0., 0., 1.]]
R = [0.001]
K, S, E = control.lqr(A, B, Q, R)
# Where K will be the matrix we want to control the system and E will be the 
# eigenvalues of (A-B*K)
print(K)
print(E)
# As we can see, since we put a heavier weight on theta, the eigenvalue that 
# represent the theta is the most aggressive.

