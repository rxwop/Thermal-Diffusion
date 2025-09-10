from math import ceil
import matrices as mt
import numpy as np
import time as t


def find_dt(self) -> float:
    a_max = np.max(self.diffusivity)
    return self.delta_xyz**2 / a_max / np.ndim(self.initial_state) / 8



class ThermalModel:

    def reset_sim(self) -> None:

        self.frames = []
        # Creates list to store frames

        self.frame_times = []
        # Creates list for times corresponding to frames


        self.state = np.copy(self.initial_state)
        # Makes a copy of the initial state

        self.time = 0.00
        # Resets simulation time

        self.cache_state()
        # Saves first frame



    def __init__(self, initial_state, thermal_diffusivity, delta_xyz, boundary_conditions = 'repeat', smallest_rate = -1, void_temp = 0) -> None:
        self.dims = np.shape(initial_state)
        self.initial_state = initial_state
        # Gives alias to static initial_state


        self.stop = smallest_rate
        # Smallest rate of temperature change (K/s) before simulation "converges" and stops

        
        self.void_temp = void_temp
        # Temperature of void boundary condition (if chosen)


        self.reset_sim()
        # Resets simulation

        self.diffusivity = np.copy(thermal_diffusivity)

        self.delta_xyz = delta_xyz

        self.boundary_conditions = boundary_conditions


        self.overrides = []
        # List of tuples of overrides



    def voxel_tick_override(self, overriden_voxels, appended_tick_differential) -> None:
        override = ( (overriden_voxels != 0) , appended_tick_differential)
        # Overriden_voxels is truned into a Boolean mask, selecting which pixels to override
        # Appended_tick_differential (type: Function) should take args (self) and return an array of self.dims to be multiplied by dt
        
        self.overrides.append(override)
    




    def cache_state(self) -> None:
        self.frames.append(np.copy(self.state))
        self.frame_times.append(self.time)
        # Saves current time, frame


    def tick(self, delta_time) -> bool:

        differential = mt.Laplacian(self.state, self.delta_xyz, self.boundary_conditions, self.void_temp)
        # Works out discretised Laplacian, with the given boundary condition

        differential *= self.diffusivity

        for override in self.overrides:
            differential += override[0] * override[1](self)
        # Local (masked by override[0]) override equation iterations


        if np.max(differential) < self.stop:
            return False
        # Check if further iterations will result in temperature change greater than the smallest allowed rate

        self.state += differential * delta_time
        # Global heat equation iteration


        self.time += delta_time
        # Advance time


        return True
        # returns False if simulation "converges" (falls below minimum allowed rate of change)


    def simulate_to(self, time, cache_fps = None, dt = None, log = False):
        self.reset_sim()

        if dt is None:
            dt = find_dt(self)
        # If no dt given, finds a suitable convergent delta time

        ticks = int(time / dt)
        # Works out how many times to tick

        checks = int(ticks / 10)
        # Works out how many ticks makes 10%

        tic = t.time()
        # Set stopwatch

        if cache_fps:
            # If a selective frame caching rate (simulated time) is given, only save frames every 'caches' ticks
            caches = ceil(1 / cache_fps / dt)
            for i in range(ticks):

                if log and i % checks == 0:
                    percent = round(i / ticks, 1) * 100
                    print(percent, "% : t = ", self.time)
                    # Print every 10% progress


                if i == 20:
                    elapsed = t.time() - tic
                    print("ETA in seconds: ", round(elapsed / 20 * (ticks - 20), 1))
                    # Calculate an overestimated time of completion (seconds)


                if not self.tick(dt):
                    print("Simulation converges, stopping further iteration")
                    self.cache_state()
                    break
                # Checks for "convergence", breaks the loop of simulation

                if i % caches == 0:
                    self.cache_state()

        else:
            # Else save every frame
            for i in range(ticks):

                if log and i % checks == 0:
                    percent = round(i / ticks, 1) * 100
                    print(percent, "% : t = ", self.time)


                if i == 20:
                    elapsed = t.time() - tic
                    print("ETA in seconds: ", round(elapsed / 20 * (ticks - 20), 1))

                b = self.tick(dt)

                if not b:
                    print("Simulation converges, stopping further iteration")
                    self.cache_state()
                    break

                self.cache_state()

        return np.array(self.frames), np.array(self.frame_times)
        # Returns tuple of array of frames across time and the corresponding frame times

