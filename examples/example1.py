from lambert_exponential_sinusoid import ExponentialSinusoidFamily
import numpy as np
import matplotlib.pyplot as plt

# ACTUALLY USING THE CLASS
exponential_sinusoid = ExponentialSinusoidFamily(1 / 8, 1, 1.5, np.pi / 6, 1)
limits = exponential_sinusoid.get_flight_path_limits()
# exponential_sinusoid.get_theta_array(), exponential_sinusoid.get_radial_distance_array(fpa)

# FIGURE STUFF
plt.figure(figsize=(8, 8), dpi=400)
ax = plt.subplot(111, projection='polar')
for fpa in np.linspace(limits[0] * 0.4, limits[1] * 0.4, 50):
    ax.plot(exponential_sinusoid.get_theta_array(), exponential_sinusoid.get_radial_distance_array(fpa))
ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
ax.grid(True)
ax.set_title("Class $k_2=1/8$ Exponential Sinusoid\n" +
             "$r_1=1$;      " +
             "$r_2=1.5$;      " +
             "$\phi=\pi/6$;      " +
             "N=1"
             , va='bottom')
plt.savefig("example1.png")