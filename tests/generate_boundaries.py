import numpy as np
import matplotlib.pyplot as plt

# Example list of center guide points (x, y)
center_points = np.array([
    [0, 0], [1, 2], [3, 3], [5, 5], [7, 8], [10, 10]
])

# Define track width (distance from the centerline to the edge)
track_width = 2  # adjust this as needed

# Function to generate the track boundaries
def generate_track_boundaries(center_points, width):
    left_boundaries = []
    right_boundaries = []
    
    # Loop through the center points and generate left and right edges
    for i in range(1, len(center_points) - 1):
        # Get the current, previous, and next points
        prev_point, curr_point, next_point = center_points[i - 1], center_points[i], center_points[i + 1]
        
        # Calculate the direction of the centerline
        dir_vector = np.array(curr_point - prev_point, dtype=np.float64)  # Convert to float64
        dir_vector_next = np.array(next_point - curr_point, dtype=np.float64)  # Convert to float64
        
        # Normalize direction vectors
        dir_vector /= np.linalg.norm(dir_vector)
        dir_vector_next /= np.linalg.norm(dir_vector_next)
        
        # Compute perpendicular vectors (normal to the centerline)
        left_normal = np.array([-dir_vector[1], dir_vector[0]]) * width
        right_normal = np.array([dir_vector[1], -dir_vector[0]]) * width
        
        # Left and right boundary points
        left_boundaries.append(curr_point + left_normal)
        right_boundaries.append(curr_point + right_normal)
    
    return np.array(left_boundaries), np.array(right_boundaries)

# Generate the track boundaries
left_boundaries, right_boundaries = generate_track_boundaries(center_points, track_width)

# Plot the centerline and track boundaries
plt.plot(center_points[:, 0], center_points[:, 1], label="Centerline", color='blue')
plt.plot(left_boundaries[:, 0], left_boundaries[:, 1], label="Left Boundary", color='green')
plt.plot(right_boundaries[:, 0], right_boundaries[:, 1], label="Right Boundary", color='red')

plt.legend()
plt.title("Track Generation from Center Guide")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.show()
