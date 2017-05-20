import pygame

# start pygame up
pygame.init()

# some constants
WIDTH = 1000
HEIGHT = 500
GAME_TITLE = "Snake Game"
FPS = 15

WHITE = (255, 255, 255)

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

# create a game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# initialize internal clock (for calculating fps)
clock = pygame.time.Clock()

# main game loop
state = "playing"
done = False
box = Unit((255,0,0), (100, 50), (200, 300))
while not done:
    # tells PyGame how often to update
    clock.tick(FPS)

    # if x button pressed, quit out of while loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    
    screen.fill((255, 255, 255))
    box.draw(screen)
    # update the screen!
    pygame.display.flip()

# quit pygame
pygame.quit()
