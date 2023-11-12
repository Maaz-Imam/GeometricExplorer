import matplotlib.pyplot as plt
from math import atan2

def graham_scan(points):
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        return 1 if val > 0 else 2

    def compare(p1, p2):
        o = orientation(anchor, p1, p2)
        if o == 0:
            return -1 if distance(anchor, p1) < distance(anchor, p2) else 1
        return 1 if o == 2 else -1

    def distance(p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

    if len(points) < 3:
        print("Graham Scan requires at least three points.")
        return

    anchor = min(points, key=lambda p: (p[1], p[0]))

    sorted_points = sorted(points, key=lambda p: (atan2(p[1] - anchor[1], p[0] - anchor[0]), p))

    hull = [anchor, sorted_points[0], sorted_points[1]]

    for i in range(2, len(sorted_points)):
        while len(hull) > 1 and orientation(hull[-2], hull[-1], sorted_points[i]) != 2:
            hull.pop()
        hull.append(sorted_points[i])

    return hull

def plot_convex_hull(points, convex_hull):
    x_points, y_points = zip(*points)
    x_hull, y_hull = zip(*convex_hull)

    plt.figure(figsize=(8, 8))
    plt.scatter(x_points, y_points, color='blue', label='Points')
    plt.plot(x_hull + (x_hull[0],), y_hull + (y_hull[0],), color='red', linestyle='-', linewidth=2, label='Convex Hull')
    plt.title('Graham Scan Convex Hull')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage:
points = [(0, 3), (1, 1), (2, 2), (4, 4), (0, 0), (1, 2), (3, 1), (3.5, 0.5)]
convex_hull = graham_scan(points)

print("Convex Hull:", convex_hull)

plot_convex_hull(points, convex_hull)