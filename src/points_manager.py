class PointsManager:
    def __init__(self, max_distance_between_points):
        self._max_distance_between_points = max_distance_between_points
        self._groups = []

    def append(self, x: int, y: int) -> None:
        closest_group = None
        min_distance = None
        for group in self._groups:
            average = group.get_average_point()
            distance = self.compute_distance_between_points(average, (x, y))
            if distance < self._max_distance_between_points:
                if not min_distance or distance < min_distance:
                    min_distance = distance
                    closest_group = group

        if not closest_group:
            new_group = PointsManager._Group()
            new_group.append(x, y)
            self._groups.append(new_group)
        else:
            closest_group.append(x, y)

    def get_average_points(self) -> list[tuple]:
        average_points = []
        for group in self._groups:
            average_points.append(group.get_average_point())

        return average_points

    class _Group:
        def __init__(self):
            self.points = []
            self.average_point = None

        def append(self, x, y) -> None:
            self.points.append((x, y))
            self.average_point = None

        def get_average_point(self) -> tuple[int, int]:
            if not self.average_point:
                self.average_point = PointsManager.compute_average_point_in_group(self.points)

            return self.average_point

    @staticmethod
    def compute_distance_between_points(point_1: tuple[int, int], point_2: tuple[int, int]) -> int:
        return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])

    @staticmethod
    def compute_average_point_in_group(points: list) -> tuple[int, int]:
        if len(points) == 0:
            raise ValueError("Points must be not empty")

        x_coordinates = []
        y_coordinates = []
        for point in points:
            x_coordinates.append(point[0])
            y_coordinates.append(point[1])

        return int(sum(x_coordinates) / len(x_coordinates)), \
            int(sum(y_coordinates) / len(y_coordinates))
