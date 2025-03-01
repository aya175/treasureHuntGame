# treasureHuntGame

In this project, you will create an exciting AI-driven grid-based game where a player navigates through a maze-like world to reach a treasure. Along the way, the player encounters challenges such as obstacles, gold, and damage tiles that affect their journey. The game will utilize the A search algorithm* for pathfinding, allowing the AI to find the optimal route to the treasure while handling real-time interactions and dynamic game mechanics.
This project combines Python programming with the Pygame library for interactive visualization, helping you learn about algorithms, game design, and grid-based navigation.

Game Features
1.	Grid-Based Maze:
•	A 20x20 grid represents the game world.
•	The grid contains different types of cells:
•	Walkable Cells: Free for movement.
•	Obstacles: Impassable blocks that the player must avoid.
•	Gold Cells: Collect these to increase the player's gold points.
•	Damage Cells: Decrease the player's health points (HP) when stepped on.

2.	Player Mechanics:
•	The player starts with a predefined amount of HP (100 Health Points) and 10 Gold Points.
•	Collect gold and avoid taking damage while navigating toward the treasure.
•	The game ends when the player reaches the treasure or runs out of HP.

3.	AI Pathfinding:
•	The A* search algorithm determines the shortest path from the start to the treasure while avoiding obstacles.
•	The AI adapts dynamically as it collects gold or takes damage.

4.	Real-Time Visualization:
•	Use the Pygame library to visualize the grid, AI's progress, and player stats.
•	Watch the AI's movements and interact with the game environment.

---> Add multiple treasures and have the AI decide the best sequence to collect them.
