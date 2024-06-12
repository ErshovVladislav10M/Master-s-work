import math


def compute_angles_by_contour_points(
    height,
    width,
    contour_point,
    max_horizontal_angle,
    max_vertical_angle
):
    horizontal_angles = (contour_point[0] / width * 2 - 1) * max_horizontal_angle
    vertical_angles = (contour_point[1] / height * 2 - 1) * max_vertical_angle

    return horizontal_angles, vertical_angles


def compute_contour_points_by_angles(
    height,
    width,
    horizontal_angle,
    vertical_angle,
    max_horizontal_angle,
    max_vertical_angle
):
    x = (horizontal_angle / max_horizontal_angle + 1) * width / 2
    y = (vertical_angle / max_vertical_angle + 1) * height / 2
    contour_point = (x, y)

    return contour_point


def compute_guide_vector_by_angles(horizontal_angle: float, vertical_angle: float):
    """
    Angles in radians within [-math.pi, math.pi].
    :param horizontal_angle:
    :param vertical_angle:
    :return: [x, y, z]
    """
    guide_vector = [1, 0, 0]

    if math.isclose(math.pi / 2, horizontal_angle):
        guide_vector[0] = 0
        guide_vector[1] = 1
    elif math.isclose(-math.pi / 2, horizontal_angle):
        guide_vector[0] = 0
        guide_vector[1] = -1
    else:
        guide_vector[1] = math.tan(horizontal_angle)

    if math.isclose(math.pi / 2, vertical_angle):
        guide_vector[0] = 0
        guide_vector[2] = 1
    elif math.isclose(-math.pi / 2, vertical_angle):
        guide_vector[0] = 0
        guide_vector[2] = -1
    else:
        guide_vector[2] = math.tan(vertical_angle)

    return guide_vector


def compute_angles_by_guide_vector(guide_vector: list):
    horizontal_angle = 0.0
    vertical_angle = 0.0

    if math.isclose(guide_vector[0], 0):
        if guide_vector[2] > 0:
            horizontal_angle = math.pi / 2
        else:
            horizontal_angle = -math.pi / 2

        if math.isclose(guide_vector[2], 0):
            if guide_vector[1] > 0:
                vertical_angle = math.pi / 2
            else:
                vertical_angle = -math.pi / 2
        else:
            vertical_angle = math.atan(guide_vector[1] / guide_vector[2])
    else:
        horizontal_angle = math.atan(guide_vector[1] / guide_vector[0])
        vertical_angle = math.atan(guide_vector[2] / guide_vector[0])

    return horizontal_angle, vertical_angle
