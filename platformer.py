import pygame
import sys
from pathlib import Path
import json
from territory import Level_01
from player import Player


class GameWindow:
    def apply_settings(self):
        json_path = Path(__file__).parent / "user_data" / "settings.json"
        with json_path.open("r", encoding="utf-8") as json_file:
            settings = json.load(json_file)
            resolution = None
            screen = None
            fullscreen = False
            vsync = False
            for key, value in settings.items():
                if key == "Громкость звука":
                    pygame.mixer.music.set_volume(value / 100)
                elif key == "Уровень сложности":
                    pass
                elif key == "Разрешение экрана":
                    resolution = (value[0], value[1])
                elif key == "Качество текстур":
                    pass
                elif key == "Режим отображения":
                    if value == "Полноэкранный":
                        fullscreen = True
                elif key == "Вертикальная синхронизация":
                    vsync = True

            flags = 0
            if fullscreen:
                flags |= pygame.FULLSCREEN
            if vsync:
                flags |= pygame.SCALED

            screen = pygame.display.set_mode(resolution, flags)
            return screen

    def main(self):
        pygame.init()

        screen = self.apply_settings()
        display_size = pygame.display.get_surface().get_size()

        pygame.display.set_caption("Платформер")
        player = Player()
        level_list = []
        level_list.append(Level_01(player))
        current_level_no = 0
        current_level = level_list[current_level_no]

        active_sprite_list = pygame.sprite.Group()
        player.level = current_level

        player.rect.x = 340
        player.rect.y = display_size[1] - player.rect.height
        active_sprite_list.add(player)

        running = False

        clock = pygame.time.Clock()

        while not running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = True

                elif event.type == pygame.KEYDOWN:
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

            CAMERA_LEFT_MARGIN = display_size[0] * 0.48
            CAMERA_RIGHT_MARGIN = display_size[0] * 0.52

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
    game = GameWindow()
    sys.exit(game.main())
