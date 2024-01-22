import pygame
from pathlib import Path
import json


class Level:
    def __init__(self, player, bg_image_file):
        self.display_size = pygame.display.get_surface().get_size()
        self.bg = pygame.transform.scale(
            pygame.image.load(bg_image_file).convert_alpha(), self.display_size
        )
        self.platform_list = pygame.sprite.Group()
        self.player = player
        self.world_shift_x = 0

    def update(self):
        self.platform_list.update()

    def shift_world(self, shift_x):
        self.world_shift_x += shift_x
        for platform in self.platform_list:
            platform.rect.x += shift_x

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        self.platform_list.draw(screen)


class Level_01(Level):
    def __init__(self, player, map_path):
        super().__init__(player, "materials/backgrounds/world_background.png")

        self.map_path = map_path

        platform_image = pygame.image.load(
            "materials/textures/colored_ground_texture.png"
        ).convert_alpha()

        self.block_width = self.display_size[0] * 0.70 * 0.05
        self.block_height = self.display_size[1] * 0.75 * 0.077

        level = self.load_map()

    def load_textures(self):
        with Path(self.map_path).open("r", encoding="utf-8") as json_file:
            level = json.load(json_file)
        return level

    def load_map(self):
        textures = self.load_textures()

        for dc in textures:
            for image_path, value in dc.items():
                print(image_path, value)


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
