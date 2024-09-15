import pygame
import random
import sys
import traceback
import math

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Bullet Game")


def main():
    try:
        running = True

        snake = [(round(WIDTH / 2), round(HEIGHT / 2))]
        snake_direction = (0, 0)

        food = spawn_food()

        barrel = Barrel()

        clock = pygame.time.Clock()
        FPS = 14  # Adjust the difficulty of the game (easy <= 15 | medium >= 15 | hard >= 25)

        while running:
            dt = clock.tick(FPS) / 1000

            screen.fill(WHITE)
            draw_grid()

            pygame.draw.rect(screen, RED, (food[0], food[1], GRID_SIZE, GRID_SIZE))

            for segment in snake:
                pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

            if barrel.update(dt, snake):
                running = False
            barrel.draw()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and snake_direction != (0, 1):
                snake_direction = (0, -1)
            elif keys[pygame.K_DOWN] and snake_direction != (0, -1):
                snake_direction = (0, 1)
            elif keys[pygame.K_LEFT] and snake_direction != (1, 0):
                snake_direction = (-1, 0)
            elif keys[pygame.K_RIGHT] and snake_direction != (-1, 0):
                snake_direction = (1, 0)

            new_head = (
                snake[0][0] + snake_direction[0] * GRID_SIZE,
                snake[0][1] + snake_direction[1] * GRID_SIZE
            )
            snake.insert(0, new_head)

            if new_head == food:
                food = spawn_food()
            else:
                snake.pop()

            if new_head in snake[1:]:
                running = False

            if (new_head[0] < 0 or new_head[0] >= WIDTH or
                    new_head[1] < 0 or new_head[1] >= HEIGHT):
                running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.update()

    except Exception as e:
        print("An error occurred:")
        traceback.print_exc()
    finally:
        pygame.quit()


def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GREY, (0, y), (WIDTH, y))


def spawn_food():
    x = random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
    y = random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
    return x, y


class Barrel:
    def __init__(self):
        self.x = random.randint(0, WIDTH - GRID_SIZE)
        self.y = random.randint(0, HEIGHT - GRID_SIZE)
        self.bullets = []
        self.bullet_speed = 5
        self.spawn_rate = 1
        self.spawn_timer = 0

    def update(self, dt, snake):
        self.spawn_timer += dt
        if self.spawn_timer >= 1 / self.spawn_rate:
            self.spawn_bullet_smart(snake)
            self.spawn_timer = 0

        self.move_bullets()

        for bullet in self.bullets:
            for segment in snake:
                if self.check_collision(segment, bullet):
                    return True

        return False

    def spawn_bullet_smart(self, snake):
        head_x, head_y = snake[0]
        angle = math.atan2(head_y - self.y, head_x - self.x)
        self.bullets.append((self.x, self.y, angle))

    def move_bullets(self):
        for i, bullet in enumerate(self.bullets):
            x, y, angle = bullet
            x += self.bullet_speed * math.cos(angle)
            y += self.bullet_speed * math.sin(angle)
            self.bullets[i] = (x, y, angle)

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, GRID_SIZE, GRID_SIZE))

        for bullet in self.bullets:
            pygame.draw.circle(screen, BLACK, (int(bullet[0] + GRID_SIZE / 2), int(bullet[1] + GRID_SIZE / 2)),
                               GRID_SIZE // 4)

    def check_collision(self, position, bullet):
        bx, by, _ = bullet
        return (bx <= position[0] < bx + GRID_SIZE and
                by <= position[1] < by + GRID_SIZE)


if __name__ == "__main__":
    main()
