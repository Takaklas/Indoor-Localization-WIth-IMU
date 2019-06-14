#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import time

import positions
import netmode
from my_compass import draw_compass, draw_arrow

import sys
visualise = False
if len(sys.argv) > 1:
    import socket
    import select
    visualise = True
    UDP_IP = "0.0.0.0"
    UDP_PORT = 5005

    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

plt.ion()
fig, ax = plt.subplots()
netmode.plot_ergasthrio(ax)
fig.canvas.draw()

fig2, ax2 = plt.subplots()
draw_compass(ax2)
arrow = draw_arrow(ax2, 0)
fig2.canvas.draw()
arrow.remove()

positions = positions.Positions
for i in positions:
    ax.plot(positions[str(i)]['Position_X'],
            positions[str(i)]['Position_Y'], 
            marker='o', markersize=3, color="black")
    ax.text(positions[str(i)]['Position_X'], 
            positions[str(i)]['Position_Y'], str(i), color="red", fontsize=12)

if visualise:
    points_x = []
    points_y = []
    while True:
        ready = select.select([sock], [], [], 0.025)
        if ready[0]:
            data = sock.recv(80).decode().split()
            if len(data) >= 2:
                x = float(data[0])
                y = float(data[1])
                print(x,y)
                points_x.append(x)
                points_y.append(y)
                ax.plot(points_x, points_y, color='k')
                fig.canvas.draw()
                #time.sleep(0.5)
            else:
                arrow = draw_arrow(ax2, float(data[0]))
                fig2.canvas.draw()
                arrow.remove()

with open('positions.txt','r') as file:
    lines = file.readlines()
    points_x = []
    points_y = []
    for line in lines:
        #numbers = line.strip().split()
        #x = float(numbers[0].strip('[,'))
        #y = float(numbers[1].strip(']'))
        numbers = line.split(',')
        x = float(numbers[0])
        y = float(numbers[1])
        print(x,y)
        points_x.append(x)
        points_y.append(y)
        ax.plot(points_x, points_y, color='k')
        fig.canvas.draw()
        #time.sleep(0.5)

#ax.plot(points_x[:i], points_y[:i], color='k')
ax.plot(points_x, points_y, color='k')

locations = [ (-7.3,15), (-2.3,16), (2.3,6) , (0.2,10)]
distances = [ 2.712, 1.259, 1.585, 4.299 ]
colors = ['r','g','b','y']
for i in range(len(locations)):
	circle = plt.Circle(locations[i], distances[i], color=colors[i], fill=False, clip_on=False)
	ax.add_artist(circle)

plt.ioff()
plt.show()
