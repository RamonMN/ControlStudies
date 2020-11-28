"""
author: Ramon Machado
"""

import control
import numpy as np
import matplotlib.pyplot as plt

"""
A first order system can be described as C(s)/R(s) = 1/(Ts + 1), where C(s) is the output
and R(s) is the input of our system. 
To be able to analyse the how our system responds to some kinds of inputs, we can place our
desired R(s) and then do the inverse Laplace transform.
1) Impulse response: C(s) = 1/(Ts + 1) = (1/T) / (s + (1/T)) -> inverse laplace -> c(t) = 1/T * exp(-t/T)

2) Step response: C(s) = 1/(Ts + 1) * 1/s -> parcial fractions -> C(s) = 1/s - 1/(s + (1/T))
        -> inverse laplace -> c(t) = 1 - exp(-t/T)
3) Ramp response: C(s) = 1/(Ts+2) * 1/s² -> partial fractions -> C(s) = 1/s² - T/s + T²/(Ts+1)
        -> inverse laplace -> c(t) = t - T + Texp(-t/T)

"""
s = control.tf('s')

# Creating a list of time constants to analyse its change
time_constants = []
for i in range(0, 20, 5):
    time_constants.append(i)
time_constants[0] = 1

# Simulation time and sampling time
simulation_time = np.arange(0., 4*time_constants[-1], 0.1)

# Creating the axes 
fig, axs = plt.subplots(3, figsize = (12,8))

#------------------------ IMPULSE --------------------------#
# Plotting the input
axs[0].axvline(0, ymin=0.04, ymax=0.96, color='k', ls='--', label='Input')
axs[0].plot(0,1,'ko')

# Creating the transfer function and then plotting the impulse response
for T in time_constants:
    G = 1./((T*s) + 1)
    t, y = control.impulse_response(G, T=simulation_time)
    axs[0].plot(t, y, label='T = {}s'.format(T))

# Setting the graph's labels and title
axs[0].set_title('Impulse Response for a First Order System')
axs[0].set_xlabel('t(s)')
axs[0].set_ylabel('Amplitude')
axs[0].legend()

#------------------------ STEP --------------------------#
# Plotting the input
u = 0*simulation_time
u[:] = 1
axs[1].plot(simulation_time, u, 'k--', label='Input')
axs[1].axvline(0, ymin=0.04 ,ymax=0.96, color='k', ls='--')

# Creating the transfer function and then plotting the step response
for T in time_constants:
    G = 1./((T*s) + 1)  # First order transfer function
    t, y = control.step_response(G, T=simulation_time)   # Step response
    axs[1].plot(t, y, label='T = {}s'.format(T))   # Plotting the results for each T
    #plt.annotate('98,2%', xy=(4*T, 0.982), xytext=(4*T-3.5, 0.5), arrowprops=dict(arrowstyle='->'))

# Setting the graph's labels and title
axs[1].set_title('Step Response for a First Order System')
axs[1].set_xlabel('t(s)')
axs[1].set_ylabel('Amplitude')
axs[1].legend()

#------------------------ RAMP --------------------------#
# Plotting the input
axs[2].plot(simulation_time, simulation_time, 'k--', label='Input')

# Creating the transfer function and then plotting the ramp response
for T in time_constants:
    G = 1./((T*s**2) + s)
    t, y = control.step_response(G, T=simulation_time)
    axs[2].plot(t, y, label='T = {}s'.format(T))

# Setting the graph's labels and title
axs[2].set_title('Ramp Response for a First Order System')
axs[2].set_xlabel('t(s)')
axs[2].set_ylabel('Amplitude')
axs[2].legend()


# Show the plots
plt.tight_layout()
plt.show()
