import pygame
import sys
import numpy as np
import random
from maze_generator import MazeGenerator
from ai_controller import AIController
from player import Player
from ui_elements import Button, MenuSystem, Legend

class MindMazeGame:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.font.init()
        
        # Game constants
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.CELL_SIZE = 40
        self.MAZE_WIDTH = 15
        self.MAZE_HEIGHT = 15
        self.MAZE_OFFSET_X = (self.SCREEN_WIDTH - self.MAZE_WIDTH * self.CELL_SIZE) // 2
        self.MAZE_OFFSET_Y = (self.SCREEN_HEIGHT - self.MAZE_HEIGHT * self.CELL_SIZE) // 2
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (128, 0, 128)
        
        # Game state
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("MindMaze: AI-Powered Labyrinth")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 20)
        
        # Game components
        self.maze_generator = MazeGenerator(self.MAZE_WIDTH, self.MAZE_HEIGHT)
        self.ai_controller = AIController(self.MAZE_WIDTH, self.MAZE_HEIGHT)
        
        # Game state variables
        self.game_state = "menu"  # "menu", "playing", "game_over"
        self.turn_count = 0
        self.ai_modify_frequency = 3  # AI modifies maze every 3 turns
        self.hints_remaining = 3
        
        # Menu system
        self.menu = MenuSystem(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
        # Legend for color meanings
        self.legend = Legend(self.SCREEN_WIDTH, 10, self.CELL_SIZE)
        
        # Initialize the game
        self.initialize_game()

    def initialize_game(self):
        # Generate initial maze
        self.maze = self.maze_generator.generate()
        
        # Set start position (top-left) and goal position (center)
        self.start_pos = (0, 0)
        self.goal_pos = (self.MAZE_WIDTH // 2, self.MAZE_HEIGHT // 2)
        
        # Create player and place at start position
        self.player = Player(self.start_pos[0], self.start_pos[1])
        
        # Reset turn count and hints
        self.turn_count = 0
        self.hints_remaining = 3
        
        # Special tiles
        self.traps = []
        self.teleporters = []
        self.shortcuts = []
        
        # Place initial traps and teleporters
        self.place_special_tiles()
        
        # Initialize AI with the maze
        self.ai_controller = AIController(self.MAZE_WIDTH, self.MAZE_HEIGHT)
        self.ai_controller.set_maze(self.maze)
        self.ai_controller.set_player_position(self.player.x, self.player.y)

    def place_special_tiles(self):
        # Clear existing special tiles
        self.traps = []
        self.teleporters = []
        self.shortcuts = []
        
        # Place traps (3 traps)
        for _ in range(3):
            x, y = self.get_random_valid_position()
            self.traps.append((x, y))
        
        # Place teleporters (2 pairs)
        for _ in range(2):
            x1, y1 = self.get_random_valid_position()
            x2, y2 = self.get_random_valid_position()
            self.teleporters.append(((x1, y1), (x2, y2)))
        
        # Place shortcuts (2)
        for _ in range(2):
            x, y = self.get_random_valid_position()
            self.shortcuts.append((x, y))

    def get_random_valid_position(self):
        while True:
            x = random.randint(0, self.MAZE_WIDTH - 1)
            y = random.randint(0, self.MAZE_HEIGHT - 1)
            
            # Check if position is not start, goal, or another special tile
            if ((x, y) != self.start_pos and 
                (x, y) != self.goal_pos and 
                (x, y) not in self.traps and
                not any((x, y) in pair for pair in self.teleporters) and
                (x, y) not in self.shortcuts and
                (x, y) != (self.player.x, self.player.y)):
                return x, y

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if self.game_state == "menu":
                action = self.menu.handle_event(event)
                if action == "start_game":
                    self.game_state = "playing"
                elif action == "quit":
                    pygame.quit()
                    sys.exit()
            
            elif self.game_state == "playing":
                if event.type == pygame.KEYDOWN:
                    self.handle_player_movement(event.key)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Use hint if clicked on hint button
                    hint_rect = pygame.Rect(10, self.SCREEN_HEIGHT - 40, 100, 30)
                    if hint_rect.collidepoint(event.pos) and self.hints_remaining > 0:
                        self.use_hint()
            
            elif self.game_state == "game_over":
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    # Reset the game and go back to the menu when game over screen is clicked
                    self.initialize_game()
                    self.game_state = "menu"

    def handle_player_movement(self, key):
        # Store previous position
        prev_x, prev_y = self.player.x, self.player.y
        
        # Handle movement keys
        if key == pygame.K_UP and self.can_move(self.player.x, self.player.y - 1):
            self.player.move(0, -1)
        elif key == pygame.K_DOWN and self.can_move(self.player.x, self.player.y + 1):
            self.player.move(0, 1)
        elif key == pygame.K_LEFT and self.can_move(self.player.x - 1, self.player.y):
            self.player.move(-1, 0)
        elif key == pygame.K_RIGHT and self.can_move(self.player.x + 1, self.player.y):
            self.player.move(1, 0)
        
        # Check if player actually moved
        if (prev_x, prev_y) != (self.player.x, self.player.y):
            self.turn_count += 1
            
            # Check for teleporter
            self.check_teleporter()
            
            # Check for trap
            if self.check_trap():
                # Player hit trap, move back
                self.player.x, self.player.y = prev_x, prev_y
            
            # Check for shortcut
            self.check_shortcut()
            
            # Check for goal
            if (self.player.x, self.player.y) == self.goal_pos:
                self.game_state = "game_over"
            
            # Update AI with new player position
            self.ai_controller.set_player_position(self.player.x, self.player.y)
            
            # AI modifies maze every few turns
            if self.turn_count % self.ai_modify_frequency == 0:
                self.ai_modify_maze()

    def can_move(self, x, y):
        # Check if position is within maze bounds
        if x < 0 or x >= self.MAZE_WIDTH or y < 0 or y >= self.MAZE_HEIGHT:
            return False
        
        # Check if there's a path in the maze
        return self.maze[y][x] == 1  # 1 represents a path

    def check_teleporter(self):
        for teleporter_pair in self.teleporters:
            if (self.player.x, self.player.y) == teleporter_pair[0]:
                self.player.x, self.player.y = teleporter_pair[1]
                break
            elif (self.player.x, self.player.y) == teleporter_pair[1]:
                self.player.x, self.player.y = teleporter_pair[0]
                break

    def check_trap(self):
        return (self.player.x, self.player.y) in self.traps

    def check_shortcut(self):
        if (self.player.x, self.player.y) in self.shortcuts:
            # Move player closer to goal
            goal_x, goal_y = self.goal_pos
            dx = goal_x - self.player.x
            dy = goal_y - self.player.y
            
            # Move in the direction of the goal by up to 3 cells
            steps = min(3, abs(dx) + abs(dy))
            
            for _ in range(steps):
                # Determine direction with highest priority
                if abs(dx) > abs(dy):
                    # Move horizontally
                    step_x = 1 if dx > 0 else -1
                    if self.can_move(self.player.x + step_x, self.player.y):
                        self.player.x += step_x
                        dx -= step_x
                    else:
                        # Try vertical if horizontal is blocked
                        step_y = 1 if dy > 0 else -1
                        if self.can_move(self.player.x, self.player.y + step_y):
                            self.player.y += step_y
                            dy -= step_y
                        else:
                            break  # If both directions are blocked, stop moving
                else:
                    # Move vertically
                    step_y = 1 if dy > 0 else -1
                    if self.can_move(self.player.x, self.player.y + step_y):
                        self.player.y += step_y
                        dy -= step_y
                    else:
                        # Try horizontal if vertical is blocked
                        step_x = 1 if dx > 0 else -1
                        if self.can_move(self.player.x + step_x, self.player.y):
                            self.player.x += step_x
                            dx -= step_x
                        else:
                            break

    def ai_modify_maze(self):
        # Let AI modify the maze
        modifications = self.ai_controller.get_maze_modifications()
        
        # Apply modifications
        for x, y, value in modifications:
            if 0 <= x < self.MAZE_WIDTH and 0 <= y < self.MAZE_HEIGHT:
                # Don't modify start, goal, or player position
                if ((x, y) != self.start_pos and 
                    (x, y) != self.goal_pos and 
                    (x, y) != (self.player.x, self.player.y)):
                    self.maze[y][x] = value
        
        # Ensure there's always a path to the goal
        self.ensure_path_to_goal()
        
        # Update special tiles
        self.update_special_tiles()

    def ensure_path_to_goal(self):
        # This is a simplified version - in a real implementation,
        # you'd want to use a pathfinding algorithm to ensure
        # there's a valid path from player to goal
        # For now, we'll just make sure all cells have at least one neighbor
        for y in range(self.MAZE_HEIGHT):
            for x in range(self.MAZE_WIDTH):
                if self.maze[y][x] == 1:  # If it's a path
                    # Count accessible neighbors
                    neighbors = 0
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < self.MAZE_WIDTH and 
                            0 <= ny < self.MAZE_HEIGHT and 
                            self.maze[ny][nx] == 1):
                            neighbors += 1
                    
                    # If isolated, connect to a neighbor
                    if neighbors == 0:
                        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                            nx, ny = x + dx, y + dy
                            if (0 <= nx < self.MAZE_WIDTH and 
                                0 <= ny < self.MAZE_HEIGHT):
                                self.maze[ny][nx] = 1
                                break

    def update_special_tiles(self):
        # Occasionally move traps based on player position
        if random.random() < 0.3:  # 30% chance to move traps
            for i in range(len(self.traps)):
                if random.random() < 0.5:  # 50% chance for each trap
                    self.traps[i] = self.get_random_valid_position()
        
        # Occasionally move teleporters
        if random.random() < 0.2:  # 20% chance to move teleporters
            for i in range(len(self.teleporters)):
                if random.random() < 0.3:  # 30% chance for each teleporter pair
                    self.teleporters[i] = (
                        self.get_random_valid_position(),
                        self.get_random_valid_position()
                    )
        
        # Occasionally move shortcuts
        if random.random() < 0.25:  # 25% chance to move shortcuts
            for i in range(len(self.shortcuts)):
                if random.random() < 0.4:  # 40% chance for each shortcut
                    self.shortcuts[i] = self.get_random_valid_position()

    def use_hint(self):
        if self.hints_remaining > 0:
            self.hints_remaining -= 1
            # Get AI predictions for next maze modification
            predictions = self.ai_controller.get_modification_prediction()
            # Store predictions for display
            self.current_hint = predictions
            self.hint_display_time = pygame.time.get_ticks()

    def draw(self):
        self.screen.fill(self.BLACK)
        
        if self.game_state == "menu":
            self.menu.draw(self.screen)
            
            # Draw the legend on the menu screen too
            self.legend.draw(self.screen, [
                ("White", self.WHITE, "Path"),
                ("Black", self.BLACK, "Wall"),
                ("Green", self.GREEN, "Goal"),
                ("Red", self.RED, "Trap"),
                ("Blue", self.BLUE, "Teleporter"),
                ("Yellow", self.YELLOW, "Shortcut"),
                ("Purple", self.PURPLE, "Player")
            ])
        
        elif self.game_state == "playing":
            self.draw_maze()
            self.draw_player()
            self.draw_ui()
            
            # Draw legend during gameplay
            self.legend.draw(self.screen, [
                ("White", self.WHITE, "Path"),
                ("Black", self.BLACK, "Wall"),
                ("Green", self.GREEN, "Goal"),
                ("Red", self.RED, "Trap"),
                ("Blue", self.BLUE, "Teleporter"),
                ("Yellow", self.YELLOW, "Shortcut"),
                ("Purple", self.PURPLE, "Player")
            ])
            
            # Draw hint if active
            if hasattr(self, 'current_hint') and hasattr(self, 'hint_display_time'):
                if pygame.time.get_ticks() - self.hint_display_time < 5000:  # Display hint for 5 seconds
                    self.draw_hint()
        
        elif self.game_state == "game_over":
            self.draw_game_over()
        
        pygame.display.flip()

    def draw_maze(self):
        for y in range(self.MAZE_HEIGHT):
            for x in range(self.MAZE_WIDTH):
                rect = pygame.Rect(
                    self.MAZE_OFFSET_X + x * self.CELL_SIZE,
                    self.MAZE_OFFSET_Y + y * self.CELL_SIZE,
                    self.CELL_SIZE,
                    self.CELL_SIZE
                )
                
                # Draw path or wall
                color = self.WHITE if self.maze[y][x] == 1 else self.BLACK
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.BLACK, rect, 1)  # Border
                
                # Draw goal
                if (x, y) == self.goal_pos:
                    pygame.draw.rect(self.screen, self.GREEN, rect)
                    pygame.draw.rect(self.screen, self.BLACK, rect, 1)
                
                # Draw special tiles
                if (x, y) in self.traps:
                    pygame.draw.rect(self.screen, self.RED, rect)
                    pygame.draw.rect(self.screen, self.BLACK, rect, 1)
                
                for teleporter_pair in self.teleporters:
                    if (x, y) in teleporter_pair:
                        pygame.draw.rect(self.screen, self.BLUE, rect)
                        pygame.draw.rect(self.screen, self.BLACK, rect, 1)
                
                if (x, y) in self.shortcuts:
                    pygame.draw.rect(self.screen, self.YELLOW, rect)
                    pygame.draw.rect(self.screen, self.BLACK, rect, 1)

    def draw_player(self):
        rect = pygame.Rect(
            self.MAZE_OFFSET_X + self.player.x * self.CELL_SIZE + self.CELL_SIZE // 4,
            self.MAZE_OFFSET_Y + self.player.y * self.CELL_SIZE + self.CELL_SIZE // 4,
            self.CELL_SIZE // 2,
            self.CELL_SIZE // 2
        )
        pygame.draw.rect(self.screen, self.PURPLE, rect)

    def draw_ui(self):
        # Draw turn counter
        turn_text = self.font.render(f"Turn: {self.turn_count}", True, self.WHITE)
        self.screen.blit(turn_text, (10, 10))
        
        # Draw hints remaining
        hint_text = self.font.render(f"Hints: {self.hints_remaining}", True, self.WHITE)
        self.screen.blit(hint_text, (10, 40))
        
        # Draw hint button
        hint_button = pygame.Rect(10, self.SCREEN_HEIGHT - 40, 100, 30)
        pygame.draw.rect(self.screen, self.GREEN if self.hints_remaining > 0 else self.RED, hint_button)
        button_text = self.font.render("Use Hint", True, self.BLACK)
        self.screen.blit(button_text, (15, self.SCREEN_HEIGHT - 35))
        
        # Draw controls info
        controls_text = self.font.render("Use arrow keys to move", True, self.WHITE)
        self.screen.blit(controls_text, (self.SCREEN_WIDTH - 200, self.SCREEN_HEIGHT - 40))

    def draw_hint(self):
        # Draw hint information
        hint_surface = pygame.Surface((300, 150))
        hint_surface.fill((50, 50, 50))
        hint_surface.set_alpha(200)
        
        self.screen.blit(hint_surface, (self.SCREEN_WIDTH - 310, 10))
        
        title_text = self.font.render("AI Prediction:", True, self.WHITE)
        self.screen.blit(title_text, (self.SCREEN_WIDTH - 300, 20))
        
        y_offset = 50
        for i, (x, y, value) in enumerate(self.current_hint[:3]):  # Show up to 3 predictions
            action = "Create path" if value == 1 else "Create wall"
            pred_text = self.font.render(f"• ({x}, {y}): {action}", True, self.WHITE)
            self.screen.blit(pred_text, (self.SCREEN_WIDTH - 300, y_offset))
            y_offset += 30

    def draw_game_over(self):
        # Dim the screen
        dim_surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        dim_surface.fill(self.BLACK)
        dim_surface.set_alpha(150)
        self.screen.blit(dim_surface, (0, 0))
        
        # Draw game over text
        font_large = pygame.font.SysFont('Arial', 48)
        game_over_text = font_large.render("You Won!", True, self.GREEN)
        text_rect = game_over_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        # Draw turn count
        turns_text = self.font.render(f"Completed in {self.turn_count} turns", True, self.WHITE)
        turns_rect = turns_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.screen.blit(turns_text, turns_rect)
        
        # Draw continue prompt
        continue_text = self.font.render("Click anywhere to return to menu and start new game", True, self.WHITE)
        continue_rect = continue_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(continue_text, continue_rect)

    def run(self):
        # Main game loop
        while True:
            self.handle_events()
            self.draw()
            self.clock.tick(60)

# Run the game
if __name__ == "__main__":
    game = MindMazeGame()
    game.run()