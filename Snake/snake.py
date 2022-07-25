# snake game made by @eyji-koike
import random
import time
import pygame
from pygame.locals import *

SIZE = 64
BACKGROUND_COLOR = (110, 110, 5)


class Apple:
    def __init__(self, surface_object):
        self.parent_screen = surface_object
        self.apple_icon = pygame.image.load("./Assets/apple.png").convert()
        self.apple_icon.set_colorkey((0, 0, 0), RLEACCEL)
        self.x = random.randint(1, 15) * SIZE
        self.y = random.randint(1, 11) * SIZE

    def draw(self):
        self.parent_screen.blit(self.apple_icon, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 15) * SIZE
        self.y = random.randint(1, 11) * SIZE


class Snake:
    def __init__(self, surface_object, snake_length):
        self.parent_screen = surface_object
        self.length = snake_length
        self.snake_icon = pygame.image.load("./Assets/snake_head.png").convert()
        self.snake_icon.set_colorkey((0, 0, 0), RLEACCEL)
        self.x = [SIZE] * snake_length
        self.y = [SIZE] * snake_length
        self.direction = 'down'

    def increase_snake_lenght(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            self.parent_screen.blit(self.snake_icon, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1024, 768))
        self.surface.fill(BACKGROUND_COLOR)
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)
        self.snake.draw()
        self.apple.draw()

    @staticmethod
    def collision(x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True
        return False

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # detect if the fruit was eaten
        if self.collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            # sound = pygame.mixer.Sound(path)
            # pygame.mixer.Sound.Play(sound)
            self.apple.move()
            self.snake.increase_snake_lenght()

        # detect if head collided with the body
        for i in range(3, self.snake.length):
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Game Over"

    def show_gameover(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        game_over_message = font.render(f"Game Over. Score: {self.snake.length - 1}", True, (200, 200, 200))
        self.surface.blit(game_over_message, (512, 382))
        play_again_message = font.render(f"Press Enter to Play Again", True, (200, 200, 200))
        self.surface.blit(play_again_message, (512, 412))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def display_score(self):
        font = pygame.font.SysFont('arial', 24)
        score = font.render(f"Score: {self.snake.length - 1}", True, (200, 200, 200))
        self.surface.blit(score, (760, 10))

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()

            except Exception as e:
                pause = True
                self.show_gameover()
                self.reset()

            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()
