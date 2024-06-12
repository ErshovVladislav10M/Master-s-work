import math
import time

import cv2

from compute_angles import compute_angles_by_contour_points
from compute_angles import compute_angles_by_guide_vector
from compute_angles import compute_contour_points_by_angles
from compute_angles import compute_guide_vector_by_angles


def create_video_by_images(video_with_contours_location: str, images: list, fps: int):
    height, width, _ = images[0].shape
    video = cv2.VideoWriter(
        video_with_contours_location,
        cv2.VideoWriter.fourcc("M", "J", "P", "G"),
        # cv2.VideoWriter.fourcc(*"mp4v"),
        fps,
        (width, height)
    )
    _ = [video.write(i) for i in images]
    video.release()


def create(video_location, video_with_contours_location, fps):
    video = cv2.VideoCapture(video_location)
    _, frame1 = video.read()
    _, frame2 = video.read()

    images = []
    average_contour_point_locations = []
    height, width = 0, 0

    while video.isOpened():
        try:
            difference = cv2.absdiff(frame1, frame2)
        except Exception:
            break

        gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        _, threshold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilate = cv2.dilate(threshold, None, iterations=3)
        contours, _ = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contour_point_locations = []
        for i, contour in enumerate(contours):
            for j, contour_point in enumerate(contour):
                contour_point_locations.append((contour_point[0][0], contour_point[0][1]))
                cv2.circle(frame1, (contour_point[0][0], contour_point[0][1]), 2, (0, 255, 0), 2, cv2.LINE_AA)

                height, width, _ = frame1.shape
                # contour_point1 = test_compute_contour_point(height, width, (contour_point[0][0], contour_point[0][1]))
                # contour_point1 = (int(contour_point1[0]), int(contour_point1[1]))
                # cv2.circle(frame1, contour_point1, 1, (0, 0, 255), 2, cv2.LINE_AA)

        if len(contour_point_locations) > 0:
            average_contour_point_location = compute_average_contour_point_locations(contour_point_locations)
            average_contour_point_locations.append(average_contour_point_location)

            cv2.circle(
                frame1, (average_contour_point_location[0], average_contour_point_location[1]), 10, (255, 0, 0),
                2, cv2.LINE_AA
            )

        # cv2.drawContours(frame1, contour, -1, (0, 0, 255), 2)
        # cv2.imshow("image", frame1)
        images.append(frame1)

        frame1 = frame2
        _, frame2 = video.read()

        if cv2.waitKey(40) == ord("q"):
            break

    # cv2.destroyAllWindows()
    video.release()

    # Writing
    time.sleep(1)

    create_video_by_images(video_with_contours_location, images, fps)

    return average_contour_point_locations, height, width


def test_compute_contour_point(height, width, contour_point):
    horizontal_angle, vertical_angle = compute_angles_by_contour_points(
        height,
        width,
        contour_point,
        max_horizontal_angle=31.1,
        max_vertical_angle=17.5
    )

    guide_vector = compute_guide_vector_by_angles(
        math.pi * horizontal_angle / 180,
        math.pi * vertical_angle / 180
    )

    horizontal_angle, vertical_angle = compute_angles_by_guide_vector(guide_vector)
    horizontal_angle = horizontal_angle * 180 / math.pi
    vertical_angle = vertical_angle * 180 / math.pi

    contour_point = compute_contour_points_by_angles(
        height,
        width,
        horizontal_angle,
        vertical_angle,
        45,
        40
    )

    return contour_point


def compute_average_contour_point_locations(contour_point_locations):
    x_coordinates = []
    y_coordinates = []
    for contour_point in contour_point_locations:
        x_coordinates.append(contour_point[0])
        y_coordinates.append(contour_point[1])

    return int(sum(x_coordinates) / len(x_coordinates)), \
        int(sum(y_coordinates) / len(y_coordinates))
