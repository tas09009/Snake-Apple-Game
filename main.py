import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple:
    def __init__(self, parentScreen):
        self.parentScreen = parentScreen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE * 3 # NOTES: Starts at x = 120
        self.y = SIZE * 3 # NOTES: Starts at y = 120

    def draw(self):
        self.parentScreen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self, width, height):
        self.x = random.randrange(0, width, SIZE)
        self.y = random.randrange(0, height, SIZE)
        self.draw()

class Snake:
    def __init__(self, parentScreen, length):
        self.parentScreen = parentScreen
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'
        
        self.length = length
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        
    def moveUp(self):
        self.direction = 'up'

    def moveDown(self):
        self.direction = 'down'

    def moveLeft(self):
        self.direction = 'left'

    def moveRight(self):
        self.direction = 'right'

    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE

        self.draw()

    def draw(self):
        self.parentScreen.fill(BACKGROUND_COLOR) # NOTES: clear the screen, fill with this color
        for i in range(self.length):
            self.parentScreen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increaseLength(self): 
        lastBlockIdx = self.length - 1
        lastBlockValueX = self.x[lastBlockIdx]
        lastBlockValueY = self.y[lastBlockIdx]
        self.x.append(lastBlockValueX - SIZE)
        self.y.append(lastBlockValueY - SIZE)
        self.length += 1


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.width = 1000
        self.height = 800
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.snake = Snake(self.surface, length=1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def isCollision(self, x1, y1, x2, y2):
        if y2 >= y1 and y2 < y1 + SIZE:
            if x2 >= x1 and x2 < x1 + SIZE:
                return True
        return False

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.displayScore()
        pygame.display.flip()

        # TODO sounds not working
        # NOTES: snake eating apple
        if self.isCollision(self.apple.x, self.apple.y, self.snake.x[0], self.snake.y[0]):
            sound = pygame.mixer.Sound("resources/ding.mp3")
            pygame.mixer.Sound.play(sound)
            self.apple.move(self.width, self.height)
            self.snake.increaseLength()

        # NOTES: snake hitting itself
        for i in range(1, self.snake.length):
            if self.isCollision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                sound = pygame.mixer.Sound("resources/crash.mp3")
                pygame.mixer.Sound.play(sound)
                raise "Game Over"

        # NOTES: snake hitting wall
        # TODO

    def displayScore(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (850,10))

    def displayGameOverMessage(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game Over! Your score is: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200,300))
        line2 = font.render("To play again, press Enter. To Exit, press Escape", True, (255, 255, 255))
        self.surface.blit(line2, (200,350))

        pygame.display.flip()

    def reset(self):
        self.snake.length = 1

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
                        if event.key == K_UP:
                            self.snake.moveUp()
                            
                        if event.key == K_DOWN:
                            self.snake.moveDown()
                            
                        if event.key == K_LEFT:
                            self.snake.moveLeft()
                            
                        if event.key == K_RIGHT:
                            self.snake.moveRight()
                        
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.displayGameOverMessage()
                pause = True
                self.reset()
            time.sleep(0.1)



if __name__ == "__main__":
    game = Game()
    game.run()
