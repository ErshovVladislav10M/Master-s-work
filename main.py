import math
import os
import time

import numpy as np
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput

from compute_angles import compute_angles_by_contour_points, compute_guide_vector_by_angles
from compute_cubes import compute_cubes
from create_video_with_contours import create


def start_video_capturing(motion_names, work_time):
    lsize = (320, 240)
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(main={"size": (1280, 720), "format": "RGB888"},
                                                     lores={"size": lsize, "format": "YUV420"})
    picam2.configure(video_config)
    encoder = H264Encoder(1000000)
    picam2.start()

    w, h = lsize
    prev = None
    encoding = False
    start_time = time.time()
    ltime = 0
    counter_motions = 0

    while start_time + work_time > time.time():
        cur = picam2.capture_buffer("lores")
        cur = cur[:w * h].reshape(h, w)
        if prev is not None:
            # Measure pixels differences between current and
            # previous frame
            mse = np.square(np.subtract(cur, prev)).mean()
            if mse > 7:
                if not encoding:
                    filename = f"motion_{counter_motions}"
                    encoder.output = FileOutput(filename + ".h264")
                    counter_motions += 1

                    picam2.start_encoder(encoder)
                    encoding = True
                    print("New Motion", mse)

                    time.sleep(1)
                    os.system(f"ffmpeg -r {30} -i {filename}.h264 -vcodec copy {filename}.mp4 -y")
                    os.system(f"rm {filename}.h264")
                    motion_names.append(filename)
                ltime = time.time()
            else:
                if encoding and time.time() - ltime > 2.0:
                    picam2.stop_encoder()
                    encoding = False
        prev = cur


motion_names = []

start_video_capturing(motion_names, 10)

for name in motion_names:
    average_contour_point_locations, height, width = create(name + ".mp4", name + "_withContours.avi", 30)
    os.system(f"rm {name}.mp4")

with open("cameraSettings/cameraSettings.txt", "r") as file:
    values = file.readline().split(";")
    camera_coordinate = (int(values[0]), int(values[1]), int(values[2]))
    alpha = int(values[3])
    gamma = int(values[4])
    cube_side = int(values[5])
    num_cubes = int(values[6])

guide_vectors = []
for average_contour_point_location in average_contour_point_locations:
    horizontal_angle, vertical_angle = compute_angles_by_contour_points(height, width, average_contour_point_location,
                                                                        max_horizontal_angle=31.1,
                                                                        max_vertical_angle=17.5)

    guide_vector = compute_guide_vector_by_angles(math.pi * (horizontal_angle + alpha) / 180,
                                                  math.pi * (vertical_angle + gamma) / 180)

    guide_vectors.append(guide_vector)

with open("detectedObjects/cubesWithObjects.txt", "w") as file:
    for guide_vector in guide_vectors:
        cubes = compute_cubes(camera_coordinate, guide_vector, cube_side, num_cubes)

        for cube in sorted(cubes):
            file.write(str(cube) + ";")
        file.write("\n")
