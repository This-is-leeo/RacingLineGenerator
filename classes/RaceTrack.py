import pygame
import math
import os
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.interpolate import make_interp_spline
from settings import *

current_folder = os.path.dirname(os.path.abspath(__file__))

class Racetrack:
    def __init__(self):
        """Initialize an empty list of track guide_points."""
        self.guide_points = []
        self.centerline_spline = []
        self.draw_spline = False
        self.inner_line = []
        self.outer_line = []
        self.track_width = 20
        
    def add_point(self, x, y):
        """Add a new point to the racetrack."""
        self.guide_points.append((x, y))

    def modify_point(self, index, x, y):
        """Modify an existing point by index."""
        if 0 <= index < len(self.guide_points):
            self.guide_points[index] = (x, y)
        else:
            print(f"Invalid index: {index}")

    def remove_point(self, index):
        """Remove a point by index."""
        if index == -1 and len(self.guide_points) > 0:
            self.guide_points.pop(index)
        elif 0 <= index < len(self.guide_points):
            self.guide_points.pop(index)
        else:
            print(f"Invalid index: {index}")

    def draw(self, screen):
        """Visualize the racetrack."""
        top_text = "Left Click to add point, right click to delete last points"
        draw_text(top_text, FONT, BLACK, screen, (SCREEN_WIDTH) / 2, 30)
        if len(self.guide_points) > 1:
            pygame.draw.lines(screen, LIGHT_GRAY, True, self.guide_points, 3)
        else:
            draw_text("Draw More than 2 point to generate track", FONT, BLACK, screen, (SCREEN_WIDTH) / 2, 60)
        
        if self.draw_spline:
            if len(self.centerline_spline) < 3:
                self.draw_spline = False
            else:
                pygame.draw.lines(screen, BLUE, True, self.centerline_spline, 3)
                self.draw_key(screen)
                pygame.draw.lines(screen, RED, True, self.inner_line)
                pygame.draw.lines(screen, RED, True, self.outer_line)
                draw_text("'a' to decrease track width, 'd' to increase track width" , FONT, BLACK, screen, (SCREEN_WIDTH) / 2, 60)
                draw_text("current width: " + str(int(self.track_width / 4 - 1)), FONT, BLACK, screen, (SCREEN_WIDTH) / 2, 90)
        for point in self.guide_points:
            pygame.draw.circle(screen, RED, point, 4)

    def calculate_length(self):
        """Calculate the approximate length of the racetrack."""
        if len(self.guide_points) < 2:
            return 0
        length = 0
        for i in range(len(self.guide_points)):
            x1, y1 = self.guide_points[i]
            x2, y2 = self.guide_points[(i + 1) % len(self.guide_points)]
            length += math.hypot(x2 - x1, y2 - y1)
        return length  
    
    def save_track(self, file_name = 'test.txt'):
        with open(os.path.join(current_folder, file_name), 'w') as output:
            for i in range(len(self.guide_points)):
                output_text = str(self.guide_points[i][0]) + ' ' + str(self.guide_points[i][1]) + '\n'
                output.write(output_text)
    
    def generate_centerline_spline(self, num_points=500):
        """
        Generate a smooth centerline spline from the guide points.
        Args:
            num_points: Number of points to generate for the smooth centerline.
        Returns:
            List of points [(x, y)] along the smooth centerline.
        """
        if len(self.guide_points) < 3:
            return self.guide_points  # Not enough points for proper smoothing

        # Separate the guide points into x and y lists
        x = [p[0] for p in self.guide_points]
        y = [p[1] for p in self.guide_points]

        # Create periodic control points for a closed loop
        x = np.append(x, x[:1])  # Repeat the first three points
        y = np.append(y, y[:1])

        # Generate parameter values for the control points
        t = np.linspace(0, 1, len(x))
        t_smooth = np.linspace(0, 1, num_points)

        # Create a B-spline for x and y
        spline_x = make_interp_spline(t, x, k=3)  # Cubic B-spline
        spline_y = make_interp_spline(t, y, k=3)

        # Evaluate the spline at smooth parameter values
        smooth_x = spline_x(t_smooth)
        smooth_y = spline_y(t_smooth)

        # Return the smooth centerline points as a list of tuples
        return list(zip(smooth_x, smooth_y))
    
    def generate_boundaries(self):
        """Generate the inside (left) and outside (right) boundaries of the racetrack."""
        if len(self.centerline_spline) < 3:
            return [], []  # Not enough points to generate boundaries
        
        # Clear the old boundaries
        self.left_boundary = []
        self.right_boundary = []

        # Loop through the centerline points and calculate the left and right boundaries
        for i in range(1, len(self.centerline_spline)):
            p1 = self.centerline_spline[i - 1]
            p2 = self.centerline_spline[i]

            # Calculate the direction (tangent) vector of the segment
            dir_vector = np.array([p2[0] - p1[0], p2[1] - p1[1]])

            # Normalize the direction vector
            dir_vector /= np.linalg.norm(dir_vector)

            # Calculate the normal vector (perpendicular to the direction vector)
            normal_vector = np.array([-dir_vector[1], dir_vector[0]])

            # Offset the points for the left and right boundaries
            left_point = (p1[0] - normal_vector[0] * self.track_width / 2, 
                            p1[1] - normal_vector[1] * self.track_width / 2)
            right_point = (p1[0] + normal_vector[0] * self.track_width / 2, 
                            p1[1] + normal_vector[1] * self.track_width / 2)

            self.left_boundary.append(left_point)
            self.right_boundary.append(right_point)

        # Append the last point for closed loop (same as the first point)
        self.left_boundary.append(self.left_boundary[0])
        self.right_boundary.append(self.right_boundary[0])

        return self.left_boundary, self.right_boundary
    
    def draw_track_preview(self, screen, x, y, size):
        """
        Draw a preview of the track on the given screen at a specified position and size.
        
        Args:
            screen (pygame.Surface): The Pygame surface to draw on.
            x (int): The x-coordinate of the top-left corner of the preview.
            y (int): The y-coordinate of the top-left corner of the preview.
            size (int): The width and height of the preview area (square).
        """

        pygame.draw.rect(screen, PASTEL_ORANGE, (x, y, size, size))

    # Draw a border around the preview
        pygame.draw.rect(screen, BLACK, (x, y, size, size), 2)
        
        # Check if there are points to create a track
        if len(self.guide_points) == 0:
            font = pygame.font.SysFont(None, 20)
            text_surface = font.render("No Track Available", True, BLACK)
            text_rect = text_surface.get_rect(center=(x + size // 2, y + size // 2))
            screen.blit(text_surface, text_rect)
            return

        # Calculate scaling factor to fit the track within the given size
        if len(self.guide_points) > 1:
            min_x = min(p[0] for p in self.guide_points)
            min_y = min(p[1] for p in self.guide_points)
            max_x = max(p[0] for p in self.guide_points)
            max_y = max(p[1] for p in self.guide_points)
        else:
            min_x, max_x = 0, SCREEN_WIDTH
            min_y, max_y = 0, SCREEN_HEIGHT

        track_width = max_x - min_x
        track_height = max_y - min_y

        scale = size / max(track_width, track_height) * 0.8
        offset_x = x + size // 2 - (track_width * scale) // 2
        offset_y = y + size // 2 - (track_height * scale) // 2

        
        """
        #Draw the guide points
        if len(self.guide_points) > 1:
            scaled_points = [
                (int((p[0] - min_x) * scale + offset_x), int((p[1] - min_y) * scale + offset_y))
                for p in self.guide_points
            ]
            pygame.draw.lines(screen, LIGHT_GRAY, True, scaled_points, 3)
            for point in scaled_points:
                pygame.draw.circle(screen, RED, point, 5)
        """

        # Draw the centerline
        if self.draw_spline and len(self.centerline_spline) >= 3:
            scaled_spline = [
                (int((p[0] - min_x) * scale + offset_x), int((p[1] - min_y) * scale + offset_y))
                for p in self.centerline_spline
            ]
            pygame.draw.lines(screen, BLUE, True, scaled_spline, 3)

        # Draw the boundaries if generated
        if len(self.inner_line) > 0 and len(self.outer_line) > 0:
            scaled_inner_line = [
                (int((p[0] - min_x) * scale + offset_x), int((p[1] - min_y) * scale + offset_y))
                for p in self.inner_line
            ]
            scaled_outer_line = [
                (int((p[0] - min_x) * scale + offset_x), int((p[1] - min_y) * scale + offset_y))
                for p in self.outer_line
            ]
            pygame.draw.lines(screen, RED, True, scaled_inner_line, 2)
            pygame.draw.lines(screen, RED, True, scaled_outer_line, 2)

    @staticmethod

    def draw_key(screen):
        """Draw the key/legend in the top-right corner."""
        # Key background
        key_x = SCREEN_WIDTH - 220  # Position near the top-right
        key_y = 20
        key_width = 200
        key_height = 100
        pygame.draw.rect(screen, (50, 50, 50), (key_x, key_y, key_width, key_height))  # Dark gray background
        pygame.draw.rect(screen, (255, 255, 255), (key_x, key_y, key_width, key_height), 2)  # White border

        # Text and colors
        entries = [
            ("Blue: Center Line", BLUE),
            ("Light Gray: Guide Points", LIGHT_GRAY),
            ("Red: Outline", RED),
        ]

        # Draw each entry
        for i, (text, color) in enumerate(entries):
            # Draw the color swatch
            swatch_size = 20
            swatch_x = key_x + 10
            swatch_y = key_y + 10 + i * 25
            pygame.draw.rect(screen, color, (swatch_x, swatch_y, swatch_size, swatch_size))

            # Draw the text
            text_surface = SMALL_FONT.render(text, True, WHITE)  # White text
            screen.blit(text_surface, (swatch_x + swatch_size + 10, swatch_y))

def draw_text(text, font, color, surface, x, y):
    
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

