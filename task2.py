import ti_robots as ti
import time 
import matplotlib.pyplot as plt
import numpy as np
import sys
from operator import itemgetter

bins = 72
nth_successor = 10
doRobot = False
saveLaser = False


def calc_angles(a):
    x = a[::2]
    y = a[1::2]
    angles = np.zeros(len(x)-nth_successor)
    for i in range (nth_successor, len(x)):
        p1 = np.array([x[i-nth_successor], y[i-nth_successor]])
        p2 = np.array([x[i], y[i]])
        u = p2 - p1
        theta = np.arccos(u[0]/ np.linalg.norm(u, ord=2))
        angles[i-nth_successor] = theta
    return angles

def cross_correlation(hist1, hist2):
    h1 = hist1[0]
    h2 = hist2[0]
    n = len(h1)
    k = np.zeros(n)
    for j in range(n):
        for i in range(n):
            k[j] += h1[i] * h2[(i+j)%n]
    return k

def rotate(scan, angle):
    rot = []
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle), np.cos(angle)]])
    for i in range(0, len(scan), 2):
        x1 = scan[i]
        x2 = scan[i+1]
        v = np.array([x1, x2])
        rot_v = np.dot(R,v)
        rot.append(rot_v[0])
        rot.append(rot_v[1])
    return rot


with open('scans.npy', 'rb') as file:
    b = np.load(file)
    a = np.load(file)
    a_angles = calc_angles(a)
    b_angles = calc_angles(b)
    hist1 = np.histogram(a_angles, bins=bins, range=(0, np.pi))

    max_idx, max_value = max(enumerate(hist1[0]), key=itemgetter(1))
    max_angle = hist1[1][max_idx]
    print('max_angle = ', max_angle)

    a_rot = rotate(a, -max_angle)
    a_rot_angles = calc_angles(a_rot)
    a_rot_hist = np.histogram(a_rot_angles, bins=bins, range=(0, np.pi))

    hist2 = np.histogram(b_angles, bins=bins, range=(0, np.pi))
    k = cross_correlation(a_rot_hist, hist2)
    print('k = ', k, ' shape ', k.shape, ' type', type(k))

    xs = np.arange(0, np.pi, np.pi/bins)
    plt.plot(xs, k)
    plt.show()

    index, element = max(enumerate(k), key=itemgetter(1))
    b_rot = rotate(b, -xs[index])
    b_rot_angles = calc_angles(b_rot)
    hist_b_rot = np.histogram(b_rot_angles, bins=bins, range=(0, np.pi))

    plt.plot(a_rot[::2], a_rot[1::2])
    plt.plot(b_rot[::2], b_rot[1::2])
    plt.show()


if not doRobot:
    sys.exit()

with ti.robots.PioneerLaserRobot("10.42.0.1", 50051) as bot:

    bot.laser = ti.laser_client.Laser(bot.channel)
    bot.base.set_auto_stop(False)

    a = bot.laser.readXY()

    with open('scans.npy', 'ab') as file:
        np.save(file, a)

    angles = calc_angles(a)
    anglesDeg = np.rad2deg(angles)
    
    x = a[::2]
    y = a[1::2]
    print(angles)
    fig, axs = plt.subplots(1, 3)
    axs[0].plot(x, y)
    axs[1].hist(angles, bins=bins)
    axs[2].hist(anglesDeg, bins=bins)
    plt.show()

    hist1 = np.histogram(angles, bins=bins, range=(0, np.pi))
    print(hist1)

    #print(a)
    #print("number of values: " + str(len(a)))

