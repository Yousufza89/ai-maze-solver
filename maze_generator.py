import numpy as np
import random

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def generate(self):
        """Generate a random maze using depth-first search with recursive backtracking"""
        # Initialize maze with walls (0)
        maze = np.zeros((self.height, self.width), dtype=int)
        
        # Starting position (top-left)
        start_x, start_y = 0, 0
        
        # Mark start position as path
        maze[start_y][start_x] = 1
        
        # Recursive backtracking to generate maze
        self._generate_recursive(maze, start_x, start_y)
        
        # Ensure the goal (center) is accessible
        center_x, center_y = self.width // 2, self.height // 2
        maze[center_y][center_x] = 1
        
        # Make sure there's a path to the center by connecting it to a neighboring path
        connected = False
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = center_x + dx, center_y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if maze[ny][nx] == 1:
                    connected = True
                    break
        
        if not connected:
            # Connect to a random neighbor
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = center_x + dx, center_y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    maze[ny][nx] = 1
                    break
        
        # Add some random paths to make the maze more interesting
        self._add_random_paths(maze)
        
        return maze
    
    def _generate_recursive(self, maze, x, y):
        """Recursive function to generate maze using depth-first search"""
        # Define possible directions: right, down, left, up
        directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check if the new position is within maze bounds
            if 0 <= nx < self.width and 0 <= ny < self.height:
                # If the cell is unvisited (it's a wall)
                if maze[ny][nx] == 0:
                    # Mark the cell and the cell between as path
                    maze[ny][nx] = 1
                    maze[y + dy//2][x + dx//2] = 1
                    
                    # Continue from the new position
                    self._generate_recursive(maze, nx, ny)
    
    def _add_random_paths(self, maze):
        """Add some random paths to make the maze more interesting"""
        # Add random paths (about 10% of the total cells)
        num_random_paths = (self.width * self.height) // 10
        
        for _ in range(num_random_paths):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
            # Determine if there's at least one neighboring path
            has_path_neighbor = False
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and maze[ny][nx] == 1:
                    has_path_neighbor = True
                    break
            
            # If there's a neighboring path, make this cell a path too
            if has_path_neighbor:
                maze[y][x] = 1