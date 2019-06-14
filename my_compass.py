import matplotlib.pyplot as plt
from math import sin, cos, radians
from time import sleep

#plt.ion()
#fig, ax = plt.subplots()
#ax.patch.set_facecolor('black')
#img = plt.imread("OuterRing.png")
#ax.imshow(img, extent=[-309/2,309/2,-309/2,309/2])
#img2 = plt.imread("CompassNeedle.png")
#ax.imshow(img2, extent=[-30/2,30/2,-273/2,273/2])

def draw_compass(ax):
    img = plt.imread("compass.png")
    width = img.shape[0]
    height = img.shape[1]
    offset = 20.5
    ax.imshow(img, extent=[-width/2-offset,width/2-offset,-height/2,height/2])

def draw_arrow(ax, degrees):
    radius = 500
    x = radius * cos(radians(degrees))
    y = radius * sin(radians(degrees))
    arr = ax.arrow(0, 0, x, y, linewidth=10, head_width=100, head_length=100, fc='k', ec='k')
    return arr

if __name__ == '__main__':
    plt.ion()
    fig, ax = plt.subplots()
    draw_compass(ax)
    fig.canvas.draw()

    degrees = 0
    while degrees < 360:
        arrow = draw_arrow(ax, degrees)
        fig.canvas.draw()
        arrow.remove()
        degrees += 1
        #sleep(0.1)

    plt.ioff()
    plt.show()
