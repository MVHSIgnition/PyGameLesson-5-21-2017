import pygame
import random

# start pygame up
pygame.init()

# some constants
WIDTH = 1000
HEIGHT = 500
GAME_TITLE = "Snake Game"
FPS = 15

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

INCREMENT = 25
UNIT_SIZE = 20
GROW_LENGTH = 1

RIGHT, UP, LEFT, DOWN = range(4)

# sprites
class Unit(pygame.sprite.Sprite):
    def __init__(self, color, position, dimensions):
        pygame.sprite.Sprite.__init__(self)

        # set the image of the sprite
        self.image = pygame.Surface(dimensions)
        self.image.fill(color)

        # move the sprite to the correct location
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def draw(self, screen):
        # displays image to the screen
        screen.blit(self.image, self.rect)

class SnakeUnit(Unit):
    # class for the boxes in the snake body
    def __init__(self, position, dimensions, direction=-1):
        Unit.__init__(self, GREEN, position, dimensions) #defaults color to GREEN

        # self.dir stores the direction the unit is facing
        # can be used to replace boxes with images in the future
        self.dir = direction

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

def generate_food_position():
    # generate a random location for the food
    x_max = int(WIDTH/INCREMENT) - 1
    x = random.randint(0, x_max)*INCREMENT
    y_max = int(HEIGHT/INCREMENT) - 1
    y = random.randint(0, y_max)*INCREMENT
    return (x, y)

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
    rect = SnakeUnit( (x, y), (UNIT_SIZE, UNIT_SIZE), direction )
    body_list.append(rect)
    body_group.add(rect)

    # get rid of the last unit if snake doesn't need to grow
    if food.get_grow() == 0:
        body_group.remove(body_list.pop(0))

# create a game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# initialize internal clock (for calculating fps)
clock = pygame.time.Clock()

# initialize list for body units
body_list = []
body_list.append( SnakeUnit( (0,0), (UNIT_SIZE, UNIT_SIZE), -1 ) )
# group body units into one big sprite
body_group = pygame.sprite.Group(body_list)
# set snake to not be moving in any direction to start
direction = -1
# create the first food box
food = Food( generate_food_position(), (UNIT_SIZE, UNIT_SIZE) )

# main game loop
state = "playing"
done = False
while not done:
    # tells PyGame how often to update
    clock.tick(FPS)

    # if x button pressed, quit out of while loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if state == "playing":
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

        # draw the sprites
        body_group.draw(screen)
        food.draw(screen)

    # update the screen!
    pygame.display.flip()

# quit pygame
pygame.quit()
