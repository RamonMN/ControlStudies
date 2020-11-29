"""
author: Ramon Machado
"""
import control
import numpy as np
import matplotlib.pyplot as plt
s = control.tf('s')
simulation_time = np.arange(0, 20, 0.1)
fig, axs = plt.subplots(2, figsize=(12,9))

"""
We'll be plotting 2nd Order System's step response with respect to 
the damping ratio and with the natural frequency to analyse the system's
behavior in both of the cases.
"""

# Varying zeta
zetas = np.linspace(0.0, 1.0, 6)
wn = 1.
u = 0*simulation_time
u[1:] = 1

axs[0].step(simulation_time, u, 'k--', label='Input')
for zeta in zetas:
    G = (wn**2)/(s**2 + 2*(zeta.round(2))*wn*s + wn**2)
    t,y = control.step_response(G, T=simulation_time)
    axs[0].plot(t,y, label=f'zeta = {zeta.round(2)}')

axs[0].set_title("Behavior of 2nd Order System's step response with respect to zeta (wn = 1rad/s)")
axs[0].set_xlabel('t(s)')
axs[0].set_ylabel('Amplitude')
axs[0].legend()

# Varying wn
zeta = 0.2
wns = [1, 1.5, 2.0, 2.5, 3.0] 

axs[1].step(simulation_time, u, 'k--', label='Input')
for wn in wns:
    #zeta = np.sqrt(1 - ((wd**2)/(wn**2)))
    G = (wn**2)/(s**2 + 2*zeta*wn*s + wn**2)
    t,y = control.step_response(G, T=simulation_time)
    axs[1].plot(t,y, label=f'wn = {wn}rad/s')
axs[1].set_title("Behavior of 2nd Order System's step response with respect to wn (zeta = 0.2)")
axs[1].set_xlabel('t(s)')
axs[1].set_ylabel('Amplitude')
axs[1].legend()

plt.tight_layout()
plt.show()
