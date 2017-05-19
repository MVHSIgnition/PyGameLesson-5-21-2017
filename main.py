import pygame
import math
import sys
import random

# define constants used throughout the program
FRAMES_PER_SECOND = 15
WIDTH = 1000
HEIGHT = 500

WHITE = (255,   255,    255)
BLACK = (0,     0,      0)
GREEN = (40,    255,    40)
RED =   (255,    40,    40)

INCREMENT = 25
BOX_SIZE = 20
GROW_LENGTH = 1
RIGHT, UP, LEFT, DOWN = range(4)
#START_POSITION = (0, 0)

# start pygame up
pygame.init()

class Unit(pygame.sprite.Sprite):
    # base class for the snake body and food boxes
    def __init__(self, color, position, dimensions, direction=-1):
        pygame.sprite.Sprite.__init__(self)

        # set the image of the sprite
        self.image = pygame.Surface(dimensions)
        self.image.fill(color)

        # move the sprite to the correct location
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class SnakeUnit(Unit):
    # class for the boxes in the snake body
    head = pygame.image.load('head.png')
    tail = pygame.image.load('tail.png')
    def __init__(self, position, dimensions, direction=-1):
        Unit.__init__(self, GREEN, position, dimensions)

        # define variables used by this sprite
        self.color = GREEN
        self.dir = direction
        self.dimensions = dimensions

    def update(self, body_list):
        index = body_list.index(self) #find which index this unit is

        if index == len(collisions)-1:
            # set image to head
            self.image = pygame.transform.rotate(self.head, self.dir*90)
        elif index == 0:
            # set image to tail
            self.image = pygame.transform.rotate(self.tail, self.dir*90)
        else:
            # body unit
            self.image = pygame.Surface(self.dimensions)
            self.image.fill(self.color)

class Food(Unit):
    # class for the food box
    def __init__(self, position, dimensions):
        Unit.__init__(self, RED, position, dimensions)

        # define sprite variables
        self.grow = 0   # length left for the snake to grow (after eating food)
        self.score = 0  # score of the user

    def update(self, collisions):
        # subtract from length still needed to grow
        if self.grow != 0: self.grow -= 1 
        if collisions != []:
            # when snake touches food,
            # move food to random location,
            # tell snake to grow,
            # and increase score
            x, y = generate_food_position()
            self.rect.x = x
            self.rect.y = y
            self.grow = GROW_LENGTH
            self.score += 1

    def get_score(self):
        return self.score

    def get_grow(self):
        return self.grow

def update_direction(direction):
    # get x and y position of the "head" unit
    x = body_list[-1].rect.x
    y = body_list[-1].rect.y

    # determine next unit location
    if direction == RIGHT: x += INCREMENT
    elif direction == UP: y -= INCREMENT
    elif direction == LEFT: x -= INCREMENT
    elif direction == DOWN: y+= INCREMENT
    elif direction == -1: return

    # add a new unit to the front of snake
    rect = SnakeUnit((x, y), (BOX_SIZE, BOX_SIZE), direction = direction)
    body_list.append(rect)
    body_group.add(rect)

    # ...and get rid of the last unit if snake doesn't need to grow
    if food.get_grow() == 0:
        body_group.remove(body_list.pop(0))
    
def generate_food_position():
    # generate a random location for the food
    x_max = int(WIDTH/INCREMENT) - 1
    x = random.randint(0, x_max)*INCREMENT
    y_max = int(HEIGHT/INCREMENT) - 1
    y = random.randint(0, y_max)*INCREMENT
    return (x, y)

# create window WIDTH x HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# set title of the window
GAME_TITLE = "My Snake Game"
pygame.display.set_caption(GAME_TITLE)

# initialize internal clock (for calculating fps)
clock = pygame.time.Clock()

# initialize game
body_list = []
for i in range(3):
    pos = (0, i*INCREMENT)
    body_list.append(SnakeUnit(pos, (BOX_SIZE, BOX_SIZE)))
body_group = pygame.sprite.Group(body_list)
direction = -1
food = Food(generate_food_position(), (BOX_SIZE, BOX_SIZE))

done = False
condition = "playing"
while not done:
    # tells PyGame how often to update
    clock.tick(FRAMES_PER_SECOND)

    # update the score
    pygame.display.set_caption(GAME_TITLE + "| Score:%d" % (food.get_score()))

    # if x button pressed, quit out of while loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    # draw everything
    if condition == "playing":
        # get key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and direction != LEFT: direction = RIGHT
        elif keys[pygame.K_UP] and direction != DOWN: direction = UP
        elif keys[pygame.K_LEFT] and direction != RIGHT: direction = LEFT
        elif keys[pygame.K_DOWN] and direction != UP: direction = DOWN

        # clear the screen every frame
        screen.fill(WHITE)

        # update the direction of the snake
        update_direction(direction)

        # check if food has been eaten
        food_collisions = pygame.sprite.spritecollide(food, body_group, False)
        food.update(food_collisions)

        # update the snake body
        body_group.update(body_list)

        # draw the sprites
        body_group.draw(screen)
        food.draw(screen)

        # check if snake is outside the boundaries or has hit itself
        body_collisions = pygame.sprite.spritecollide(body_list[-1], body_group, False)
        # subtract increment because coordinates are calculated from top left
        outside_boundaries = body_list[-1].rect.x > WIDTH-INCREMENT or body_list[-1].rect.x < 0 or body_list[-1].rect.y > HEIGHT-INCREMENT or body_list[-1].rect.y < 0
        if len(body_collisions) == 2 or outside_boundaries:
            condition = "lost"
        
    elif condition == "lost":
        # Display message to user, notifying them of their loss
        font = pygame.font.Font(pygame.font.get_default_font(), 30)
        text = font.render("You lost. Score: %d.Press spacebar to play again..." % (food.score), True, BLACK)
        screen.blit(text, (30, 30))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            # reset the game
            condition = "playing"
            body_list = []
            for i in range(3):
                pos = (0, i*INCREMENT)
                body_list.append(SnakeUnit(pos, (BOX_SIZE, BOX_SIZE)))
            body_group = pygame.sprite.Group(body_list)
            direction = -1
            food = Food(generate_food_position(), (BOX_SIZE, BOX_SIZE))

    # update the display
    pygame.display.flip()

# must have this to unload pygame, and exit the game
pygame.quit()
