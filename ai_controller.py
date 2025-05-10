import numpy as np
import random

class AIController:
    def __init__(self, maze_width, maze_height):
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.maze = None
        self.player_x = 0
        self.player_y = 0
        self.goal_x = maze_width // 2
        self.goal_y = maze_height // 2
        
        # Learning parameters
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 0.3
        
        # Q-values for maze modifications
        self.q_values = {}  # (state, action) -> value
        
        # State history
        self.state_history = []
        
        # Define action space (x, y, new_value)
        self.actions = []
        for x in range(maze_width):
            for y in range(maze_height):
                for value in [0, 1]:  # 0 = wall, 1 = path
                    self.actions.append((x, y, value))
    
    def set_maze(self, maze):
        """Set the current maze state"""
        self.maze = np.copy(maze)
    
    def set_player_position(self, x, y):
        """Update the player's position"""
        self.player_x = x
        self.player_y = y
        
        # Add current state to history
        current_state = self._get_state()
        self.state_history.append(current_state)
        
        # If history is too long, remove oldest state
        if len(self.state_history) > 10:
            self.state_history.pop(0)
    
    def _get_state(self):
        """Create a simplified state representation
        State includes:
        - Player position
        - Distance to goal
        - Surrounding walls/paths (3x3 area around player)
        """
        # Flatten the player position and distance to goal
        manhattan_dist = abs(self.player_x - self.goal_x) + abs(self.player_y - self.goal_y)
        
        # Get surroundings (3x3 area around player)
        surroundings = []
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = self.player_x + dx, self.player_y + dy
                if 0 <= nx < self.maze_width and 0 <= ny < self.maze_height:
                    surroundings.append(self.maze[ny][nx])
                else:
                    surroundings.append(0)  # Treat out-of-bounds as walls
        
        # Combine all state elements into a tuple
        return (self.player_x, self.player_y, manhattan_dist, tuple(surroundings))
    
    def _get_reward(self, state, action, new_state):
        """Calculate reward for a state-action-new_state transition
        Rewards:
        - Positive if action makes it harder for player
        - Negative if action makes it impossible to reach goal
        - Zero otherwise
        """
        x, y, value = action
        
        # We want to make the game challenging but not impossible
        # So we reward actions that increase the path length to the goal
        
        # Extract player position and distance from state tuples
        _, _, old_dist, _ = state
        _, _, new_dist, _ = new_state
        
        # Did the distance to goal increase?
        if new_dist > old_dist:
            return 1.0  # Positive reward
        
        # Did we make it impossible to reach the goal?
        # This is a simplified check - in reality you'd use a pathfinding algorithm
        if value == 0 and self._is_critical_path(x, y):
            return -5.0  # Strong negative reward
        
        # Neutral action
        return 0.0
    
    def _is_critical_path(self, x, y):
        """Check if a position is on the critical path to the goal
        This is a simplified version - would use pathfinding in a real implementation
        """
        # Check if this position is directly between player and goal
        if (min(self.player_x, self.goal_x) <= x <= max(self.player_x, self.goal_x) and
            min(self.player_y, self.goal_y) <= y <= max(self.player_y, self.goal_y)):
            return True
        return False
    
    def _get_valid_actions(self):
        """Get valid actions in the current state
        Invalid actions:
        - Modifying player or goal position
        - Actions that would make the goal unreachable
        """
        valid_actions = []
        
        for action in self.actions:
            x, y, value = action
            
            # Skip player and goal positions
            if (x == self.player_x and y == self.player_y) or (x == self.goal_x and y == self.goal_y):
                continue
            
            # For now, allow all other actions (in a real implementation,
            # you'd check if the action makes the goal unreachable)
            valid_actions.append(action)
        
        return valid_actions
    
    def _choose_action(self, state):
        """Choose action using epsilon-greedy strategy"""
        valid_actions = self._get_valid_actions()
        
        # Exploration: choose random action
        if random.random() < self.exploration_rate:
            return random.choice(valid_actions)
        
        # Exploitation: choose best action based on Q-values
        best_value = float('-inf')
        best_actions = []
        
        for action in valid_actions:
            state_action = (state, action)
            q_value = self.q_values.get(state_action, 0.0)
            
            if q_value > best_value:
                best_value = q_value
                best_actions = [action]
            elif q_value == best_value:
                best_actions.append(action)
        
        # If there are multiple best actions, choose randomly
        return random.choice(best_actions)
    
    def _update_q_value(self, state, action, reward, next_state):
        """Update Q-value using Q-learning update rule"""
        state_action = (state, action)
        
        # Get current Q-value
        current_q = self.q_values.get(state_action, 0.0)
        
        # Get maximum Q-value for next state
        next_max_q = 0.0
        valid_next_actions = self._get_valid_actions()
        for next_action in valid_next_actions:
            next_state_action = (next_state, next_action)
            next_q = self.q_values.get(next_state_action, 0.0)
            next_max_q = max(next_max_q, next_q)
        
        # Q-learning update rule
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)
        
        # Update Q-value
        self.q_values[state_action] = new_q
    
    def get_maze_modifications(self):
        """Get AI-generated maze modifications"""
        # Get current state
        current_state = self._get_state()
        
        # Choose actions (2-5 modifications)
        num_modifications = random.randint(2, 5)
        modifications = []
        
        # Copy maze for simulation
        temp_maze = np.copy(self.maze)
        
        for _ in range(num_modifications):
            # Choose an action
            action = self._choose_action(current_state)
            x, y, value = action
            
            # Apply the action to the temp maze
            temp_maze[y][x] = value
            
            # Add to modifications list
            modifications.append(action)
            
            # Get new state
            new_state = self._simulate_new_state(temp_maze, current_state)
            
            # Calculate reward
            reward = self._get_reward(current_state, action, new_state)
            
            # Update Q-value
            self._update_q_value(current_state, action, reward, new_state)
            
            # Update current state for next iteration
            current_state = new_state
        
        return modifications
    
    def _simulate_new_state(self, maze, state):
        """Simulate new state after a maze modification"""
        player_x, player_y, _, _ = state
        
        # Calculate new Manhattan distance
        manhattan_dist = abs(player_x - self.goal_x) + abs(player_y - self.goal_y)
        
        # Get new surroundings
        surroundings = []
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = player_x + dx, player_y + dy
                if 0 <= nx < self.maze_width and 0 <= ny < self.maze_height:
                    surroundings.append(maze[ny][nx])
                else:
                    surroundings.append(0)  # Treat out-of-bounds as walls
        
        # Return new state
        return (player_x, player_y, manhattan_dist, tuple(surroundings))
    
    def get_modification_prediction(self):
        """Get prediction of next maze modifications (for hints)"""
        # Use current state to predict likely modifications
        current_state = self._get_state()
        
        # Get valid actions
        valid_actions = self._get_valid_actions()
        
        # Sort actions by Q-value
        action_values = []
        for action in valid_actions:
            state_action = (current_state, action)
            q_value = self.q_values.get(state_action, 0.0)
            action_values.append((action, q_value))
        
        # Sort by Q-value (descending)
        action_values.sort(key=lambda x: x[1], reverse=True)
        
        # Return top 5 actions
        return [action for action, _ in action_values[:5]]