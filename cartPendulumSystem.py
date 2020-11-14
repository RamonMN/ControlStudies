#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 10:00:22 2020
@author: ramon

This script intend to implement the example 3.9 from Ogata's 4th edition, wich 
is the modelling of a inverted pendulum on a cart.

First of all, we need to build a free body diagram of the elements of our
system, in this case, a cart and a bar representing the pendulum.

We will call 'M' the mass of the cart, 'm' the mass of the bar, 'I' the moment of 
inertia with respect to the bar's center of mass, 'g' the gravity, 'L' half of
the bar's length, 'u' the input force applied to the cart, 'theta' the that the 
bar makes with the vertical axis, 'x' the distance the cart is far from the origin
in the horizontal axis, and let 'V' and 'H' be the internal forces between the
bar and the cart, respectively the vertical and the horizontal one.

We can apply the Newton's Second Law for rotations to the bar's center of mass
and then we'll have: 
            I(theta)'' = Vsin(theta)L - Hcos(theta)L
And for translations, to the X and Y axes of the bar and to the X axis of the cart,
 as it follows:
            m(x+Lsin(theta))'' = H
            m(Lcos(theta))'' = V - mg => V = mg
            M(x)'' = u - H
At this point, we can make some assumptions to linearize the problem, using
the first term of the Taylor's expansion, we can assume that for a small value
of theta(where we need the pendulum to stay) and theta':
            theta ~ 0, theta' ~ 0
            sin(theta) ~ theta
            cos(theta) ~ 1
Other than that, if we assume that the pendulum is actually a body of mass at
the center of gravity and the mass of the bar that holds this body isn't, relatively
large:
            I = 0
Thus, we can write down the system equations by removing the internal forces and
resolving for theta'' and x'':
            ML(theta)'' = (M+m)g(theta) - u
            Mx'' = u - mg(theta)
Also, we can represent this system in the State Space as:
            x = [theta, theta', x, x'], y = [theta, x]
        
                 _                                  _       _       _
            x' =|  0             1      0       0    |     |   0     |
                |  (M+m/ML)g     0      0       0    |x  + |   -1/ML |u
                |  0             0      0       1    |     |   0     |
                |_ -(m/M)g       0      0       0   _|     |_  1/M  _|
             
            [y1] = [1 0 0 0] x
            [y2]   [0 0 1 0]
"""
import control
import numpy as np
import matplotlib.pyplot as plt

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

# Transfer function (Theta/U) 
num = [1]
den = [-M*L, 0., (M+m)*g]

# State Space represantation
ssSys = control.ss(A,B,C,D)
# Transfer function representation
tfSys = control.tf(num,den)



# There are two basic ways to check wheter our system is stable or not.
# First, checking the poles of our transfer function, if there is at least
# one positive pole, then the system is unstable under these conditions:
print("Transfer function poles = {}".format(control.pole(tfSys))) 
# As we can see, there is a positive pole: p =1.038

# Second, we can check the eigenvalues of the matrix A of the State Space representation
# and for stability we need to have all the eigenvalues real parts less then 0:
print("SS representation eigenvalues = {}".format(np.linalg.eig(A)[0])) 
# As we can see, there is an eigenvalue equals to 10.38

# So, now that we know the system isn't stable under these open loop conditions, 
# we need to check wheter it is controllable or not, and to do so we'll compute the
# controllability matrix and check if it has rank equals to its size.
print("Rank of the controllability matrix = {}".format(np.linalg.matrix_rank(control.ctrb(A,B))))
# As we can see, the system is controllable, and the next steps will be implement
# the controller to make our system stable.







