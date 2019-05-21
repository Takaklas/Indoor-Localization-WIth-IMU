import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math

import numpy as np
import quaternion

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

g = 9.80665
gravity = np.array([0, 0, 1])
speed = np.array([0, 0, 0])
position = np.array([4.5, 3.5, 0])
time_elapsed = 0
dt = 0
start = time.time()
end = 0
c = 1 # (1 + alpha) / 2.
alpha = 0.9
file_pos = open("positions.txt","w")
file_pos.write('{},{}\n'.format(position[0],position[1]))
min_x, min_y, min_z = 10, 10, 10 
max_x, max_y, max_z = -10, -10, -10

try:
    while True:
        if imu.IMURead():
            # x, y, z = imu.getFusionData()
            # print("%f %f %f" % (x,y,z))
            data = imu.getIMUData()
            fusionPose = data["fusionPose"]
            pitch, roll, yaw = fusionPose
            
            acc_x, acc_y, acc_z = (i * g for i in data["accel"])
            # acc_x, acc_y, acc_z = (i * g for i in imu.getAccelResiduals())
            #acc_z = (1 - alpha) * acc_z + alpha * sample_old
            #print(acc_z)
        
            # local_coordinate_system:
            lcs = data["fusionQPose"]
            q_lcs = np.quaternion(lcs[0], lcs[1], lcs[2], lcs[3])
            # accel quaternion:
            acc_lcs = data["accel"]
            q_acc = np.quaternion(acc_lcs[0], acc_lcs[1], acc_lcs[2])
            # global_coordinate_system:
            q_gcs = q_lcs * q_acc * q_lcs.inverse()
            acc_gcs = q_gcs.vec
            #print("LCS_X: %6.3f LCS_Y: %6.3f LCS_Z: %6.3f" % (acc_lcs[0], acc_lcs[1], acc_lcs[2]))
            #print("GCS_X: %6.3f GCS_Y: %6.3f GCS_Z: %6.3f" % (acc_gcs[0], acc_gcs[1], acc_gcs[2]))

            # rotate global coordinate system
            # on z axis by θ degrees
            angle = 160 # 90 -25
            angle_rad = math.radians(angle)
            # https://math.stackexchange.com/questions/2261003/rotating-a-quaternion-around-its-z-axis-to-point-its-x-axis-towards-a-given-poin
            q_rotator = np.quaternion(math.cos(angle_rad/2.0), 0, 0, math.sin(angle_rad/2.0))
            q_spiti = q_rotator * q_gcs * q_rotator.inverse()
            acc_spiti = q_spiti.vec
            # SCS = spiti coordinate system
            #print("SCS_X: %6.3f SCS_Y: %6.3f SCS_Z: %6.3f" % (acc_spiti[0], acc_spiti[1], acc_spiti[2]))
            min_x = min(min_x, acc_spiti[0])
            min_y = min(min_y, acc_spiti[1])
            min_z = min(min_z, acc_spiti[2])
            max_x = max(max_x, acc_spiti[0])
            max_y = max(max_y, acc_spiti[1])
            max_z = max(max_z, acc_spiti[2])
            #print("Min X: %6.3f Y: %6.3f Z:%6.3f" % (min_x, min_y, min_z))
            #print("Max X: %6.3f Y: %6.3f Z:%6.3f" % (max_x, max_y, max_z))
            #r, p, y = map(math.degrees,quaternion.as_euler_angles(q_lcs))
            #print("Roll: %10.3f Pitch: %10.3f Yaw: %10.3f" % (r, p, y))

            end = time.time()
            dt = end - start
            start = end
            acc_spiti = -((acc_spiti - gravity) * g)
            speed = c * (acc_spiti * dt) + speed #alpha * speed
            position = c * (speed * dt) + position #alpha * position
            file_pos.write('{:.3f},{:.3f}\n'.format(position[0],position[1]))
            #file_pos.write('{:.3f},{:.3f},{:.3f}\n'.format(position[0],position[1],position[2]))
            time_elapsed += dt

            time.sleep(poll_interval * 1.0 / 1000.0)
except KeyboardInterrupt:
    file_pos.close()
        
