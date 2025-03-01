import pygame
import heapq
import random

pygame.init()
# Constants
WIDTH, HEIGHT = 600, 600 # Window dimensions
ROWS, COL = 20, 20 # Number of rows and columns in the grid
SIZE = WIDTH // COL # Size of each cell in the grid
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (212, 175, 55)
BLUE = (0, 0, 255)
GREEN = (124, 252, 0)

# Game variables
HP = 100 # Initial health points
GOLD = 10 # Initial gold

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Treasure Hunt Game")

LIGHT_GREEN = (144, 238, 144)
def draw_grid(grid, visited_cells):
    """
    Draw the grid on the screen.

    Args:
    grid (list of lists): The grid representing the game map.
    visited_cells (list of tuples): List of cells visited by the player.
    """
    for row in range(ROWS):
        for col in range(COL):
            color = WHITE
            if (row, col) in visited_cells:
                color = LIGHT_GREEN  
            elif grid[row][col] == 1:  
                color = BLACK  
            elif grid[row][col] == 2:  
                color = YELLOW  
            elif grid[row][col] == 3:  
                color = RED  
            elif grid[row][col] == 4:  
                color = BLUE  
            pygame.draw.rect(screen, color, (col * SIZE, row * SIZE, SIZE, SIZE))
            pygame.draw.rect(screen, BLACK, (col * SIZE, row * SIZE, SIZE, SIZE), 1)

def heuristic(a, b):
    """
    Calculate the Manhattan distance between two points.

    Args:
    a (tuple): Coordinates of the first point (row, col).
    b (tuple): Coordinates of the second point (row, col).

    Returns:
    int: The Manhattan distance between the two points.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def path(S, G):
    """
    Reconstruct the path from the start to the goal.

    Args:
    S (dict): Dictionary mapping each node to its predecessor.
    G (tuple): Coordinates of the goal node (row, col).

    Returns:
    list of tuples: The path from the start to the goal.
    """
    p = []
    while G in S:
        p.append(G)
        G = S[G]
    p.reverse()
    return p

def a_star_search(grid, start, goal):
    """
    Perform A* search to find the shortest path from the start to the goal.

    Args:
    grid (list of lists): The grid representing the game map.
    start (tuple): Coordinates of the start point (row, col).
    goal (tuple): Coordinates of the goal point (row, col).

    Returns:
    list of tuples: The path from the start to the goal, or an empty list if no path is found.
    """
    try:
        Q = []
        heapq.heappush(Q, (0, start))
        FROM = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        while Q:
            _, current = heapq.heappop(Q)

            if current == goal:
                return path(FROM, current)

            for a, b in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + a, current[1] + b)
                if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COL:
                    if grid[neighbor[0]][neighbor[1]] == 1:  # Obstacle
                        continue
                    tentative_g_score = g_score[current] + 1

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        FROM[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        heapq.heappush(Q, (f_score[neighbor], neighbor))
        return []
    except Exception as e:
        print(f"Error in A* search:{e}")
        return[]

def create_grid():
    """
    Create the game grid with random obstacles, gold, traps, and treasures.

    Returns:
    tuple: The grid, the starting position of the player, and the positions of the treasures.
    """
    grid = [[0 for _ in range(COL)] for _ in range(ROWS)]

    for _ in range(80):
        grid[random.randint(0, ROWS-1)][random.randint(0, COL-1)] = 1  
    for _ in range(20):
        grid[random.randint(0, ROWS-1)][random.randint(0, COL-1)] = 2  
    for _ in range(20):
        grid[random.randint(0, ROWS-1)][random.randint(0, COL-1)] = 3  

    treasures = []
    for _ in range(3):  
        while True:
            t_row, t_col = random.randint(0, ROWS-1), random.randint(0, COL-1)
            if grid[t_row][t_col] == 0:
                grid[t_row][t_col] = 4  
                treasures.append((t_row, t_col))
                break

    return grid, (0, 0), treasures


def main():
    """
    Main function to run the game.
    """
    try:
        clock = pygame.time.Clock()
        grid, start, treasures = create_grid()

        playerPos = start
        hp = HP
        gold = GOLD
        visited_cells = []
        collected_treasures = 0
        total_treasures = len(treasures)
        path = a_star_search(grid, playerPos, treasures[0]) if treasures else []

        run = True
        while run:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                screen.fill(WHITE)
                draw_grid(grid, visited_cells)
                pygame.draw.rect(screen, GREEN, (playerPos[1] * SIZE, playerPos[0] * SIZE, SIZE, SIZE))

                if path:
                    next_pos = path.pop(0)
                    visited_cells.append(next_pos)
                    if grid[next_pos[0]][next_pos[1]] == 2:  
                        gold += 10
                        grid[next_pos[0]][next_pos[1]] = 0
                    elif grid[next_pos[0]][next_pos[1]] == 3:  
                        hp -= 10
                        grid[next_pos[0]][next_pos[1]] = 0
                    playerPos = next_pos

                    
                    if playerPos == treasures[0]:
                        treasures.pop(0)  
                        collected_treasures += 1
                        path = a_star_search(grid, playerPos, treasures[0]) if treasures else []

                font = pygame.font.SysFont(None, 55)
                hp_text = font.render(f"HP: {hp}", True, RED)
                gold_text = font.render(f"Gold: {gold}", True, YELLOW)
                treasures_text = font.render(f"Treasures: {collected_treasures}/{total_treasures}", True, BLUE)
                screen.blit(hp_text, (10, 10))
                screen.blit(gold_text, (150, 10))
                screen.blit(treasures_text, (330, 10))

                if hp <= 0 or not treasures:
                    end_text = font.render("Game Over!", True, BLUE)
                    screen.blit(end_text, (WIDTH // 2 - 100, HEIGHT // 2))
                    pygame.display.flip()
                    pygame.time.delay(5000)
                    run = False

                pygame.display.flip()   
                clock.tick(5)
            except Exception as e:
                print(f"Error during game loop: {e}")    
                run = False
    except Exception as e:
        print(f"Error initializing the game: {e}")
    finally:
        pygame.quit()   


if __name__ == "__main__":
    main()
