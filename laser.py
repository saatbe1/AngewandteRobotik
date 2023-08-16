import ti_robots as ti
import time 
import matplotlib.pyplot as plt

with ti.robots.PioneerLaserRobot("10.42.0.1", 50051) as bot:

    bot.laser = ti.laser_client.Laser(bot.channel)
    bot.base.set_auto_stop(True)

    # example to move the robot forward
    #bot.base.move(0.1)

    # get and print 10 laser readings:
    for x in range(10):
        print("reading number " + str(x) + " : ")
        # read laser scan xy (returns list of x and y values) - only available with tim561
        a = bot.laser.readXY()
        print(a)
        x = a[::2]
        y = a[1::2]
        print(x)
        print(y)
        plt.plot(x, y)
        plt.show()
        #print(a)
        #print("number of values: " + str(len(a)))
        time.sleep(2)

