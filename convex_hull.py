import math


def orientation(p, q, r):
    """
    Utility function to find the orientation of three points (p, q, r).
    Returns:
    0 - Collinear
    1 - Clockwise
    2 - Counterclockwise
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    return 1 if val > 0 else 2


def brute_force_convex_hull(points):
    """
    Brute Force Convex Hull Algorithm.
    """
    n = len(points)
    hull = []

    for i in range(n):
        for j in range(i + 1, n):
            valid = True
            for k in range(n):
                if k != i and k != j:
                    if orientation(points[i], points[j], points[k]) == 0:
                        valid = False
                        break
            if valid:
                hull.append(points[i])
                hull.append(points[j])

    # Remove duplicate points
    hull = list(set(hull))
    return hull


def jarvis_march_convex_hull(points):
    """
    Jarvis March (Gift Wrapping) Convex Hull Algorithm.
    """
    n = len(points)
    hull = []

    # Find the leftmost point
    leftmost = min(points, key=lambda x: x[0])
    current_point = leftmost
    next_point = None

    while next_point != leftmost:
        hull.append(current_point)
        next_point = points[0]
        for i in range(1, n):
            if next_point == current_point or orientation(current_point, points[i], next_point) == 2:
                next_point = points[i]

        current_point = next_point

    return hull


def graham_scan_convex_hull(points):
    """
    Graham Scan Convex Hull Algorithm.
    """
    n = len(points)

    def compare(p1, p2):
        angle1 = math.atan2(p1[1] - points[0][1], p1[0] - points[0][0])
        angle2 = math.atan2(p2[1] - points[0][1], p2[0] - points[0][0])

        if angle1 < angle2:
            return -1
        elif angle1 > angle2:
            return 1
        else:
            return 0

    points.sort(key=lambda x: (x[1], x[0]))
    points = [points[0]] + sorted(points[1:], key=lambda x: math.atan2(x[1] - points[0][1], x[0] - points[0][0]))

    stack = []
    for i in range(n):
        while len(stack) > 1 and orientation(stack[-2], stack[-1], points[i]) != 2:
            stack.pop()
        stack.append(points[i])

    return stack


def quick_elimination_convex_hull(points):
    """
    Quick Elimination Convex Hull Algorithm.
    """
    def find_tangent(point, hull, upper):
        tangent_index = None
        n = len(hull)

        for i in range(n):
            if tangent_index is None or orientation(point, hull[i], hull[tangent_index]) == upper:
                tangent_index = i

        return tangent_index

    n = len(points)

    # Sort points by x-coordinate
    points.sort(key=lambda x: x[0])

    # Initialize upper and lower hulls
    upper_hull = [points[0], points[1]]
    lower_hull = [points[0], points[1]]

    # Build upper and lower hulls
    for i in range(2, n):
        upper_tangent = find_tangent(points[i], upper_hull, 2)
        lower_tangent = find_tangent(points[i], lower_hull, 1)

        upper_hull = upper_hull[:upper_tangent + 1] + [points[i]] + upper_hull[upper_tangent + 1:]
        lower_hull = lower_hull[:lower_tangent + 1] + [points[i]] + lower_hull[lower_tangent + 1:]

    # Concatenate upper and lower hulls to form the convex hull
    convex_hull = upper_hull + lower_hull[1:-1]
    return convex_hull


# Example usage:
points = [(0, 0), (1, 1), (2, 2), (3, 1), (2, 0), (0, 2), (1, -1)]
print("Brute Force Convex Hull:", brute_force_convex_hull(points))
print("Jarvis March Convex Hull:", jarvis_march_convex_hull(points))
print("Graham Scan Convex Hull:", graham_scan_convex_hull(points))
print("Quick Elimination Convex Hull:", quick_elimination_convex_hull(points))