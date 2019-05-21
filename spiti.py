#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import time

#plt.ion()
fig, ax = plt.subplots()
ax.hlines(y=-3.1, xmin=6.5, xmax=8.5, linewidth=2, color='r')
ax.hlines(y=0, xmin=0, xmax=6.5, linewidth=2, color='r')
ax.hlines(y=0, xmin=7.4, xmax=8.5, linewidth=2, color='r')
ax.hlines(y=1.2, xmin=0, xmax=2.5, linewidth=2, color='r')
ax.hlines(y=1.2, xmin=6.5, xmax=7.4, linewidth=2, color='r')
ax.hlines(y=3.75, xmin=6.5, xmax=8.5, linewidth=2, color='r')
ax.hlines(y=3.75, xmin=5.4, xmax=6.5, linewidth=2, color='g')
ax.hlines(y=7.3, xmin=2.5, xmax=8.5, linewidth=2, color='r')

ax.vlines(x=0, ymin=0, ymax=1.2, linewidth=2, color='r')
ax.vlines(x=2.5, ymin=1.2, ymax=7.3, linewidth=2, color='r')
ax.vlines(x=5.4, ymin=0, ymax=1.2, linewidth=2, color='g')
ax.vlines(x=5.4, ymin=1.2, ymax=7.3, linewidth=2, color='r')
ax.vlines(x=6.5, ymin=0, ymax=1.2, linewidth=2, color='g')
ax.vlines(x=6.5, ymin=1.2, ymax=3.75, linewidth=2, color='r')
ax.vlines(x=6.5, ymin=-3.1, ymax=0, linewidth=2, color='r')
ax.vlines(x=7.4, ymin=0, ymax=1.2, linewidth=2, color='r')
ax.vlines(x=8.5, ymin=-3.1, ymax=0, linewidth=2, color='r')
ax.vlines(x=8.5, ymin=3.75, ymax=7.3, linewidth=2, color='r')

#epipla saloni
ax.hlines(y=0.7, xmin=0, xmax=4.6, linewidth=2, color='b')
ax.vlines(x=4.6, ymin=0, ymax=0.7, linewidth=2, color='b')

#epipla_kouzina
ax.hlines(y=-1.2, xmin=6.5, xmax=7.25, linewidth=2, color='b')
ax.vlines(x=7.25, ymin=-3.1, ymax=-1.2, linewidth=2, color='b')
ax.vlines(x=7.9, ymin=-3.1, ymax=0, linewidth=2, color='b')

#trapezi_saloni
ax.hlines(y=4.05, xmin=3.35, xmax=4.25, linewidth=2, color='b')
ax.hlines(y=5.8, xmin=3.35, xmax=4.25, linewidth=2, color='b')
ax.vlines(x=3.35, ymin=4.05, ymax=5.8, linewidth=2, color='b')
ax.vlines(x=4.25, ymin=4.05, ymax=5.8, linewidth=2, color='b')

#krevati_upnodomatio
ax.hlines(y=5.1, xmin=6.4, xmax=8.5, linewidth=2, color='b')
ax.hlines(y=6.6, xmin=6.4, xmax=8.5, linewidth=2, color='b')
ax.vlines(x=6.4, ymin=5.1, ymax=6.6, linewidth=2, color='b')
print("OK")

i = 0
with open('positions.txt','r') as file:
    lines = file.readlines()
    points_x = np.arange(0.,len(lines))
    points_y = np.arange(0.,len(lines))
    for line in lines:
        #numbers = line.strip().split()
        #x = float(numbers[0].strip('[,'))
        #y = float(numbers[1].strip(']'))
        numbers = line.split(',')
        x = float(numbers[0])
        y = float(numbers[1])
        print(x,y)
        points_x[i] = x
        points_y[i] = y
        i += 1

#ax.plot(points_x[:i], points_y[:i], color='k')
ax.plot(points_x, points_y, color='k')

plt.show()
#plt.draw()
