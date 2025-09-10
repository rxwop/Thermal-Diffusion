import numpy as np, raster_geometry as rg
from parameters import *



def pixels(length):
    return length / scale
    # Converts continuous length to counterpart scale in pixels



def reuleaux(dims, height, infra_radius, radius):
    a = np.ones(dims, dtype = bool)

    constructors = [
    [-infra_radius, 0, 0],
    [0.5 * infra_radius, np.sqrt(3) / 2 * infra_radius, 0],
    [0.5 * infra_radius, -np.sqrt(3) / 2 * infra_radius, 0]]

    for i in constructors:
        a *= rg.cylinder(dims, height, radius, position = np.array(i) / np.array(dims) + 0.5)


    return a

# Construct Reuleaux triangle raster by intersection of three equidistant constructor cylinders






initial = np.ones(dims) * room_temp # inital temperature state

alpha = np.ones(dims) * alpha_air # set diffusivity to all alpha_air


cyl_bool = reuleaux(dims, pixels(h_cyl), pixels(infra_cyl), pixels(r_cyl))
water_bool = reuleaux(dims, pixels(h_water), pixels(infra_cyl), pixels(r_water))
wire_bool = rg.cylinder(dims, pixels(h_wire), pixels(r_wire), axis = 1)
# Rasterise reuleaux / cylinders as Boolean mask arrays

alpha[cyl_bool] = alpha_cyl
alpha[water_bool] = alpha_water
alpha[wire_bool] = alpha_wire
# Fill diffusivity data with these region masks


import plots as p
p.heatmap(cyl_bool[:, :, 20])
p.heatmap(cyl_bool[:, 20, :])
p.heatmap(cyl_bool[20, :, :])
exit()


J = voltage**2 / mass_resistor / heat_capacity_resistor / ref_resistance

def Wire_tick(self):
    arr = self.state - ref_temp
    arr = np.multiply(arr, self.diffusivity)

    arr += 1

    return J * np.reciprocal(arr)

# Define wire override tick




import simulation as sim

Model = sim.ThermalModel(initial, alpha, scale, 'void', -1, room_temp)
# Construct a model with the above initial state, diffusivity, delta_x, void boundary, no convergence cutoff rate

Model.voxel_tick_override(wire_bool, Wire_tick)
# Enact the resistive element simulation override

frames, times = Model.simulate_to(3, cache_fps=60, log = True)
# Simulate evolution of temperature


np.savez('simulation data', frames = frames, times = times)
# Save the data!
