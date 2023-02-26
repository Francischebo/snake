import pygame as pg
import random

# Initialize Pygame
pg.init()

# Define game variables
screen_width = 800
screen_height = 600
block_size = 10
food_size = 10
game_over = False

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Set up the game screen
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Snake Game")


# Define the Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((screen_width / 2), (screen_height / 2))]
        self.direction = random.choice([pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT])
        self.color = green

    def get_head_position(self):
        return self.positions[0]


    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x = self.direction
        y = self.direction
        new = ((cur[0] + x * block_size) % screen_width, (cur[1] + y * block_size) % screen_height)
        if len(self.positions) > 2 and new in self.positions[2:]:
            game_over = True
        else:
            self.positions.insert(0, new) 
            if len(self.positions) > self.length:
                self.positions.pop()



    def reset(self):
        self.length = 1
        self.positions = [((screen_width / 2), (screen_height / 2))]
        self.direction = random.choice([pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT])

    def draw(self, surface):
        for p in self.positions:
            r = pg.Rect((p[0], p[1]), (block_size, block_size))
            pg.draw.rect(surface, self.color, r)
            pg.draw.rect(surface, black, r, 1)


# Define the Food class
class Food:
    def __init__(self):
        x = random.randrange(food_size, screen_width - food_size, food_size)
        y = random.randrange(food_size, screen_height - food_size, food_size)
        self.position = (x, y)
        self.color = red

    def draw(self, surface):
        r = pg.Rect((self.position[0], self.position[1]), (food_size, food_size))
        pg.draw.rect(surface, self.color, r)
        pg.draw.rect(surface, black, r, 1)


# Initialize the Snake and Food objects
snake = Snake()
food = Food()


# Define the main game loop
clock = pg.time.Clock()
pause = True
while not game_over:
    clock.tick(5)
    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_over = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                pause = not pause
            elif not pause:
                if event.key == pg.K_UP:
                    snake.turn((0, -1))
                elif event.key == pg.K_DOWN:
                    snake.turn((0, 1))
                elif event.key == pg.K_LEFT:
                    snake.turn((-1, 0))
                elif event.key == pg.K_RIGHT:
                    snake.turn((1, 0))

    # Move the snake and check for collision
    if not pause:
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            food = Food()

    # Draw the game screen
    screen.fill(white)
    snake.draw(screen)
    food.draw(screen)
    pg.display.update()

    # Limit the frame rate
    clock.tick(10)


