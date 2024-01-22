import pygame
import sys
from pathlib import Path
import json
from territory import Level_01
from player import Player


class GameWindow:
    def __init__(self, max_screen_size):
        pygame.init()
        self.screen = self.apply_settings(max_screen_size)
        self.display_size = pygame.display.get_surface().get_size()

        self.width = self.display_size[0]
        self.height = self.display_size[1]

        self.player = Player()

    def apply_settings(self, max_screen_size):
        json_path = Path(__file__).parent / "user_data" / "settings.json"

        with json_path.open("r", encoding="utf-8") as json_file:
            settings = json.load(json_file)
            resolution = None
            screen = None
            fullscreen = False
            # vsync = False

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
                elif key == "Ограничение по FPS":
                    self.fps = value
                # elif key == "Вертикальная синхронизация":
                #     vsync = True

        if not fullscreen:
            if (
                resolution[0] >= max_screen_size.width()
                and resolution[1] >= max_screen_size.height()
            ):
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                screen = (
                    pygame.display.set_mode(max_screen_size.width()),
                    max_screen_size.height(),
                )
        else:
            screen = pygame.display.set_mode(
                (resolution[0], resolution[1]), pygame.FULLSCREEN
            )
        return screen

    def main(self):
        pygame.display.set_caption("Платформер")

        level_list = []
        level_list.append(Level_01(self.player))
        current_level_no = 0
        current_level = level_list[current_level_no]

        active_sprite_list = pygame.sprite.Group()
        self.player.level = current_level

        self.player.rect.x = 1000
        self.player.rect.y = self.height - self.player.rect.height
        active_sprite_list.add(self.player)

        running = True
        flag_sountrack = False

        clock = pygame.time.Clock()
        pygame.mixer.music.load("sounds/ost_soundtrack.mp3")
        pygame.mixer.music.play(-1, 0.0, 1)

        while running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        flag_sountrack = not flag_sountrack
                        if flag_sountrack:
                            pygame.mixer.music.pause()
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.go_left()
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.go_right()
                    if (
                        event.key == pygame.K_UP
                        or event.key == pygame.K_SPACE
                        or event.key == pygame.K_w
                    ):
                        self.player.jump()
                    if event.key == pygame.K_ESCAPE:
                        running = False

                elif event.type == pygame.KEYUP:
                    if (
                        event.key == pygame.K_LEFT or event.key == pygame.K_a
                    ) and self.player.change_x < 0:
                        self.player.stop()
                    if (
                        event.key == pygame.K_RIGHT or event.key == pygame.K_d
                    ) and self.player.change_x > 0:
                        self.player.stop()

            CAMERA_LEFT_MARGIN = self.width * 0.48
            CAMERA_RIGHT_MARGIN = self.width * 0.52

            self.player_center_x = self.player.rect.centerx
            if self.player_center_x > CAMERA_RIGHT_MARGIN:
                diff = self.player_center_x - CAMERA_RIGHT_MARGIN
                self.player.rect.centerx = CAMERA_RIGHT_MARGIN
                current_level.shift_world(-diff)
            elif self.player_center_x < CAMERA_LEFT_MARGIN:
                diff = CAMERA_LEFT_MARGIN - self.player_center_x
                self.player.rect.centerx = CAMERA_LEFT_MARGIN
                current_level.shift_world(diff)

            active_sprite_list.update()
            current_level.update()

            current_level.draw(self.screen)
            active_sprite_list.draw(self.screen)

            clock.tick(self.fps)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = GameWindow()
    sys.exit(game.main())
