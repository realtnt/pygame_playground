import os

import pygame

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Fighters")

BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)

FPS = 60
SPACESHIP_VEL = 5

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("galaxy_fighters", "assets", "spaceship_yellow.png")
)
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("galaxy_fighters", "assets", "spaceship_red.png")
)
RED_SPACESHIP =  pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)

def draw_window(red, yellow):
    WIN.fill("black")
    pygame.draw.rect(WIN, "white", BORDER)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    
    pygame.display.update()
    
def yellow_handle_movement(keys, yellow):
    if keys[pygame.K_w]:
        yellow.y -= SPACESHIP_VEL
    if keys[pygame.K_s]:
        yellow.y += SPACESHIP_VEL
    if keys[pygame.K_a]:
        yellow.x -= SPACESHIP_VEL
    if keys[pygame.K_d]:
        yellow.x += SPACESHIP_VEL

def red_handle_movement(keys, red):
    if keys[pygame.K_UP]:
        red.y -= SPACESHIP_VEL
    if keys[pygame.K_DOWN]:
        red.y += SPACESHIP_VEL
    if keys[pygame.K_LEFT]:
        red.x -= SPACESHIP_VEL
    if keys[pygame.K_RIGHT]:
        red.x += SPACESHIP_VEL

def main():
    red = pygame.Rect(WIDTH - WIDTH/4 - SPACESHIP_WIDTH, HEIGHT/2 - SPACESHIP_HEIGHT/2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(WIDTH/4, HEIGHT/2 - SPACESHIP_HEIGHT/2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        yellow_handle_movement(keys, yellow)
        red_handle_movement(keys, red)
        
        if keys[pygame.K_x]:
            run = False

        draw_window(red, yellow)


if __name__ == "__main__":
    main()
