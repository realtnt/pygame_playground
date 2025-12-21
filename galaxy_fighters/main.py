import os

import pygame

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Fighters")

WIN_FONT = pygame.font.SysFont("comicsans", 60)
HEALTH_FONT = pygame.font.SysFont("comicsans", 20)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("galaxy_fighters", "assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("galaxy_fighters", "assets", "Gun+Silencer.mp3"))

FPS = 60
SPACESHIP_VEL = 5
BULLET_VEL = 8
MAX_BULLETS = 3

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 41
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("galaxy_fighters", "assets", "spaceship_yellow.png")
)
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    90,
)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("galaxy_fighters", "assets", "spaceship_red.png")
)
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    -90,
)

SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join("galaxy_fighters", "assets", "space.png")),
    (WIDTH, HEIGHT),
)


def draw_window(red, yellow, yellow_bullets, red_bullets, yellow_lives, red_lives):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, "white", BORDER)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, "yellow", bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, "red", bullet)

    yellow_lives_text = HEALTH_FONT.render(f"Lives: {yellow_lives}", 1, "yellow")
    red_lives_text = HEALTH_FONT.render(f"Lives: {red_lives}", 1, "red")

    WIN.blit(yellow_lives_text, (10, 10))
    WIN.blit(red_lives_text, (WIDTH - red_lives_text.get_width() - 10, 10))

    pygame.display.update()


def draw_winner(text):
    winner_text = WIN_FONT.render(text, 1, "white")
    WIN.blit(
        winner_text,
        (
            WIDTH / 2 - winner_text.get_width() / 2,
            HEIGHT / 2 - winner_text.get_height() / 2,
        ),
    )
    pygame.display.update()
    pygame.time.delay(5000)


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if bullet.x - bullet.width > WIDTH:
            yellow_bullets.remove(bullet)
        elif red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if bullet.x + bullet.width < 0:
            red_bullets.remove(bullet)
        elif yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)


def yellow_handle_movement(keys, ship):
    if keys[pygame.K_a] and ship.x - SPACESHIP_VEL > 0:
        ship.x -= SPACESHIP_VEL
    if (
        keys[pygame.K_d]
        and ship.x + SPACESHIP_VEL + ship.width < BORDER.x + BORDER.width
    ):
        ship.x += SPACESHIP_VEL
    if keys[pygame.K_w] and ship.y - SPACESHIP_VEL > 0:
        ship.y -= SPACESHIP_VEL
    if keys[pygame.K_s] and ship.y + SPACESHIP_VEL + ship.height < HEIGHT:
        ship.y += SPACESHIP_VEL


def red_handle_movement(keys, ship):
    if keys[pygame.K_LEFT] and ship.x - SPACESHIP_VEL > BORDER.x + BORDER.width:
        ship.x -= SPACESHIP_VEL
    if keys[pygame.K_RIGHT] and ship.x + SPACESHIP_VEL + ship.width < WIDTH:
        ship.x += SPACESHIP_VEL
    if keys[pygame.K_UP] and ship.y - SPACESHIP_VEL > 0:
        ship.y -= SPACESHIP_VEL
    if keys[pygame.K_DOWN] and ship.y + SPACESHIP_VEL + ship.height < HEIGHT:
        ship.y += SPACESHIP_VEL


def main():
    red = pygame.Rect(
        WIDTH - WIDTH / 4 - SPACESHIP_WIDTH,
        HEIGHT / 2 - SPACESHIP_HEIGHT / 2,
        SPACESHIP_WIDTH,
        SPACESHIP_HEIGHT,
    )
    yellow = pygame.Rect(
        WIDTH / 4, HEIGHT / 2 - SPACESHIP_HEIGHT / 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT
    )

    run = True
    clock = pygame.time.Clock()

    yellow_bullets = []
    red_bullets = []

    yellow_lives = 9
    red_lives = 9

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,
                        yellow.y + yellow.height // 2 - 2,
                        10,
                        5,
                    )
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
            if event.type == YELLOW_HIT:
                yellow_lives -= 1
                BULLET_HIT_SOUND.play()
            if event.type == RED_HIT:
                red_lives -= 1
                BULLET_HIT_SOUND.play()
                
        winner_text_string = ""
        if yellow_lives <= 0:
            winner_text_string = "Red Wins!"
        if red_lives <= 0:
            winner_text_string = "Yellow Wins!"
        if winner_text_string != "":
            draw_winner(winner_text_string)
            break

        keys = pygame.key.get_pressed()
        yellow_handle_movement(keys, yellow)
        red_handle_movement(keys, red)

        if keys[pygame.K_x]:
            pygame.quit()

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, yellow_bullets, red_bullets, yellow_lives, red_lives)

    main()


if __name__ == "__main__":
    main()
