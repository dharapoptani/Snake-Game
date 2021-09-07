import math
import random
import time
from pygame import mixer
import pygame

class Game:
    def __init__(self):
        pygame.init()
        # creating screen
        self.screen = pygame.display.set_mode((864, 640))

        #creating music
        sound = mixer.music.load("bg.wav")

        # changing title and favicon
        self.icon = pygame.image.load("snake.png")
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("Snake game")

        self.check_for_over = False
        self.player = Snake(self.screen)
        self.food = Fruit(self.screen)
        self.score = 0
        self.score_font = pygame.font.Font('freesansbold.ttf', 24)

    def show_score(self):
        value = self.score_font.render('Score : '+str(self.score), True, (28, 43, 117))
        self.screen.blit(value, (15, 10))

    def game_over(self):
        self.stop_music()
        self.check_for_over = True
        for i in range(self.player.length):
            self.player.snake_x[i] = 1000
            self.player.snake_y[i] = 1000

        value = self.score_font.render('Press ENTER to restart and ESCAPE to quit', True, (117, 28, 96))
        self.screen.blit(value, (180, 254))
        value = self.score_font.render('GAME OVER !!!', True, (117, 28, 96))
        self.screen.blit(value, (300, 284))

    def iscollision(self, x1, x2, y1, y2):
        t = math.sqrt(math.pow(x1-x2, 2)+math.pow(y2-y1, 2))
        if t <= 17:
            return True
        else:
            return False

    def start_music(self):
        mixer.music.set_volume(0.2)
        mixer.music.play(-1)

    def stop_music(self):
        mixer.music.stop()

    def play(self):
        self.start_music()
        self.player.walk()
        self.food.show_fruit()

        if(self.iscollision(self.player.snake_x[0], self.food.fruitX, self.player.snake_y[0], self.food.fruitY)):
            self.player.snake_x.append(self.player.snake_x[-1])
            self.player.snake_y.append(self.player.snake_y[-1])
            self.player.length += 1
            self.food.fruitX = random.randint(0, 26)*32
            self.food.fruitY = random.randint(0, 19)*32
            self.score += 1

        for i in range(5, self.player.length):
            if(self.check_for_over == True or self.iscollision(self.player.snake_x[0],self.player.snake_x[i],self.player.snake_y[0],self.player.snake_y[i])):
                self.game_over()
        self.show_score()

    def run(self):


        run = True
        while run:

            # changing screen color
            self.screen.fill((87, 120, 187))
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    elif event.key == pygame.K_UP:
                        self.player.move_up()
                    elif event.key == pygame.K_DOWN:
                        self.player.move_down()
                    elif event.key == pygame.K_LEFT:
                        self.player.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.player.move_right()
                    elif event.key == pygame.K_SPACE and self.check_for_over == True:
                        self.start_music()
                        self.check_for_over = False
                        self.player = Snake(self.screen)
                        self.score = 0





            time.sleep(0.2)
            self.play()

            pygame.display.update()


class Snake:
    def __init__(self, screen):
        self.screen = screen
        self.length = 1
        self.snake = pygame.image.load("square2.png")
        self.snake_x = [300]*self.length
        self.snake_y = [250]*self.length
        self.direction = "right"
        self.chng = 32

    def show_snake(self):
        for i in range(len(self.snake_x)):
            self.screen.blit(self.snake, (self.snake_x[i], self.snake_y[i]))

    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'


    def move_down(self):
        if self.direction != 'up':
            self.direction = 'down'

    def move_left(self):
        if self.direction != 'right':
            self.direction = 'left'

    def move_right(self):
        if self.direction != 'left':
            self.direction = 'right'


    def walk(self):
        for i in range(len(self.snake_x)-1, 0, -1):
            self.snake_x[i] = self.snake_x[i-1]
            self.snake_y[i] = self.snake_y[i-1]

        if self.direction == 'left':
            self.snake_x[0] -= self.chng
            if self.snake_x[0] < 0:
                self.snake_x[0] = 832
        elif self.direction == 'right':
            self.snake_x[0] += self.chng
            if self.snake_x[0] > 864:
                self.snake_x[0] = 0
        elif self.direction == 'up':
            self.snake_y[0] -= self.chng
            if self.snake_y[0] < 0:
                self.snake_y[0] = 608
        elif self.direction == 'down':
            self.snake_y[0] += self.chng
            if self.snake_y[0] > 640:
                self.snake_y[0] = 0

        self.show_snake()


class Fruit:
    def __init__(self, screen):
        self.screen = screen
        self.fruit = pygame.image.load("apple.png")
        self.fruitX = random.randint(0, 26) * 32
        self.fruitY = random.randint(0, 19) * 32

    def show_fruit(self):
        self.screen.blit(self.fruit, (self.fruitX, self.fruitY))

if __name__ == "__main__":
    game = Game()
    game.run()
