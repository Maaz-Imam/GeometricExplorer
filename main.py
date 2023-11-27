import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.animation as animation
import time


def on_segment(p, q, r):
    # Check if point q lies on the line segment formed by points p and r
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

def distance(p1, p2, p3):
    # Sample distance function (you may need to adjust it based on your requirements)
    return abs((p3[0] - p1[0]) * (p2[1] - p1[1]) - (p3[1] - p1[1]) * (p2[0] - p1[0])) / ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**0.5

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0 # colinear
    return 1 if val > 0 else 2 #CW else CCW


def graham_scan_convex_hull(sorted_points):
    n = len(sorted_points)
    print("GS Sorted Points: ",sorted_points)
    # If there are less than 3 points, the convex hull is not defined
    if n < 3:
        return sorted_points
    
    # Initialize the convex hull with the first three points
    convex_hull = [sorted_points[0], sorted_points[1], sorted_points[2]]

    # Iterate through the sorted points to build the convex hull
    for i in range(3, n):
        while len(convex_hull) > 1 and orientation(convex_hull[-2], convex_hull[-1], sorted_points[i]) != 2:
            convex_hull.pop()
        convex_hull.append(sorted_points[i])

    return convex_hull


def brute_force_convex_hull(points):
    n = len(points)
    print("BF Points: ",points)
    if n < 3:
        return points

    hull_edges = []  # List to store potential convex hull edges
    bound_edges = []

    for i in range(n):
        print("\nNew vertex\n")
        for j in range(i + 1, n):
            # Form a line segment between points i and j
            current_edge = [points[i], points[j]]
            valid_edge = True
            for k in range(n):
                if k != i and k != j:
                    # Check if all other points lie on one side of the line segment
                    orient = orientation(points[i], points[j], points[k])
                    if orient == 0 and on_segment(points[i], points[k], points[j]):
                        # Points are collinear and on the segment, ignore
                        continue
                    elif orient != 0:
                        # Points are not collinear
                        if valid_edge:
                            valid_edge = False
                            if hull_edges:
                                # Append the current edge to the last edge in hull_edges
                                print("Before",hull_edges)
                                hull_edges[-1].extend(current_edge)
                                print("New Addition",current_edge)
                                # Append the joint edge to the hull
                                hull_edges.append(list(hull_edges[-1]))
                                print("After",hull_edges,"\n")
                                bound_edges.extend(current_edge)
                            else:
                                hull_edges.append(list(current_edge))
                                hull_edges.append(list(current_edge))
                                # print(current_edge,hull_edges,"\n")
                                bound_edges.extend(current_edge)
                        break
    
    # print(bound_edges)
    # hull_edges.append(bound_edges)
    print("BF Hull Edges: ",hull_edges)
    return hull_edges[:-1]
    # return list(bound_edges)


def jarvis_march_convex_hull(points,pivot):
    n = len(points)
    print("JM Points: ",points)
    # If there are fewer than 3 points, the convex hull is not defined
    if n < 3:
        return points

    # Initialize the convex hull with the pivot
    convex_hull = [pivot,points[1]]
    print("JM Convex Hull: ",convex_hull)

    while True:
        # Sort points based on polar angles with respect to the last point in the convex hull
        sorted_points = sorted(points, key=lambda x: np.arctan2(x[1] - convex_hull[-1][1], x[0] - convex_hull[-1][0]))
        print("JM Sorted Points: ",sorted_points)
        next_point = sorted_points[0]
        print("JM Next Point: ",next_point)
        for candidate in sorted_points[1:]:
            # Check if the candidate is not collinear with the last two points in the convex hull
            if orientation(convex_hull[-2], convex_hull[-1], candidate) != 0:
                next_point = candidate
                break
        
        print("JM CD Next Point: ",next_point)
        
        # If the next point is the pivot, the convex hull is complete
        if next_point == pivot:
            break

        convex_hull.append(next_point)
        print("JM Updated Convex Hull: ",convex_hull,"\n")
        time.sleep(10)

    return convex_hull


def quick_elimination_convex_hull(points):
    n = len(points)
    print("QE Points: ",points)
    # If there are fewer than 3 points, the convex hull is not defined
    if n < 3:
        return points
    
    def compare(p1, p2):
        o = orientation(points[0], p1, p2)
        if o == 0:
            return -1 if (p1[0] + p1[1]) < (p2[0] + p2[1]) else 1
        return -1 if o == 2 else 1

    # Sort points based on polar angle with respect to the first point
    points.sort(key=lambda p: (p[1], p[0]))

    # Initialize the convex hull with the first two points
    convex_hull = [points[0], points[1]]

    # Eliminate points inside the convex hull
    for i in range(2, len(points)):
        while len(convex_hull) > 1 and orientation(convex_hull[-2], convex_hull[-1], points[i]) != 2:
            convex_hull.pop()
        convex_hull.append(points[i])

    print(convex_hull)
    return convex_hull


def visualize_animation(points, hull_frames):
    fig, ax = plt.subplots()

    # Find min and max coordinates for fixed axes limits
    min_x, min_y = min(p[0] for p in points), min(p[1] for p in points)
    max_x, max_y = max(p[0] for p in points), max(p[1] for p in points)

    def update(frame):
        ax.clear()

        # Draw points
        ax.plot(*zip(*points), 'o', color='blue', label='Points')

        # Draw lines forming the convex hull up to the current frame
        hull_points = np.array(hull_frames[frame] + [hull_frames[frame][0]])
        ax.plot(hull_points[:, 0], hull_points[:, 1], color='red', label='Convex Hull')

        # Set fixed axes limits
        ax.set_xlim(min_x - 1, max_x + 1)
        ax.set_ylim(min_y - 1, max_y + 1)

        ax.legend()

    ani = animation.FuncAnimation(fig, update, frames=len(hull_frames), repeat=False)
    return fig, ani

def main():
    st.title("Step-by-Step Convex Hull Visualization")

    # Get user input for points
    user_input = st.text_input("Enter points (e.g., '2,4;1,1;5,2'):")
    # user_input = "2,4;3,3;2,5;1,1"

    if user_input:
        # Parse user input into a list of tuples
        points = [tuple(map(float, point.split(','))) for point in user_input.split(';')]
        #   2,4;3,3;2,5;1,1;6,7;8,5;3,4

        hull_frames = []

        # Choose your Algorithm
        st.markdown('Choose your algorithm for Convex Hull solution of the above selected points: ')

        if(st.button("Graham Scan")):
            # Calculate convex hull with step-by-step visualization for Graham Scan
            pivot = min(points, key=lambda x: (x[1], x[0]))
            print("\n\nGS Min Point: ",pivot)
            
            # Sort points based on polar angles with respect to the pivot
            sorted_points = sorted(points, key=lambda x: np.arctan2(x[1] - pivot[1], x[0] - pivot[0]))
            print("GS Sorted Points: ",sorted_points)

            hull_frames = [graham_scan_convex_hull(sorted_points[:i + 1]) for i in range(len(sorted_points))]
            print("GS Ans: ",hull_frames)

        if(st.button("Brute Force")):
            # Calculate convex hull with step-by-step visualization for Brute Force
            print("\n\n")

            hull_frames = brute_force_convex_hull(points)
            print("BF Ans: ",hull_frames)

        if(st.button("Jarvis March")):
            # Calculate convex hull with step-by-step visualization for Jarvis March

            # Sort points by x-coordinate
            # sorted_points = sorted(points, key=lambda x: x[0])

            pivot = min(points, key=lambda x: (x[1], x[0]))
            print("\n\nJM Min Point: ",pivot)

            # Sort points w.r.t Pivot
            sorted_points = sorted(points, key=lambda x: np.arctan2(x[1] - pivot[1], x[0] - pivot[0]))

            hull_frames = [jarvis_march_convex_hull(sorted_points[:i + 1],pivot) for i in range(len(points))]
            print("JM Ans: ",hull_frames)

        if(st.button("Quick Elimination")):
            # Calculate convex hull with step-by-step visualization for Quick Elimination
            print("\n\n")

            hull_frames = quick_elimination_convex_hull(points)
            print("QE Ans: ",hull_frames)

        if hull_frames:
            # Visualize the convex hull animation
            fig, ani = visualize_animation(points, hull_frames)

            # Save the animation as a GIF
            gif_path = 'convex_hull_animation.gif'
            ani.save(gif_path, writer='pillow', fps=1)

            # Display the GIF using Streamlit
            st.image(gif_path, use_column_width=True)

            # Optionally, display the convex hull result
            st.markdown(f"**Convex Hull Result:** {hull_frames[-1]}")

if __name__ == "__main__":
    main()