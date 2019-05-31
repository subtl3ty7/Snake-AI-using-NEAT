import pygame
from numpy.random import choice,randint
import random
import neat
import math
SCREENWIDTH = 500
SCREENHEIGHT = 500
SNAKESIZE = (SCREENWIDTH/50,SCREENHEIGHT/50)
SCORE = 0
BESTSCORE = 0
NODES = 0
MAX_FITNESS = 0
BEST_GENOME = 0
GENERATION = 1


class Snake:
    def __init__(self,display,head,prev):
        self.screen = display
        self.isHead = head
        self.next = None
        if head == True:
            self.x = choice([i for i in range(0,491,10)])
            self.y = choice([i for i in range(0,491,10)])
            self.direction = choice(["UP","DOWN","LEFT","RIGHT"])

        else:
            self.previous = prev
            if self.previous.direction == "UP":
                self.x = self.previous.x
                self.y = self.previous.y +10
            if self.previous.direction == "DOWN":
                self.x = self.previous.x
                self.y = self.previous.y -10
            if self.previous.direction == "LEFT":
                self.x = self.previous.x +10
                self.y = self.previous.y
            if self.previous.direction == "RIGHT":
                self.x = self.previous.x -10
                self.y = self.previous.y
            self.direction = self.previous.direction
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.prevx = self.x
        self.prevy = self.y


    def move(self):
        self.boundaryCheck()
        if self.isHead:
            self.prevy = self.y
            self.prevx = self.x
            if self.direction == "UP":
                self.y -=15
            if self.direction == "DOWN":
                self.y +=15
            if self.direction == "LEFT":
                self.x -=15
            if self.direction == "RIGHT":
                self.x +=15
            self.display()
        else:
            self.followPrevious()

    def changeDirection(self,input):
        self.direction = input



    def display(self):
       self.rect = pygame.draw.rect(self.screen,(0,0,0),[self.x,self.y,SNAKESIZE[0],SNAKESIZE[1]])

    def boundaryCheck(self):
        if (self.y < 0):
            return True
        if (self.y > 490):
            return True
        if (self.x < 0):
            return True
        if (self.x > 490):
            return True


    def followPrevious(self):
        self.prevx = self.x
        self.prevy = self.y
        self.x = self.previous.prevx
        self.y = self.previous.prevy
        self.changeDirection(self.previous.direction)
        self.display()

    def addTail(self):
        global NODES
        NODES+=1
        if self.next is None:
            self.next = Snake(self.screen,False,self)
        else:
            node = self.getNext()
            while True:
                temp = node.getNext()
                if temp is None:
                    node.next = Snake(self.screen,False,node)
                    break
                else:
                    node = node.getNext()



    def getNext(self):
        return self.next



class Food:


    def __init__(self,display):
        self.x = choice([i for i in range(0, 491, 10)])
        self.y = choice([i for i in range(0, 491, 10)])
        self.screen = display
        self.rect = pygame.Rect(self.x,self.y,SNAKESIZE[0],SNAKESIZE[1])


    def display(self):
       self.rect = pygame.draw.rect(self.screen,(255,0,0),[self.x,self.y,SNAKESIZE[0],SNAKESIZE[1]])

    def spawnNew(self):
        self.x = choice([i for i in range(0, 491, 10)])
        self.y = choice([i for i in range(0, 491, 10)])


def self_collide(snake):
    node = snake.getNext()
    if snake.rect.colliderect(node.rect):
        return True
    temp2 = node.getNext()
    while temp2 is not None:
        node = node.getNext()
        if snake.rect.colliderect(node.rect):
            return True
        temp2 = node.getNext()
    return False

def eats(food,snake):
    snake.x = snake.x
    snake.y = snake.y
    food.x = food.x
    food.y = food.y

    if snake.rect.colliderect(food.rect):
        return True
    return False


def game(genome,config):
    net = neat.nn.FeedForwardNetwork.create(genome,config)
    pygame.init()
    fpsclock = pygame.time.Clock()
    display = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Snake")
    snake = Snake(display,True,None)
    snake.addTail()
    snake.addTail()
    food = Food(display)
    gameOver = False
    global SCORE

    while not gameOver:
        display.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == 'QUIT':
                gameOver = True
                continue

        if pygame.key.get_pressed()[pygame.K_UP]:
            if snake.direction != "UP" and snake.direction != "DOWN":
                snake.changeDirection("UP")
        if pygame.key.get_pressed()[pygame.K_DOWN]:
                if snake.direction != "DOWN" and snake.direction != "UP":
                    snake.changeDirection("DOWN")
        if pygame.key.get_pressed()[pygame.K_LEFT]:
                if snake.direction != "LEFT" and snake.direction != "RIGHT":
                    snake.changeDirection("LEFT")
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
                if snake.direction != "RIGHT" and snake.direction != "LEFT":
                    snake.changeDirection("RIGHT")

        inputs = setInputs(snake,food)

        dist = math.sqrt(math.pow((snake.y - food.y),2) + math.pow((snake.x - food.x),2))

        fitness = SCORE - dist

        if eats(food,snake):
            SCORE+=50
            food.spawnNew()
            snake.addTail()


        if self_collide(snake) or snake.boundaryCheck():
            SCORE = 0
            return fitness

        output = net.activate(inputs)
        print(output[0])
        if output[0] <= 0.3:
            if snake.direction != "UP" and snake.direction != "DOWN":
                snake.changeDirection("UP")
        elif output[0] <= 0.6:
            if snake.direction != "DOWN" and snake.direction != "UP":
                snake.changeDirection("DOWN")
        elif output[0] <= 1:
            if snake.direction != "LEFT" and snake.direction != "RIGHT":
                snake.changeDirection("LEFT")
        elif output[0] <= 10:
            if snake.direction != "RIGHT" and snake.direction != "LEFT":
                snake.changeDirection("RIGHT")

        food.display()
        snake.move()
        SCORE+=10
        if snake.next is not None:
            node = snake.getNext()
            node.move()
            temp2 = node.getNext()
            while temp2 is not None:
                node = node.getNext()
                node.move()
                temp2 = node.getNext()
        pygame.display.update()
        fpsclock.tick(10)

    pygame.quit()
    quit()

def isLeftFree(snake):
    snake.x = snake.x
    leftX = snake.x - 10
    node = snake.getNext()
    if node.x == leftX and node.y == snake.y:
        return 0
    temp2 = node.getNext()
    while temp2 is not None:
        node = node.getNext()
        if node.x == leftX and node.y == snake.y:
            return 0
        temp2 = node.getNext()
    if leftX < 0:
        return 0
    return 1

def isRightFree(snake):
    snake.x = snake.x
    rightX = snake.x + 10
    node = snake.getNext()
    if node.x == rightX and node.y == snake.y:
        return 0
    temp2 = node.getNext()
    while temp2 is not None:
        node = node.getNext()
        if node.x == rightX and node.y == snake.y:
            return 0
        temp2 = node.getNext()
    if rightX >= 500:
        return 0
    return 1

def isUpFree(snake):
    snake.x = snake.x
    upY = snake.y - 10
    node = snake.getNext()
    if node.y == upY and node.x == snake.x:
        return 0
    temp2 = node.getNext()
    while temp2 is not None:
        node = node.getNext()
        if node.y == upY and node.x == snake.x:
            return 0
        temp2 = node.getNext()
    if upY < 0:
        return 0
    return 1

def isDownFree(snake):
    snake.x = snake.x
    downY = snake.y + 10
    node = snake.getNext()
    if node.y == downY and node.x == snake.x:
        return 0
    temp2 = node.getNext()
    while temp2 is not None:
        node = node.getNext()
        if node.y == downY and node.x == snake.x:
            return 0
        temp2 = node.getNext()
    if downY >= 500:
        return 0
    return 1

def isFoodUp(snake,food):
    if snake.y > food.y:
        return 1
    return 0
def isFoodDown(snake,food):
    if snake.y < food.y:
        return 1
    return 0
def isFoodLeft(snake,food):
    if snake.x > food.x:
        return 1
    return 0
def isFoodRight(snake,food):
    if snake.x < food.x:
        return 1
    return 0
def setInputs(snake,food):

    return (isUpFree(snake),isDownFree(snake),isLeftFree(snake),isRightFree(snake),
            isFoodUp(snake,food),isFoodDown(snake,food),isFoodLeft(snake,food),isFoodRight(snake,food))


def eval_genomes(genomes,config):
    i = 0

    global SCORE
    global GENERATION,MAX_FITNESS,BEST_GENOME
    GENERATION+=1
    for genome_id, genome in genomes:
        genome.fitness = game(genome,config)
        print("Gen : %d Genome # : %d  Fitness : %f Max Fitness : %f" % (GENERATION, i, genome.fitness, MAX_FITNESS))

        if genome.fitness >= MAX_FITNESS:
            MAX_FITNESS = genome.fitness

            BEST_GENOME = genome
        SCORE = 0

        i+=1

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,

                     neat.DefaultSpeciesSet, neat.DefaultStagnation,

                     'config')

pop = neat.Population(config)

stats = neat.StatisticsReporter()

pop.add_reporter(stats)



if __name__== "__main__":
    winner = pop.run(eval_genomes, 30)