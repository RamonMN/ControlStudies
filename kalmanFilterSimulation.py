import numpy as np
import control
import control.matlab as matlab
import matplotlib.pyplot as plt
import seaborn as sns

"""
This script will be based on the Steve Brunton's class about Kalman Filter,
at the Control Bootcamp. The system that we will be studing is the
pendulum on a cart, but for now, using the pendulum in the down position.
x = [x, x_dot, theta, theta_dot]
"""
# Declaring the variables
m = 1
M = 5
L = 2
g = -10

# System description
A = np.array([[0, 1, 0, 0],
              [0, -1/M, -m*g/M, 0],
              [0, 0, 0, 1],
              [0, 1/(M*L), ((m+M)*g)/(M*L), 0]])

B = np.array([[0],
              [1/M],
              [0],
              [-1/(M*L)]])

C = np.array([[1, 0, 0, 0]])    # Taking only x as a measurement

D = np.zeros((np.size(C,0), np.size(B,1)))  # D has the same numbers of rows as C, and columns as B

# Disturbance and noise covariances
Vd = 0.1*np.eye(4)  # Giving the same weight to all the states
Vn = 1

# Building a new B matrix, for the new input u = [u, d, n], where
# u is the input force, d is the system's disturbance and n is the sensor's noise
aug_B = np.column_stack([B, Vd, 0*B])

# Now, we are able to build 2 systems, one of than observing all of the states
# and another one observing only one state (x). This way we can compare each
# other afterwards

# Single measurement system
single_sys = control.ss(A, aug_B, C, [0, 0, 0, 0, 0, Vn])
# Full state measurement system, without noise
full_C = np.eye(4)
full_sys = control.ss(A, aug_B, full_C, np.zeros((np.size(full_C,0), np.size(aug_B,1))))

# Now we'll use the linear quadratic estimator command to design the Kalman Filter Gain 
# and build the system that corresponds to the full-state estimator
Kf, P, E = control.lqe(A, Vd, C, Vd, Vn)
kf_inputs = np.column_stack([B, Kf])
kf_sys = control.ss(A - Kf@C, kf_inputs, np.eye(4), 0*kf_inputs)

# In this part we are building an input signal, a disturbance signal and noise signal
# so we can see how the systems' response looks like
t = np.arange(0, 50, 0.01).round(decimals=2)

# Input force
u = 0*t
u[100:120] = 100
u[1500:1520] = -100

# Input disturbance
u_dist = np.random.randn(4, np.size(t))

# Input noise
u_noise = np.random.randn(np.size(t))

# The input taking all the parts
aug_u = np.row_stack([u, Vd@Vd@u_dist, u_noise])

# Calculating the outputs
y, t, ph = matlab.lsim(single_sys, aug_u.transpose(), t)
fs_x, t, ph = matlab.lsim(full_sys, aug_u.transpose(), t)
x_hat, t, ph = matlab.lsim(kf_sys, np.row_stack([u, y]).transpose(), t)

# Plotting the results
fig, axs = plt.subplots(2, figsize = (14, 8))
axs[0].plot(t, y, label='System output', linewidth = 0.8)
axs[0].plot(t, x_hat[:,0], 'r', label='Estimative of this variable', linewidth = 1.5)
axs[0].legend()
axs[0].set_xlabel('t (s)')
axs[0].set_ylabel('Amplitude')
axs[0].set_title('Noise and disturbance rejection')

axs[1].plot(t[1000:2000], fs_x[:,0][1000:2000], 'b', label='True Full-State Output', linewidth = 3)
axs[1].plot(t[1000:2000], fs_x[1000:2000], 'b', linewidth = 3)
axs[1].plot(t[1000:2000], x_hat[:,0][1000:2000], 'r--', label='Estimated')
axs[1].plot(t[1000:2000], x_hat[1000:2000], 'r--')
axs[1].legend()
axs[1].set_xlabel('t (s)')
axs[1].set_ylabel('Amplitude')
axs[1].set_title('True full-state output versus estimated ')

plt.tight_layout()
plt.show()