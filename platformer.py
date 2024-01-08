import pygame
import sys
from territory import Level_01
from player import Player
from const import SCREEN_HEIGHT, SCREEN_WIDTH


def main():
    pygame.init()
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Платформер")
    player = Player()
    level_list = []
    level_list.append(Level_01(player))
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    running = False
    flag_sountrack = False

    clock = pygame.time.Clock()
    pygame.mixer.music.load("sounds/ost_soundtrack.mp3")
    pygame.mixer.music.play(-1, 0.0, 1)

    while not running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    flag_sountrack = not flag_sountrack
                    if flag_sountrack:
                        pygame.mixer.music.stop()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.go_left()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.go_right()
                if (
                    event.key == pygame.K_UP
                    or event.key == pygame.K_SPACE
                    or event.key == pygame.K_w
                ):
                    player.jump()

            elif event.type == pygame.KEYUP:
                if (
                    event.key == pygame.K_LEFT or event.key == pygame.K_a
                ) and player.change_x < 0:
                    player.stop()
                if (
                    event.key == pygame.K_RIGHT or event.key == pygame.K_d
                ) and player.change_x > 0:
                    player.stop()

        CAMERA_LEFT_MARGIN = SCREEN_WIDTH * 0.48
        CAMERA_RIGHT_MARGIN = SCREEN_WIDTH * 0.52

        player_center_x = player.rect.centerx
        if player_center_x > CAMERA_RIGHT_MARGIN:
            diff = player_center_x - CAMERA_RIGHT_MARGIN
            player.rect.centerx = CAMERA_RIGHT_MARGIN
            current_level.shift_world(-diff)
        elif player_center_x < CAMERA_LEFT_MARGIN:
            diff = CAMERA_LEFT_MARGIN - player_center_x
            player.rect.centerx = CAMERA_LEFT_MARGIN
            current_level.shift_world(diff)

        active_sprite_list.update()
        current_level.update()

        current_level.draw(screen)
        active_sprite_list.draw(screen)
        clock.tick(45)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    sys.exit(main())
