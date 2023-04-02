import pygame
import random

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
SPEED = 10

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def move(self):
        x, y = self.positions[0]
        if self.direction == UP:
            y -= CELL_SIZE
        elif self.direction == DOWN:
            y += CELL_SIZE
        elif self.direction == LEFT:
            x -= CELL_SIZE
        elif self.direction == RIGHT:
            x += CELL_SIZE

        # Wrap around the screen if the snake hits a wall
        x = x % WINDOW_WIDTH
        y = y % WINDOW_HEIGHT

        self.positions.insert(0, (x, y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def collide_with_wall(self):
        x, y = self.positions[0]
        return x < 0 or x > WINDOW_WIDTH - CELL_SIZE or y < 0 or y > WINDOW_HEIGHT - CELL_SIZE

    def collide_with_self(self):
        return any(self.positions[0] == p for p in self.positions[1:])

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.score = 0
        self.spawn()

    def spawn(self):
        x = random.randint(0, WINDOW_WIDTH // CELL_SIZE - 1) * CELL_SIZE
        y = random.randint(0, WINDOW_HEIGHT // CELL_SIZE - 1) * CELL_SIZE
        self.position = (x, y)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, (255, 0, 0), r)

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')

snake = Snake()
food = Food()

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(SPEED)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.direction = RIGHT

    snake.move()

    if snake.collide_with_wall() or snake.collide_with_self():
        running = False

    if snake.positions[0] == food.position:
        snake.length += 1
        food.score += 1
        food.spawn()

    window.fill((255, 255, 255))
    food.draw(window)
    snake_rects = [pygame.Rect((p[0], p[1]), (CELL_SIZE, CELL_SIZE)) for p in snake.positions]
    pygame.draw.rect(window, (0, 255, 0), snake_rects[0])
    for rect in snake_rects[1:]:
        pygame.draw.rect(window, (0, 200, 0), rect)

    score_font = pygame.font.SysFont(None, 30)
    score_surface = score_font.render(f"Score: {food.score}", True, (0, 0, 0))
    score_rect = score_surface.get_rect()
    score_rect.topleft = (10, 10)
    window.blit(score_surface, score_rect)

    pygame.display.update()

pygame.quit()

