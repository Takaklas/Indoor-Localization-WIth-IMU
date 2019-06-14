import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math

import numpy as np
import quaternion

visualise = False
if len(sys.argv) > 1:
    import socket
    visualise = True
    UDP_IP = "192.168.1." + str(input("Enter server ip: 192.168.1."))
    UDP_PORT = 5005
    MESSAGE = "Hello, World!"

    print("UDP target IP:", UDP_IP)
    print("UDP target port:", UDP_PORT)
    print("message:", MESSAGE)
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP

SETTINGS_FILE = "RTIMULib"

print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
    print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

print("IMU Name: " + imu.IMUName())

if (not imu.IMUInit()):
    print("IMU Init Failed")
    sys.exit(1)
else:
    print("IMU Init Succeeded")

# this is a good time to set any fusion parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)

steps = 0
alpha = 0.9
sample_old = 9.81
i = 0  # general index counter
j = 0  # window index counter
j_end = 0.5 / poll_interval  # every 0.5 sec window
new_min = 20
min = 20
new_max = 0
max = 0
threshold = 9.81
g = 9.80665
#position = [4.5, 3.5]
position = [1.2, 12]
step_len = 0.65
file_x = open("accel_X.txt","w") 
file_y = open("accel_Y.txt","w")
file_z = open("accel_Z.txt","w")
file_pos = open("positions.txt","w")
file_heading = open("heading.txt","w")
file_positions_heading = open("positions_heading.txt","w")
file_pos.write('{:.3f},{:.3f}\n'.format(position[0],position[1]))
heading = 90
file_positions_heading.write('{:.3f}\n'.format(heading))

start = time.time()
reps = 0
start_of_step = time.time()
last_sent_heading_data_time = time.time()
quantization_every_degrees = 45 #90
try:
    while True:
        if imu.IMURead():
            reps += 1
            # x, y, z = imu.getFusionData()
            # print("%f %f %f" % (x,y,z))
            data = imu.getIMUData()
            fusionPose = data["fusionPose"]
            pitch, roll, yaw = fusionPose

            # correct heading
            pitch, roll, yaw = map(math.degrees,fusionPose)
            if yaw < 0: yaw = yaw + 360.0
            #heading = 280.0 - heading
            heading = 165 - yaw #165.0 - yaw
            if heading < 0: heading += 360
            heading_keep_rad = math.radians(heading)
            heading_quantized = round(heading/90) * 90 #-90
            heading_rad = math.radians(heading_quantized)               
            file_heading.write('{:.3f}\n'.format(heading_keep_rad))
            if visualise and (time.time() - last_sent_heading_data_time > 0.1):
                last_sent_heading_data_time = time.time()
                MESSAGE = '{:.3f}\n'.format(heading)
                print(MESSAGE)
                sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

            # local_coordinate_system:
            lcs = data["fusionQPose"]
            q_lcs = np.quaternion(lcs[0], lcs[1], lcs[2], lcs[3])
            # accel quaternion:
            acc_lcs = data["accel"]
            q_acc = np.quaternion(acc_lcs[0], acc_lcs[1], acc_lcs[2])
            # global_coordinate_system:
            q_gcs = q_lcs * q_acc * q_lcs.inverse()
            acc_gcs = q_gcs.vec
            acc_x, acc_y, acc_z = (i * g for i in acc_gcs)

            # acc_x, acc_y, acc_z = (i * g for i in data["accel"])
            # acc_x, acc_y, acc_z = (i * g for i in imu.getAccelResiduals())
            acc_z = (1 - alpha) * acc_z + alpha * sample_old
            #print(acc_z)

            file_x.write('{:.3f}\n'.format(acc_x))
            file_y.write('{:.3f}\n'.format(acc_y))
            file_z.write('{:.3f}\n'.format(acc_z))

            #start of new possible step
            if (acc_z > sample_old) and (acc_z > threshold) and (threshold > sample_old):
                start_of_step = time.time()

            #check if we have a step
            if (acc_z < sample_old) and (acc_z < threshold) and (threshold < sample_old):
                end_of_step = time.time()
                step_condition_1 = step_condition_2 = False
                if end_of_step - start_of_step > 0.1: step_condition_1 = True
                if (new_max - new_min) > 2: step_condition_2 = True
                #if (new_max-threshold) > 1: step = True
                #if (threshold-new_min) > 1: step = True 
                
                if step_condition_1 and step_condition_2:
                    #step_len = 1.131 * math.log(new_max - new_min) + 0.159
                    position[0] += step_len * math.cos(heading_rad)
                    position[1] += step_len * math.sin(heading_rad)
                    print(position)
                    file_pos.write('{:.3f},{:.3f}\n'.format(position[0],position[1]))
                    file_positions_heading.write('{:.3f}\n'.format(heading))
                    steps += 1
                    if visualise:
                        MESSAGE = '{:.3f} {:.3f}\n'.format(position[0],position[1])
                        print(MESSAGE)
                        sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
                # else: print("NO STEP")
                new_max = 0
                new_min = 20
            sample_old = acc_z            

            #update new_min, new_max for this step
            if (acc_z < new_min):
                new_min = acc_z
            elif (acc_z > new_max):
                new_max = acc_z

            #calculate min max for next threshold
            if (acc_z < min):
                min = acc_z
            elif (acc_z > max):
                max = acc_z
            i += 1
            j += 1

            #check if window is reached
            if (j == j_end):
                threshold = (max + min) / 2
                j = 0
                min = 20
                max = 0

            time.sleep(poll_interval * 1.0 / 1000.0)
except KeyboardInterrupt:
    file_x.close()
    file_y.close()
    file_z.close()
    file_pos.close()
    file_heading.close()
    file_positions_heading.close()
    print("Mean time {}ms".format((time.time()-start)/reps))
    print("Total steps: %d " % steps)


