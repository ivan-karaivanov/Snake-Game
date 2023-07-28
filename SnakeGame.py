import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
FPS = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.food = self.generate_food()

    def generate_food(self):
        while True:
            x, y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                return x, y

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT

    def move_snake(self):
        head_x, head_y = self.snake[-1]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        self.snake.append(new_head)
        if new_head == self.food:
            self.food = self.generate_food()
        else:
            self.snake.pop(0)

    def check_collision(self):
        head_x, head_y = self.snake[-1]
        return (
            head_x < 0 or head_x >= GRID_WIDTH
            or head_y < 0 or head_y >= GRID_HEIGHT
            or self.snake[-1] in self.snake[:-1]
        )

    def draw(self):
        self.screen.fill(BLACK)
        for segment in self.snake:
            pygame.draw.rect(self.screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, RED, (self.food[0] * CELL_SIZE, self.food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.update()

    def show_game_over_screen(self, score):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Check if the restart button is clicked
                    if WIDTH // 2 - 60 <= event.pos[0] <= WIDTH // 2 + 60 and HEIGHT // 2 + 100 <= event.pos[
                        1] <= HEIGHT // 2 + 140:
                        return

            font = pygame.font.Font(None, 74)
            text_surface = font.render('Game Over', True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 32)
            score_surface = font.render(f'Your Score: {score}', True, WHITE)
            score_rect = score_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            self.screen.blit(score_surface, score_rect)

            # Draw restart button
            pygame.draw.rect(self.screen, GREEN, (WIDTH // 2 - 60, HEIGHT // 2 + 100, 120, 40))
            font = pygame.font.Font(None, 28)
            restart_surface = font.render('Restart', True, WHITE)
            restart_rect = restart_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
            self.screen.blit(restart_surface, restart_rect)

            pygame.display.update()

    def run(self):
        while self.is_running:
            self.handle_events()
            self.move_snake()
            if self.check_collision():
                self.show_game_over_screen(len(self.snake) - 1)
                self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
                self.direction = RIGHT
                self.food = self.generate_food()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == '__main__':
    game = SnakeGame()
    game.run()
