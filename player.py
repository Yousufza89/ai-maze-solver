class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.moves = 0
        self.score = 0
        
    def move(self, dx, dy):
        """Move the player by the given deltas"""
        self.x += dx
        self.y += dy
        self.moves += 1
    
    def reset(self, x, y):
        """Reset player to specific position"""
        self.x = x
        self.y = y
        
    def get_position(self):
        """Get current position"""
        return (self.x, self.y)