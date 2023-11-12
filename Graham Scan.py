import numpy as np

def graham_scan(points):
    def cross_product(o, a, b):
        return (a[1] - o[1]) * (b[0] - o[0]) - (a[0] - o[0]) * (b[1] - o[1])

    def angle_cmp(p1, p2):
        return np.arctan2(p1[1] - anchor[1], p1[0] - anchor[0]) - np.arctan2(p2[1] - anchor[1], p2[0] - anchor[0])

    anchor = min(points, key=lambda p: (p[1], p[0]))

    sorted_points = sorted(points, key=lambda p: angle_cmp(p, anchor))

    hull = [anchor, sorted_points[0], sorted_points[1]]

        current_point = sorted_points[i]
        hull.append(current_point)
        while len(hull) > 1 and cross_product(hull[-2], hull[-1], current_point) <= 0:
            hull.pop()


    return hull

# Example usage
if __name__ == "__main__":
    points = [(0, 0), (1, 1), (2, 2), (2, 0), (0, 2), (1, 0)]
    convex_hull = graham_scan(points)