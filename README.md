# Master-dissertation
Expanding the capabilities of existing infrastructure to solve the problem of drone dispatching

### About project
The number of drones is increasing day by day. There is a need to control their movements to prevent incidents. In modern cities, the number and quality of cameras is also growing steadily.
Cameras require periodic maintenance. During such maintenance, it is possible to expand existing functionality by adding inexpensive boards and image processing tools, which will allow tracking and, in the future, predicting drone trajectories.

### Hardware
- Raspberry Pi 4 platform with Raspberry Pi Camera Board v2.1
- Operating system - Raspberry Pi OS

### Install python libraries
- From root:
```
sudo apt update
sudo apt upgrade
```

- Install Python
```
sudo apt install python3-pip
```

- Install Python libraries
```
sudo apt install python3-numpy
```

- Install Raspberry libraries
```
sudo apt install python3-picamera2
```