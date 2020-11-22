import control
import numpy as np

# Variables
m = 1
M = 5
L = 2
g = -10
d = 1

# System representation
A = np.array([[0, 1, 0, 0],
             [0, -d/M, -m*g/M, 0],
             [0, 0, 0, 1],
             [0, d/(M*L), (m+M)*g/(M*L), 0]])

B = np.array([[0],
              [1/M],
              [0],
              [-1/(M*L)]])

C = np.array([[1, 0, 0, 0]])


D = np.zeros((np.size(C,0), np.size(B,1)))  # D has the same numbers of rows as C, and columns as B

# Disturbance and noise covariances
Vd = 0.1*np.eye(4)
Vn = 1

# B matrix considering the new inputs (noise and disturbance)
BF = np.column_stack([B, Vd, 0*B])

sys_single_state = control.ss(A, BF, C, [0, 0, 0, 0, 0, Vn])

sys_full_state = control.ss(A, BF, np.eye(4), np.zeros((4,np.size(BF,1))))

[Kf, P, E] = control.lqe(A, Vd, C, Vd, Vn)

sys_kf = control.ss(A - Kf*C, np.column_stack([B, Kf]), np.eye(4), 0*(np.column_stack([B, Kf])))






