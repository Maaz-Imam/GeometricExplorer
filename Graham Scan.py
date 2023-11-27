import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.animation as animation

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

def graham_scan_convex_hull(sorted_points,pivot):
    """
    Graham Scan Convex Hull Algorithm.
    """
    n = len(sorted_points)
    print("All Points: ",sorted_points)
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

#   2,4;3,3;2,5;1,1;6,7;8,5;3,4

    print("Convex Hull: ",convex_hull,"\n\n")
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
        hull_points = np.array(hull_frames[frame] + [hull_frames[frame][0]])  # Close the convex hull
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

    if user_input:
        # Parse user input into a list of tuples
        points = [tuple(map(float, point.split(','))) for point in user_input.split(';')]
        # Find the point with the lowest y-coordinate (and leftmost if ties)

        pivot = min(points, key=lambda x: (x[1], x[0]))
        print("Min Point: ",pivot)
        
        # Sort points based on polar angles with respect to the pivot
        sorted_points = sorted(points, key=lambda x: np.arctan2(x[1] - pivot[1], x[0] - pivot[0]))
        print("Sorted Points: ",sorted_points)

        # Calculate convex hull with step-by-step visualization
        hull_frames = [graham_scan_convex_hull(sorted_points[:i + 1],pivot) for i in range(len(sorted_points))]

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