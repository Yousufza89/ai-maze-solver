import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.font = pygame.font.SysFont('Arial', 20)
        
    def draw(self, screen):
        # Draw the button
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Border
        
        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class MenuSystem:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Create buttons
        button_width = 200
        button_height = 50
        
        self.buttons = {
            "start_game": Button(
                screen_width // 2 - button_width // 2,
                screen_height // 2 - button_height,
                button_width,
                button_height,
                "Start Game",
                (0, 200, 0),
                (0, 255, 0),
                (0, 0, 0)
            ),
            "quit": Button(
                screen_width // 2 - button_width // 2,
                screen_height // 2 + button_height,
                button_width,
                button_height,
                "Quit",
                (200, 0, 0),
                (255, 0, 0),
                (0, 0, 0)
            )
        }
        
        # Title font
        self.title_font = pygame.font.SysFont('Arial', 48)
        self.subtitle_font = pygame.font.SysFont('Arial', 24)
        self.instruction_font = pygame.font.SysFont('Arial', 20)
        
    def handle_event(self, event):
        """Handle mouse events for the menu"""
        if event.type == pygame.MOUSEMOTION:
            # Update hover states
            for button in self.buttons.values():
                button.check_hover(event.pos)
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check for button clicks
            if self.buttons["start_game"].is_clicked(event.pos):
                return "start_game"
            elif self.buttons["quit"].is_clicked(event.pos):
                return "quit"
        
        return None
        
    def draw(self, screen):
        """Draw the menu"""
        # Fill background
        screen.fill((0, 0, 0))
        
        # Draw title
        title_surface = self.title_font.render("MindMaze: AI-Powered Labyrinth", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 4 - 30))
        screen.blit(title_surface, title_rect)
        
        # Draw subtitle
        subtitle_surface = self.subtitle_font.render("Navigate the shifting maze controlled by AI", True, (200, 200, 200))
        subtitle_rect = subtitle_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 4 + 20))
        screen.blit(subtitle_surface, subtitle_rect)
        
        # Draw instructions
        instructions = [
            "Use arrow keys to move your character",
            "Reach the green goal while avoiding red traps",
            "Blue teleporters will transport you to a paired location",
            "Yellow shortcuts will move you closer to the goal",
            "The AI will modify the maze every few turns"
        ]
        
        y_offset = self.screen_height // 4 + 80
        for instruction in instructions:
            instruction_surface = self.instruction_font.render(instruction, True, (180, 180, 180))
            instruction_rect = instruction_surface.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(instruction_surface, instruction_rect)
            y_offset += 30
        
        # Draw buttons
        for button in self.buttons.values():
            button.draw(screen)

class Legend:
    def __init__(self, x, y, square_size):
        self.x = x - 170  # Position on right side
        self.y = y
        self.square_size = square_size // 2
        self.padding = 5
        self.font = pygame.font.SysFont('Arial', 16)
        
    def draw(self, screen, items):
        """Draw the color legend
        items: list of tuples (name, color, description)
        """
        # Draw legend background
        legend_width = 160
        legend_height = len(items) * (self.square_size + self.padding * 2) + self.padding * 2
        legend_surface = pygame.Surface((legend_width, legend_height))
        legend_surface.fill((40, 40, 40))
        legend_surface.set_alpha(220)
        screen.blit(legend_surface, (self.x, self.y))
        
        # Draw title
        title_text = self.font.render("LEGEND:", True, (255, 255, 255))
        screen.blit(title_text, (self.x + 10, self.y + 10))
        
        # Draw items
        y_offset = self.y + 35
        for name, color, description in items:
            # Skip black (wall) in the legend since it's hard to see
            if color == (0, 0, 0):  # Black
                # Draw with border
                rect = pygame.Rect(self.x + 10, y_offset, self.square_size, self.square_size)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # White border
            else:
                # Draw color square
                pygame.draw.rect(screen, color, 
                              (self.x + 10, y_offset, self.square_size, self.square_size))
                
            # Draw description text
            text = self.font.render(f"{description}", True, (255, 255, 255))
            screen.blit(text, (self.x + 20 + self.square_size, y_offset + 2))
            
            y_offset += self.square_size + self.padding * 2