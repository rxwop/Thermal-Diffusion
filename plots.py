import matplotlib.pyplot as plt, matplotlib.animation as animation
import numpy as np

def heatmap(arr, block = True):
    fig = plt.imshow(arr, cmap='hot', interpolation='nearest')
    plt.colorbar(fig)
    plt.show(block=block)

def heatmap_anim(arr, step = 1):
    fig = plt.figure()
    im = plt.imshow(arr[0], cmap='hot', interpolation='nearest', vmin = np.min(arr), vmax = np.max(arr))
    plt.colorbar(im)

    def init():
        im.set_data(arr[0])
        return [im]

    def animate(i):
        im.set_array(arr[i])
        return [im]

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=np.shape(arr)[0], interval=20, blit=True)

    anim.save('heatmap.gif')
