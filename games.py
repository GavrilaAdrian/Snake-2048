import pygame
import time
import random
import numpy as np


class Apple:
    def __init__(self):
        self.apple = [0, 0]
    def generateApple(self, mySnake = [[0, 0]], dis_height = 300, dis_width = 300, block_sizes = 10):
        self.apple = [mySnake[0][0], mySnake[0][1]]
        while self.apple in mySnake:
            self.apple = [int(random.randint(0, 99) * dis_height  / 100/ block_sizes), int(random.randint(0, 99) * dis_height / 100 / block_sizes)]
    def appleEaten(self, x = [0, 0]):
        if x == self.apple:
            return True
        return False

class Snake:
    # head = [[int(dis_height / block_sizes / 2), int(dis_width / block_sizes / 2)]] - middle of map
    def __init__(self, head = [0, 0], initial_lenght = 3):
        self. initial_lenght = initial_lenght
        self.snake = []
        self.direction = "down"
        for i in range(0, initial_lenght):
            self.snake.append([int(head[0] - i), int(head[1])])
        self.gameLost = False
    def controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not self.direction == "right":
                    self.direction = "left"
                    break
                elif event.key == pygame.K_RIGHT and not self.direction == "left":
                    self.direction = "right"
                    break
                elif event.key == pygame.K_DOWN and not self.direction == "up":
                    self.direction = "down"
                    break
                elif event.key == pygame.K_UP and not self.direction == "down":
                    self.direction = "up"
                    break
        return False
    def gotApple(self, apple):
        if self.snake[0] == apple:
            return True
        return False
    def createNewListForSnake(self, newHead, appleCatched = False):
        newSnakeList = [newHead]
        for i in self.snake:
            if i is not self.snake[len(self.snake) - 1]: # we dont save the last element
                newSnakeList.append(i)
            elif appleCatched == True: # we save the last element if we got the apple
                newSnakeList.append(i)
        self.snake = newSnakeList
    def move(self, a, dis_width = 600, dis_height = 450, block_sizes = 30):
        x = []
        if self.direction == "right":
            x = [self.snake[0][0], self.snake[0][1] + 1]
        elif self.direction == "left":
            x = [self.snake[0][0], self.snake[0][1] - 1]
        elif pygame.K_DOWN and not self.direction == "up":
            x = [self.snake[0][0] + 1, self.snake[0][1]]
        elif pygame.K_UP and not self.direction == "down":
            x = [self.snake[0][0] - 1, self.snake[0][1]]

        if x in self.snake or x[0] < 0 or x[1] < 0:
            self.gameLost = True
        if x[0] >= int(dis_height / block_sizes) or x[1] >= int(dis_width / block_sizes):
            self.gameLost = True
        if x == a:
            self.createNewListForSnake(x, True)
            return True
        else:
            self.createNewListForSnake(x, False)
        return False

class GameSnake:
    def __init__(self, dis_width = 600, dis_height = 450, block_sizes = 30, movement_speed = 8):
        pygame.init()

        self.clock = pygame.time.Clock()

        self.dis_width = dis_width
        self.dis_height = dis_height
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption('Snake by AG')

        self.block_sizes = block_sizes
        self.movement_speed = movement_speed

        self.white = (255, 255, 255)
        self.blue = (50, 153, 213) 
        self.green = (0, 255, 0) 
        self.yellow = (255, 255, 102)
        self.gray = (128, 128, 128) 
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)

    def printSnake(self, snake, apple):
        self.dis.fill(self.black)
        pygame.draw.rect(self.dis, self.red, [apple[1] * self.block_sizes, apple[0] * self.block_sizes, self.block_sizes, self.block_sizes]) #apple
        
        for x in snake:
            pygame.draw.rect(self.dis, self.green, [x[1] * self.block_sizes, x[0] * self.block_sizes, self.block_sizes, self.block_sizes]) # snake body
        pygame.draw.rect(self.dis, self.yellow, [snake[0][1] * self.block_sizes, snake[0][0] * self.block_sizes, self.block_sizes, self.block_sizes]) # head

    def gameLoop(self):
        self.clock.tick(self.movement_speed)
        stop = False

        s = Snake(head = [int(self.dis_height / self.block_sizes / 2), int(self.dis_width / self.block_sizes / 2)])
        a = Apple()
        a.generateApple(s.snake, self.dis_height, self.dis_width, self.block_sizes)

        while not stop and not s.gameLost:
            stop = s.controls()
            if s.move(a.apple):
                a.generateApple(s.snake, self.dis_height, self.dis_width, self.block_sizes)
            self.printSnake(s.snake, a.apple)
            pygame.display.update()
            self.clock.tick(self.movement_speed)
        return len(s.snake) - s.initial_lenght
    def endScreen(self, score = 0):
        self.dis.fill(self.white)
        score_font = pygame.font.SysFont("comicsansms", 35)
        option_font = pygame.font.SysFont("comicsansms", 20)

        value = score_font.render(f"Game Over! Your Score: {score}", True, self.green)
        self.dis.blit(value, [0, 0])

        value2 = score_font.render(f"Press W to restart, Q to exit!", True, self.blue)
        self.dis.blit(value2, [0, 50])
        value3 = score_font.render(f"Press P to switch game!", True, self.blue)
        self.dis.blit(value3, [0, 85])

        pygame.display.update()

        play_again = False
        switch_game = False
        action = False
        while not action:
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    play_again = False
                    switch_game = False
                    action = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        play_again = False
                        switch_game = False
                        action = True
                    if event.key == pygame.K_w:
                        play_again = True
                        switch_game = False
                        action = True
                    if event.key == pygame.K_p:
                        play_again = True
                        switch_game = True
                        action = True
            pygame.display.flip()
            self.clock.tick(60)
        return play_again, switch_game

class Game2048: 
    def __init__(self, dis_height = 600, dis_width = 600, block_sizes = 150, movement_speed = 8, grid = 5):
        pygame.init()

        self.clock = pygame.time.Clock()

        self.dis_width = dis_width
        self.dis_height = dis_height
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption('2048 by AG')

        self.block_sizes = block_sizes
        self.movement_speed = movement_speed

        self.white = (255, 255, 255)
        self.gray = (128, 128, 128)
        self.darkgray = (200, 200, 200)
        self.black = (0, 0, 0)

        self.blue = (50, 153, 213) 
        self.green = (0, 255, 0) 
        self.yellow = (255, 255, 102)
        self.darkeryellow = (255, 255, 52)
        self.lightyellow = (255, 255, 237)
        self.darkyellow = (140, 128, 0)
        self.lightorange = (255, 213, 128)
        self.orange = (255, 165, 0)
        self.semilightorange = (255, 180, 60)
        self.purple = (160, 32, 240)
        self.red = (255, 0, 0)

        self.automove = 0

        self.gameMap = []
        for i in range(0, int(dis_height / block_sizes)):
            new_line = []
            for j in range(0, int(dis_width / block_sizes)):
                new_line.append(0)
            self.gameMap.append(new_line)

    def add_block(self):
        zeros = False
        for line in self.gameMap:
            if zeros == False:
                for element in line:
                    if element == 0:
                        zeros = True
                        break
        if not zeros:
            return True
        a = random.randint(0, len(self.gameMap) - 1)
        b = random.randint(0, len(self.gameMap[0]) - 1)
        while self.gameMap[a][b] != 0:
            a = random.randint(0, len(self.gameMap) - 1)
            b = random.randint(0, len(self.gameMap[0]) - 1)
        new_number = 2**(random.randint(1, 3))
        self.gameMap[a][b] = new_number
        return False # we return if we lost
    def calculateRow(self, new_line):
        stop = False
        while not stop:
            stop = True
            last_index = len(new_line)
            my_index = 0
            while my_index < last_index - 1:
                if new_line[my_index] == new_line[my_index + 1]:
                    new_line[my_index] *= 2
                    new_line.pop(my_index + 1)
                    stop = False # if there is a change then we will run it again
                last_index = len(new_line)
                my_index += 1
        return new_line
    def goLeft(self):
        for i in range(0, len(self.gameMap)):
            # shiftam toate elementele nenule la stanga
            new_line = []
            for j in range(0, len(self.gameMap[i])):
                if self.gameMap[i][j] != 0:
                    new_line.append(self.gameMap[i][j])
            # combinam elementele la stanga
            new_line = self.calculateRow(new_line)
            # we add the removed zeros 
            index = 0
            for j in range(0, len(self.gameMap[i])):
                self.gameMap[i][j] = 0
                if index < len(new_line):
                    self.gameMap[i][j] = new_line[index]
                    index += 1
    def goRight(self):
        for i in range(0, len(self.gameMap)):
            # shiftam toate elementele nenule la dreapta
            new_line = []
            for j in range(len(self.gameMap[i]) - 1, -1, -1):
                if self.gameMap[i][j] != 0:
                    new_line.append(self.gameMap[i][j])

            new_line = self.calculateRow(new_line)
            # we add the removed zeros
            index = 0
            for j in range(len(self.gameMap[i]) - 1, -1, -1):
                self.gameMap[i][j] = 0
                if index < len(new_line):
                    self.gameMap[i][j] = new_line[index]
                    index += 1
    def goUp(self):
        for j in range(0, len(self.gameMap[0])):
            new_line = []
            for i in range(0, len(self.gameMap)):
                if self.gameMap[i][j] != 0:
                    new_line.append(self.gameMap[i][j])

            new_line = self.calculateRow(new_line)
            index = 0
            for i in range(0, len(self.gameMap)):
                self.gameMap[i][j] = 0
                if index < len(new_line):
                    self.gameMap[i][j] = new_line[index]
                    index += 1
    def goDown(self):
        for j in range(0, len(self.gameMap[0])):
            new_line = []
            for i in range(len(self.gameMap) - 1, -1, -1):
                if self.gameMap[i][j] != 0:
                    new_line.append(self.gameMap[i][j])

            new_line = self.calculateRow(new_line)
            index = 0
            for i in range(len(self.gameMap) - 1, -1, -1):
                self.gameMap[i][j] = 0
                if index < len(new_line):
                    self.gameMap[i][j] = new_line[index]
                    index += 1
    def controls(self):
        action = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if self.automove == 0:
                        self.automove = 1
                    else:
                        self.automove = 0
                if event.key == pygame.K_LEFT and self.automove == 0:
                    action = True
                    self.goLeft()
                    break
                elif event.key == pygame.K_RIGHT and self.automove == 0:
                    action = True
                    self.goRight()
                    break
                elif event.key == pygame.K_UP and self.automove == 0:
                    action = True
                    self.goUp()
                    break
                elif event.key == pygame.K_DOWN and self.automove == 0:
                    action = True
                    self.goDown()
                    break
        if self.automove != 0:
            action = True
            if self.automove == 1:
                self.automove = 2
                self.goLeft()
            elif self.automove == 2:
                self.automove = 3
                self.goDown()
            elif self.automove == 3:
                self.automove = 4
                self.goRight()
            elif self.automove == 4:
                self.automove = 1
                self.goUp()
        if action == True:
            return self.add_block()
        return False

    def sumMap(self):
        sum = 0
        for line in self.gameMap:
            for element in line:
                sum += element
        return sum
    def printMap(self):
        self.dis.fill(self.black)
        number_font = pygame.font.SysFont("comicsansms", 40)
        for i in range(0, len(self.gameMap)): #print blocks
            for j in range(0, len(self.gameMap[i])):
                text_color = (0,0,0)
                background_color = (0,0,0)
                if self.gameMap[i][j] == 0:
                    text_color = self.darkgray
                    background_color = self.darkgray
                elif self.gameMap[i][j] == 2:
                    text_color = self.darkgray
                    background_color = self.white
                elif self.gameMap[i][j] == 4:
                    text_color = self.darkgray
                    background_color = self.lightyellow
                elif self.gameMap[i][j] == 8:
                    text_color = self.darkgray
                    background_color = self.lightorange
                elif self.gameMap[i][j] == 16:
                    text_color = self.darkgray
                    background_color = self.semilightorange
                elif self.gameMap[i][j] == 32:
                    text_color = self.white
                    background_color = self.orange
                elif self.gameMap[i][j] == 64:
                    text_color = self.white
                    background_color = self.red
                elif self.gameMap[i][j] == 128:
                    text_color = self.white
                    background_color = self.yellow
                elif self.gameMap[i][j] == 256:
                    text_color = self.white
                    background_color =  self.darkeryellow
                elif self.gameMap[i][j] == 512:
                    text_color = self.white
                    background_color = self.darkyellow
                elif self.gameMap[i][j] == 1024:
                    text_color = self.white
                    background_color = self.blue
                elif self.gameMap[i][j] == 2048:
                    text_color = self.white
                    background_color = self.purple
                else:
                    text_color = self.white
                    background_color = self.green
                value = number_font.render(f"{self.gameMap[i][j]}", True, text_color)
                pygame.draw.rect(self.dis, background_color, [j * self.block_sizes, i * self.block_sizes, self.block_sizes, self.block_sizes])
                self.dis.blit(value, [j * self.block_sizes + self.block_sizes / 2 - 40, i * self.block_sizes + self.block_sizes / 2 - 30])
        for i in range(0, len(self.gameMap)):
            pygame.draw.rect(self.dis, self.black, [0, i * self.block_sizes, self.dis_width, 5])
        for j in range(0, len(self.gameMap[i])):
            pygame.draw.rect(self.dis, self.black, [j * self.block_sizes, 0, 5, self.dis_height])
        pygame.draw.rect(self.dis, self.black, [0, len(self.gameMap[0]) * self.block_sizes - 5, self.dis_width, 5])
        pygame.draw.rect(self.dis, self.black, [len(self.gameMap) * self.block_sizes - 5, 0, 5, self.dis_height])
        pygame.display.update()
    def gameLoop(self):
        self.clock.tick(self.movement_speed)
        stop = False
        for _ in range(0, 3):
            self.add_block()

        while not stop:
            stop = self.controls()
            score = self.sumMap()
            self.printMap()
            self.clock.tick(self.movement_speed)
        
        return score
    def endScreen(self, score = 0):
        self.dis.fill(self.white)
        score_font = pygame.font.SysFont("comicsansms", 35)
        option_font = pygame.font.SysFont("comicsansms", 20)

        value = score_font.render(f"Game Over! Your Score: {score}", True, self.green)
        self.dis.blit(value, [0, 0])

        value2 = score_font.render(f"Press W to restart, Q to exit!", True, self.blue)
        self.dis.blit(value2, [0, 50])
        value3 = score_font.render(f"Press P to switch game!", True, self.blue)
        self.dis.blit(value3, [0, 85])

        pygame.display.update()

        play_again = False
        switch_game = False
        action = False
        while not action:
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    play_again = False
                    switch_game = False
                    action = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        play_again = False
                        switch_game = False
                        action = True
                    if event.key == pygame.K_w:
                        play_again = True
                        switch_game = False
                        action = True
                    if event.key == pygame.K_p:
                        play_again = True
                        switch_game = True
                        action = True
            pygame.display.flip()
            self.clock.tick(60)
        return play_again, switch_game

play = True
play_snake = True
while play:
    game_changed = True
    if play_snake:
        g = GameSnake()
        score = int(g.gameLoop())
        play, game_changed = g.endScreen(score= score)
        if game_changed:
            play_snake = False
    else:
        g = Game2048()
        score = int(g.gameLoop())
        play, game_changed = g.endScreen(score= score)
        if game_changed:
            play_snake = True

pygame.quit()