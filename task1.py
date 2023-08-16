import ti_robots as ti
import time 
import numpy as np


wall_distance = 0.7
corridor_width = 0.6

angle = np.rad2deg(np.arctan(corridor_width/(2*wall_distance)))
laser_angle = 270 / 811
laser_count = np.round(angle/laser_angle)
print(laser_count)

with ti.robots.PioneerLaserRobot("10.42.0.1", 50051) as bot:

    bot.laser = ti.laser_client.Laser(bot.channel)
    bot.base.set_auto_stop(False)

    velocity = 0.1
    v2 = 0.5 * velocity

    lock = False
        
    while True:

        distances = bot.laser.read()
        sliced_distances = distances[405-laser_count:405+laser_count]
        min_distance = np.min(sliced_distances)
        r, l = np.array_split(sliced_distances, 2)
        left = np.min(l)
        right = np.min(r)
        if (min_distance > wall_distance):
            print('Forward')
            bot.base.set_velocity(velocity)
            lock = False
        #turn right
        elif left < right and not lock:
            print('Locking Right')
            lock = True
            bot.base.set_velocity_lr(v2, -v2)
        elif right < left and not lock:
            print('Locking Left')
            lock = True
            bot.base.set_velocity_lr(-v2, v2)
        time.sleep(0.1)
        


