# Indoor-Localization-WIth-IMU
Pedestrian Dead Reckoning a.k.a. Indoor Localization using IMU (Inertial Measurement Unit)

A set of python scripts for indoor localization using IMU. Heavy use of the RTIMU library for IMU management, data gathering and orientation estimation using kalman-RTQF filters.
RTIMULib : https://github.com/RTIMULib/RTIMULib2

A brief description:
- position_PDR.py: Performs localization based on the Step Counting technique, combined with orientation (mainly heading) from the sensor. A fixed step length is used and heading is corrected using a predifined offset based on mapping of the space used indoors. Performs quite nicely (>95% step detection). Errors accumulate from heading declinations (~5-10 degrees) so quantization of heading is used (that means we split the 360 degree plane in 2,4,8 etc regins such as eg for 4 regions:
  - -45<^<45 -> 0 degrees
  - 45<^<145 -> 90 degrees
  etc.
  
  If called with a random parameter, sends data to an inserted ip server running plot.py file for visualization.
  Implementation based on: https://web.cs.wpi.edu/~emmanuel/courses/cs528/F17/slides/lecture06b.pdf
  
- position_Dead_reckoning.py: Performs localization by double integration of accelerometer sensor, combined with orientation (mainly heading) from the sensor. Does LCS (Local Coordinate System) to GCS (Global Coordinate System) using quaternions. Performs poorly.
  based on https://www.st.com/resource/en/design_tip/dm00513638.pdf  
  
 - plot.py: Visualization in space, uses a file like ergasthrio.py with matplotlib indoor map design. If called with any random parameters, visualization is done in real time, just supply server ip (found using ifconfig) to the script called for sending data like position_PDR.py .
