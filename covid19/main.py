import random
import time
import os

import pygame

from . import constants as k

pygame.font.init()

pygame.display.set_caption("Covid19")

WIN = pygame.display.set_mode((k.WIDTH, k.HEIGHT))
BG = pygame.transform.scale(
    pygame.image.load(os.path.join('covid19', 'bg.jpeg')), (k.WIDTH, k.HEIGHT)
)
FONT = pygame.font.SysFont("comicsans", 30)


def draw(player, elapsed_time, stars, hits, hit_text_string, bullets):
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))
    hits_text = FONT.render(str(hits), 1, "white")
    WIN.blit(hits_text, (k.WIDTH / 2, 10))
    pygame.draw.rect(WIN, "red", player)
    hit_text = FONT.render(hit_text_string, 1, "white")
    WIN.blit(
        hit_text,
        (
            k.WIDTH / 2 - hit_text.get_width() / 2,
            k.HEIGHT / 2 - hit_text.get_height() / 2,
        ),
    )

    for star in stars:
        pygame.draw.rect(WIN, star[1], star[0])

    for bullet in bullets:
        pygame.draw.rect(WIN, "white", bullet)

    pygame.display.update()


def main():
    run = True

    player = pygame.Rect(
        20, k.HEIGHT / 2 - k.PLAYER_HEIGHT / 2, k.PLAYER_WIDTH, k.PLAYER_HEIGHT
    )
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 500
    star_count = 0

    bullets = []
    stars = []
    hit = False
    hits = 0
    hit_display = 0
    hit_text = ""
    bullet_gap = 3
    fired = bullet_gap
    simul_bullets_count = 1

    while run:
        star_count += clock.tick(k.FPS)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_y = random.randint(0, k.HEIGHT - k.STAR_HEIGHT)
                star = pygame.Rect(
                    k.WIDTH + k.STAR_WIDTH, star_y, k.STAR_WIDTH, k.STAR_HEIGHT
                )
                my_tuple = (star, random.choice(k.COLORS))
                stars.append(my_tuple)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - k.PLAYER_VEL >= 0:
            player.x -= k.PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + k.PLAYER_VEL + player.width <= k.WIDTH:
            player.x += k.PLAYER_VEL
        if keys[pygame.K_UP] and player.y - k.PLAYER_VEL >= 0:
            player.y -= k.PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + k.PLAYER_VEL + player.height <= k.HEIGHT:
            player.y += k.PLAYER_VEL
        if keys[pygame.K_SPACE]:
            fired += 1
            if fired > bullet_gap:
                fired = 0
            if len(bullets) < simul_bullets_count and fired >= bullet_gap:
                bullet = pygame.Rect(
                    player.x, player.y, k.BULLET_WIDTH, k.BULLET_HEIGHT
                )
                bullets.append(bullet)

        if keys[pygame.K_x]:
            run = False

        for star in stars[:]:
            star[0].x -= k.STAR_VEL
            if star[0].x < -k.WIDTH:
                stars.remove(star)
            elif star[0].x + star[0].width >= player.x and star[0].colliderect(player):
                stars.remove(star)
                hit = True
                if star[1] == "red":
                    hits += 10
                elif star[1] == "yellow":
                    hits -= 10
                elif star[1] == "cyan":
                    hits = 0
                elif star[1] == "orange":
                    simul_bullets_count += 1
                else:
                    hits += 1
                break

        for bullet in bullets[:]:
            bullet.x += k.BULLET_VEL
            if bullet.x >= k.WIDTH + k.BULLET_WIDTH:
                bullets.remove(bullet)

        if hit:
            hit_text = "Yeeha"
            hit_display += 1
            if hit_display > k.FPS * k.HIT_DELAY:
                hit = False
                hit_display = 0
                hit_text = ""

        draw(player, elapsed_time, stars, hits, hit_text, bullets)
    pygame.quit()


if __name__ == "__main__":
    main()
