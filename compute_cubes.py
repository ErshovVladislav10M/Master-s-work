import numpy as np


def compute_cubes(coord, guide_vector, cube_side, num_cubes):
    np_coord = np.array(coord)
    np_guide_vector = np.array(guide_vector)

    cubes = set()
    for i in range(num_cubes):
        x_t = (i * cube_side - np_coord[0]) / np_guide_vector[0]
        coord_in_x_cube = np_coord + np_guide_vector * x_t
        x_cube = coord_in_x_cube // cube_side
        if 0 <= x_cube[0] <= num_cubes and 0 <= x_cube[1] <= num_cubes and 0 <= x_cube[2] <= num_cubes:
            cubes.add(tuple(x_cube))
            # add neighboring cube
            cubes.add(tuple(x_cube - np.array([1, 0, 0])))

        y_t = (i * cube_side - coord[1]) / guide_vector[1]
        coord_in_y_cube = np_coord + np_guide_vector * y_t
        y_cube = coord_in_y_cube // cube_side
        if 0 <= y_cube[0] <= num_cubes and 0 <= y_cube[1] <= num_cubes and 0 <= y_cube[2] <= num_cubes:
            cubes.add(tuple(y_cube))
            # add neighboring cube
            cubes.add(tuple(y_cube - np.array([0, 1, 0])))

        z_t = (i * cube_side - coord[2]) / guide_vector[2]
        coord_in_z_cube = np_coord + np_guide_vector * z_t
        z_cube = coord_in_z_cube // cube_side
        if 0 <= z_cube[0] <= num_cubes and 0 <= z_cube[1] <= num_cubes and 0 <= z_cube[2] <= num_cubes:
            cubes.add(tuple(z_cube))
            # add neighboring cube
            cubes.add(tuple(z_cube - np.array([0, 0, 1])))

    return cubes
