#Runjie Chu   Xi Hu

'''
How to use it
In this program, we design a snake game, using keyboard letter w, a, s, d to represents turn up, turn left, turn down, turn right respectively
When game is over, you can press R to restart or Q to quit.
'''

import pygame,sys,random

'''This part we will define class Food whose function is to generate food on the screen randomly.
By the way, the color patten of snake will have the same color pattern of rainbow.'''

class Food(object):
    def __init__(self):
        self.index=4
        self.xyz = [(0,0),(0,0,0)]
        self.md_xyz()

# get the value of position and color for snake
    def md_xyz(self):
        color = self.randomcolor()
        self.xyz = [ (random.randint(0,49), random.randint(0,29)),   color]

#we pick seven colors and use them to draw the snake in sequence
    def randomcolor(self):
        colors = [(255,0,0),(255,165,0),(255,255,0),(0,255,0),(0,127,255),(0,0,255),(139,0,255)]
        if self.index != (len(colors)-1):
            self.index+=1
            return colors[self.index]
        else:
            self.index=0
            return colors[self.index]
# draw food
    def draw(self):
        color = self.xyz[1]
        x = self.xyz[0][0]*20
        y = self.xyz[0][1]*20
        pygame.draw.rect(screen, color, (x,y,20,20) ,0)

'''In class Snake we define the method move, check_food, check_self and draw method. We also attach sound effect
when the snake eat the food and when the snake die.'''
class Snake(object):

    def __init__(self):
        self.food = Food()
        self.image=pygame.image.load('slug_logo.jpg').convert()
        self.eat_food_sound = pygame.mixer.Sound('food.wav') 
        self.death_sound = pygame.mixer.Sound('death.wav')
        self.clock = pygame.time.Clock()
        self.body = [ [(15, 13), (16, 13), (17, 13), (18, 13), (19, 13)],  \
                      [(0,127,255),(0,255,0),(255,255,0),(255,165,0),(255,0,0)]]
        self.direction = "a" 
        self.live = True 
        self.score = 0


    '''When the snake is moving in the screen, the program will check the value of self.live, if it's true then program turns to check direction.
    According to the direction, the body position of the snake will change. Then it will check whether the head position of the snake is same
    with the food. If true, the food will add into the body of the snake and program will generate another food. After this, the program will check
    whether the snake eats itself. If true, self.value becomes False the program stops

    '''
# how the snake will move with different keyboard press
    def move(self):
        head = (0,0)
        x = self.body[0][0][0]
        y = self.body[0][0][1]
        if self.live:
            if self.direction == "a": head = (x-1 if x>0 else 49, y)
            if self.direction == "d": head = (x+1 if x<49 else 0, y)
            if self.direction == "w": head = (x, y-1 if y>0 else 29)
            if self.direction == "s": head = (x, y+1 if y<29 else 0)

            if self.check_food():
                self.body[0].insert(0,head)
                self.body[1].insert(0,self.food.xyz[1])
                self.food.md_xyz()
            else:
                self.body[0].pop() 
                self.body[0].insert(0,head)
            self.check_self()
            self.draw()
        self.clock.tick(8)


# to check whether the snake eat food successfully
    def check_food(self):
        if self.body[0][0] == self.food.xyz[0]:
            self.eat_food_sound.play()
            self.score += 100
            return True

# to check whether the snake eat itself
    def check_self(self):
        if self.body[0][0] in self.body[0][1:]:
            self.death_sound.play()
            self.live = False
            return True

# draw snake & show scores in screen
    def draw(self):
        screen.fill((255,255,255))
        screen.blit(self.image,(325,150))

        for x,y in self.body[0]:
            color = self.body[1][ self.body[0].index((x,y)) ]
            pygame.draw.rect(screen, color, (x*20,y*20,20,20),0)

        self.food.draw()
        screen.blit(pygame.font.SysFont(None, 25).render("score : " + str(self.score),True,(0,0,0)),(10,10))

        if not self.live:
            screen.blit(pygame.font.SysFont(None, 25).render("You die! Press R to restart or Q to quit",True,(0,0,0)),(320,100))

        pygame.display.flip()


# program starts

pygame.init()
pygame.display.set_mode((1000,600))
screen = pygame.display.get_surface()

snake = Snake()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and snake.direction != "s": snake.direction = "w"
            if event.key == pygame.K_s and snake.direction != "w": snake.direction = "s"
            if event.key == pygame.K_a and snake.direction != "d": snake.direction = "a"
            if event.key == pygame.K_d and snake.direction != "a": snake.direction = "d"
            if event.key == pygame.K_r: snake.__init__()

    snake.move()







