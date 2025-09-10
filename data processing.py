import plots as p, numpy as np
from parameters import infra_cyl, h_water, r_cyl, scale


with np.load('simulation data.npz') as data:
    frames = data['frames']
    times = data['times']

frames = frames[::6]
times = times[::6]

dims = np.shape(frames)[1:]
mid = np.array(np.rint(np.array(dims) / 2), dtype = int) # Midpoints of array in each dim

def pixels(length):
    return int(length / scale)
    # Converts continuous length to counterpart scale in pixels


#p.heatmap_anim(frames[:, :, :, mid[2]])


from matplotlib import pyplot as plt

frames -= 25
frames *= 40
frames += 25

fig = plt.figure()

r_intercircle = r_cyl - infra_cyl

plt.plot(times, frames[:, mid[0], mid[1], mid[2]])
plt.plot(times, frames[:, mid[0] - pixels(0.25 * r_intercircle), mid[1], mid[2] + pixels(h_water / 4)])
plt.plot(times, frames[:, mid[0] - pixels(0.5 * r_intercircle) + 2, mid[1], mid[2] + pixels(h_water / 2)])

plt.show()