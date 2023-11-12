import matplotlib.pyplot as plt
import numpy as np

def graham_scan(points):
    def cross_product(o, a, b):
        return (a[1] - o[1]) * (b[0] - o[0]) - (a[0] - o[0]) * (b[1] - o[1])

    def angle_cmp(p1, p2):
        return np.arctan2(p1[1] - anchor[1], p1[0] - anchor[0]) - np.arctan2(p2[1] - anchor[1], p2[0] - anchor[0])

    # Find the point with the lowest y-coordinate (and leftmost if ties)
    anchor = min(points, key=lambda p: (p[1], p[0]))

    # Sort the points based on the polar angle from the anchor point
    sorted_points = sorted(points, key=lambda p: angle_cmp(p, anchor))

    # Initialize the convex hull with the anchor and the first two sorted points
    hull = [anchor, sorted_points[0], sorted_points[1]]

    fig, ax = plt.subplots()

    for i in range(2, len(sorted_points)):
        # Pop the last point from the hull if a clockwise turn is encountered
        while len(hull) > 1 and cross_product(hull[-2], hull[-1], sorted_points[i]) <= 0:
            hull.pop()

        # Add the current point to the hull
        hull.append(sorted_points[i])

        # Plot current state
        ax.clear()
        ax.scatter(*zip(*points), c='black', marker='o', label='Points')
        ax.plot(*zip(*hull, hull[0]), color='r', linestyle='-', linewidth=2, label='Convex Hull')
        ax.legend()
        plt.title('Graham Scan - Step {}'.format(i + 1))
        plt.pause(0.5)  # Adjust the pause time as needed

    plt.show()

    return hull

# Example usage
if __name__ == "__main__":
    # Replace this list with your set of coordinates
    points = [(0, 0), (1, 1), (2, 2), (2, 0), (0, 2), (1, 0)]

    # Run Graham Scan algorithm
    convex_hull = graham_scan(points)
