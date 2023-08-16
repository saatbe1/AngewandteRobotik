import ti_robots as ti
import time 
import numpy as np

with ti.robots.PioneerLaserRobot("10.42.0.1", 50051) as bot:

    bot.laser = ti.laser_client.Laser(bot.channel)
    bot.base.set_auto_stop(True)

    wall_distance = 0.7
    velocity = 0.1
    
    while True:
        print('.')
        distances = bot.laser.read()
        sliced_distances = distances[353:457]
        min_distance = np.min(sliced_distances)

        l, r = np.array_split(sliced_distances, 2)
        left = np.min(l)
        right = np.min(r)
        if (min_distance > wall_distance):
            bot.base.set_velocity(velocity)
        #turn right
        elif left < right:
            while min_distance <= wall_distance:
                bot.base.set_velocity_lr(velocity, -1*velocity)
        else:
            while min_distance <= wall_distance:
                bot.base.set_velocity_lr(-1*velocity, velocity)


