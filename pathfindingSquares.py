import pygame
import numpy as np
import heapq

# Initialize Pygame
pygame.init()

# Window settings
width, height = 420, 315
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("LiDAR Pathfinding Simulation with Heatmap")
clock = pygame.time.Clock()  # Initialize a clock for controlling the frame rate

# Define the frame rate and the steps per second for drawing the path
frame_rate = 60
steps_per_second = 10
frame_counter = 0  # Counter to control when to move to the next step in the path

# Circle positions and radii
heatmap_circle_pos = (width - 50, 50)  # Near the top-right corner
pathfind_circle_pos = (width - 50, 100)  # A little below the heatmap circle
circle_radius = 20

# Colors for the circles
heatmap_circle_color = (100, 100, 255)  # Blueish
pathfind_circle_color = (255, 100, 100)  # Redish


# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)  # Start point color
blue = (0, 0, 255)   # End point color
yellow = (255, 255, 0)  # Obstacle color

path = []  # Global path variable
current_step = 0  # Tracks the current step in the path
drawing_path = False  # Flag to indicate when we are drawing the path


# Grid settings
cell_size = 20
grid_width = width // cell_size
grid_height = height // cell_size

# Create a 2D numpy array for the grid and heatmap
grid = np.zeros((grid_height, grid_width))
heatmap = np.zeros((grid_height, grid_width))  # Separate heatmap for visualization

def heuristic(a, b):
    """Calculate the Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(pos):
    """Returns valid neighbors of a cell, considering grid boundaries and obstacles."""
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4-way movement
    for d in directions:
        nx, ny = pos[0] + d[0], pos[1] + d[1]
        if 0 <= nx < grid_width and 0 <= ny < grid_height and grid[ny][nx] != 1:
            neighbors.append((nx, ny))
    return neighbors

def a_star_search(start, goal):
    """Implements the A* search algorithm to find a path from start to goal."""
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not len(frontier) == 0:
        current = heapq.heappop(frontier)[1]

        if current == goal:
            break

        for next in get_neighbors(current):
            new_cost = cost_so_far[current] + calculate_cost(current, next, end_pos)  # Use the new cost function
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current

    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    """Reconstructs the path from start to goal given the came_from map."""
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)  # Optional
    path.reverse()  # Optional
    return path

# Add the rest of your Pygame initialization and loop here, including the draw_grid and update_display functions.
def draw_grid():
    """Draws the grid lines on the window."""
    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(window, white, rect, 1)

def generate_heatmap():
    """Generates the heatmap based on the distance to the nearest obstacle for each cell."""
    for row in range(grid_height):
        for col in range(grid_width):
            # Skip if it's an obstacle
            if grid[row][col] == 1:
                continue
            min_dist = float('inf')
            # Check distance from all obstacles
            for oy in range(grid_height):
                for ox in range(grid_width):
                    if grid[oy][ox] == 1:
                        dist = abs(oy - row) + abs(ox - col)  # Manhattan distance
                        if dist < min_dist:
                            min_dist = dist
            heatmap[row][col] = min_dist * 10  # Amplify the distance for better visibility

def calculate_cost(current, next, goal):
    """Calculate cost from current to next node, including penalties for being close to obstacles."""
    base_cost = 1  # Base cost for moving from one cell to another
    penalty = 0  # Penalty for being close to obstacles

    # Check proximity to nearest obstacle and add penalty
    for dy in range(-1, 2):  # Check adjacent cells including diagonally
        for dx in range(-1, 2):
            nx, ny = next[0] + dx, next[1] + dy
            if 0 <= nx < grid_width and 0 <= ny < grid_height and grid[ny][nx] == 1:
                penalty += 10  # High penalty for being close to obstacles

    return base_cost + penalty

def update_display():
    """Updates the display with the current state of the grid and heatmap."""
    window.fill(black)
    for row in range(grid_height):
        for col in range(grid_width):
            if grid[row][col] == 1:  # Obstacle
                pygame.draw.rect(window, yellow, (col * cell_size, row * cell_size, cell_size, cell_size))
            elif grid[row][col] == 2:  # Start point
                pygame.draw.rect(window, green, (col * cell_size, row * cell_size, cell_size, cell_size))
            elif grid[row][col] == 3:  # End point
                pygame.draw.rect(window, blue, (col * cell_size, row * cell_size, cell_size, cell_size))
            elif grid[row][col] == 4:  # Path
                pygame.draw.rect(window, (128, 128, 128), (col * cell_size, row * cell_size, cell_size, cell_size))  # Use a distinct color for the path

            else:
                # Calculate color based on heatmap value
                intensity = min(heatmap[row][col], 255)  # Ensure the value is within the RGB range
                color = (255, 255 - intensity, 255 - intensity)  # Green to Red transition
                if intensity > 0:
                    pygame.draw.rect(window, color, (col * cell_size, row * cell_size, cell_size, cell_size))
    draw_grid()
    pygame.display.update()

start_pos = None
end_pos = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            cell_x, cell_y = pos[0] // cell_size, pos[1] // cell_size
            
            if cell_x < grid_width and cell_y < grid_height:
                if not start_pos:
                    start_pos = (cell_x, cell_y)
                    grid[cell_y][cell_x] = 2
                elif not end_pos and (cell_x, cell_y) != start_pos:
                    end_pos = (cell_x, cell_y)
                    grid[cell_y][cell_x] = 3
                else:
                    grid[cell_y][cell_x] = 1

    # Check if start and end positions are set to automatically generate heatmap and pathfinding
    if start_pos and end_pos:
        generate_heatmap()  # Automatically generate the heatmap
        
        # Automatically generate the path if not already drawing or just finished drawing
        if not drawing_path or current_step >= len(path):
            came_from, cost_so_far = a_star_search(start_pos, end_pos)
            path = reconstruct_path(came_from, start_pos, end_pos)
            grid[grid == 4] = 0  # Clear previous path
            for step in path:
                if step != start_pos and step != end_pos:
                    grid[step[1]][step[0]] = 4  # Mark cells in the path

    update_display()
    clock.tick(frame_rate)
