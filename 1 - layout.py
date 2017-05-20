import pygame

# start pygame up
pygame.init()

# some constants
WIDTH = 1000
HEIGHT = 500
GAME_TITLE = "Snake Game"
FPS = 15

# create a game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# initialize internal clock (for calculating fps)
clock = pygame.time.Clock()

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

# quit pygame
pygame.quit()
