#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import sys
import math
'''
file = open("accel.txt","w") 
file.write("1\n") 
file.write("2\n")
file.write("3\n")
file.write("4\n") 
file.close() 
'''


#takes a np array
def low_pass_filter(y_old, alpha=0.9):
    y_new = [y_old[0]] * (y.size + 1)
    for i in range(0, y.size, 1):
        y_new[i + 1] = (1 - alpha) * y_old[i] + alpha * y_new[i]
    return np.array(y_new[1:])


def low_pass_filter2(y_old, alpha=0.9):
    y_new = [y_old[0]] * (y.size + 1)
    for i in range(0, y.size, 1):
        y_new[i + 1] = (1 - alpha) * y_old[i] + alpha * y_new[i]
    return np.array(y_new)


def high_pass_filter(y_old, alpha=0.9):
    y_new = [9.81] * y.size
    for i in range(0, y.size - 1, 1):
        y_new[i + 1] = (1 - alpha) * y_new[i] + (1 - alpha) * (
            y_old[i + 1] - y_old[i])
    return np.array(y_new)

def read_file(file):
    with open(file, "r") as a:
        points = a.read().split()
    print("Done reading")
    y = np.array(points).astype(np.float)
    return y

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        file = "accel_Z.txt"
    
    y = read_file(file) 
    size = len(y)
    #hypothetic: 
    #interval = 0.004
    interval = 0.012
    start = 0.
    end = size * interval
    x = np.arange(start, end, interval)[:size]   
    plt.plot(x, y, label=file.split('.')[0]) #'Accel')

    y2 = read_file("accel_Y.txt")
    y2 = low_pass_filter(y2, alpha=0.9)
    y2 = y2 + 9.81
    #plt.plot(x, y2, label='Accel_Y')

    heading = read_file("heading.txt")
    plt.plot(x, [0.5*math.pi]*size, label='90 degrees')
    plt.plot(x, [math.pi]*size, label='180 degrees')
    plt.plot(x, [1.5*math.pi]*size, label='270 degrees') 
    plt.plot(x, [2*math.pi]*size, label='360 degrees')
    linestyles = ['-', '--', '-.', ':']
    plt.plot(x, [0.25*math.pi]*size, linestyle = linestyles[3], label='45 degrees')
    plt.plot(x, [0.75*math.pi]*size, linestyle = linestyles[3], label='135 degrees')
    plt.plot(x, [1.25*math.pi]*size, linestyle = linestyles[3], label='225 degrees') 
    plt.plot(x, [1.75*math.pi]*size, linestyle = linestyles[3], label='315 degrees')
    plt.plot(x, heading, label='heading')

    dt = interval  # = 1/fs where fs is your sampling frequency
    cut_off_freq = 20  # Hz
    tau = 1 / cut_off_freq  # desired time constant
    alpha = tau / (tau + dt)
    print("alpha = %f" % alpha)
    #plt.plot(x, low_pass_filter(y,alpha = alpha), label='LPF Accel')
    #plt.plot(x, high_pass_filter(y, alpha = alpha), label='HPF Accel')

    #fig, ax = plt.subplots()
    #y = low_pass_filter(y, alpha=alpha)
    steps = 0
    sample_old = 0
    i = 0  # general index counter
    j = 0  # window index counter
    j_end = 0.5 / interval  # every 0.5 sec window
    new_min = 20
    min = 20
    new_max = 0
    max = 0
    threshold = 9.81
    for point in y:
        #check if we have a step
        if (point < sample_old) and (point < threshold) and (threshold < sample_old):
            if (new_max - new_min) > 2:  # and (new_max-threshold)>1 and (threshold-new_min)>1:
                plt.plot(i * interval, point, 'o')
                steps += 1
            new_max = 0
            new_min = 20
        sample_old = point

        #update new_min, new_max for this step
        if (point < new_min):
            new_min = point
        elif (point > new_max):
            new_max = point

        #calculate min max for next threshold
        if (point < min):
            min = point
        elif (point > max):
            max = point
        i += 1
        j += 1

        #check if window is reached
        if (j == j_end):
            threshold = (max + min) / 2
            x2 = np.arange(i * interval, (i + j_end) * interval, interval)
            y2 = [threshold] * int(j_end)
            plt.plot(x2, y2)  #, label='Threshold')
            j = 0
            min = 20
            max = 0

    print("Steps: %d" % steps)

    #plt.axis([0, end, y.min()-1, y.max()+1])
    plt.title("File: {} | Number of steps: {}".format(file.split('.')[0], steps))
    plt.xlabel('time(s)')
    plt.ylabel('linear acceleration(m/s^2)')
    plt.grid()
    plt.legend()
    plt.show()

