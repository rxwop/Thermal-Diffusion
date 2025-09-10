voltage = 1.5
ref_resistance = 50
mass_resistor = 3e-5
heat_capacity_resistor = 431
ref_temp = 25

room_temp = 25

alpha_air = 1.94e-5
alpha_water = 1.46e-7
alpha_cyl = 0.214e-6
alpha_wire = 3.72e-6

h_cyl = 7e-3
r_cyl = 6e-2
infra_cyl = 5.713e-2
thickness_cyl = 1.1e-3
r_water = r_cyl - thickness_cyl
h_water = h_cyl - 2 * thickness_cyl

h_wire = 4.5e-3
r_wire = 1e-3





a = 10 # Multiplier for dimensions
dims = (4*a, 4*a, 4*a)
length_x = h_cyl * 1.5 # length of Z side

scale = length_x / dims[2] # dx