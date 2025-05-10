# MindMaze: AI-Powered Labyrinth

A dynamic maze board game where AI controls the maze structure, adapting in real-time to player movements and strategies. Players navigate through the shifting labyrinth to reach the center while avoiding AI-generated traps.

## Project Overview

This implementation is based on the project proposal submitted by Syed Azmeer Un Nabi. The game features an adaptive AI that alters the maze layout using reinforcement learning, increasing the challenge dynamically based on player strategies while ensuring a fair yet unpredictable gameplay experience.

## Features

- Dynamic maze that changes in response to player movements
- AI-controlled traps, teleporters, and shortcuts
- Reinforcement learning algorithm that adapts to player strategies
- Hint system to predict AI's next moves
- Graphical user interface built with Pygame

## Installation Requirements

To run the game, you need:

1. Python 3.7 or higher
2. Pygame
3. NumPy

Install the required packages using pip:

```bash
pip install pygame numpy
```

## Running the Game

1. Make sure all Python files are in the same directory
2. Run the main game file:

```bash
python main.py
```

## Game Instructions

- Use arrow keys to move the player character
- Reach the green center of the maze to win
- Avoid red traps
- Blue tiles are teleporters that transport you to another location
- Yellow tiles are shortcuts that move you closer to the goal
- The AI will modify the maze every few turns
- Use the "Use Hint" button to get predictions about the AI's next modifications (limited uses)

## File Structure

- `main.py`: Main game file containing the game loop and rendering logic
- `maze_generator.py`: Module for generating random mazes
- `ai_controller.py`: AI implementation using reinforcement learning
- `player.py`: Player class for tracking position and movement
- `ui_elements.py`: UI components like buttons and menus

## Game Rules

- Players must reach the center of the maze while avoiding AI-controlled obstacles
- The AI modifies the maze layout every few turns based on player actions
- Players receive a limited number of predictive hints to anticipate maze changes
- Special tiles (traps, teleportation, and shortcuts) are AI-controlled

## Color Key

- White: Open path
- Black: Wall
- Green: Goal (center)
- Red: Trap
- Blue: Teleporter
- Yellow: Shortcut
- Purple: Player

## Future Enhancements

- Multiple difficulty levels
- Multiple players (competitive or cooperative)
- More complex AI strategies
- Sound effects and music
- Ability to save/load games
- Additional power-ups and challenges

## Credits

Developed based on the project proposal by Syed Azmeer Un Nabi for the AI course instructed by Sir Abdullah Yaqoob.