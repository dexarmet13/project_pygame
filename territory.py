import pygame
from pathlib import Path
import json
import numpy as np


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

        self.block_width = self.display_size[0] / 21
        self.block_height = self.display_size[1] / 14

        self.load_map()

    def load_textures(self):
        with Path(self.map_path).open("r", encoding="utf-8") as json_file:
            level = json.load(json_file)
        return level

    def load_map(self):
        textures = self.load_textures()

        image_cache = {}

        for i, dc in enumerate(textures):
            for image_path, value in dc.items():
                if image_path not in image_cache:
                    image_cache[image_path] = pygame.image.load(
                        image_path
                    ).convert_alpha()

                for block in value:
                    position = self.grid_to_pixel(block[0], block[1])
                    platform = Platform(
                        self.block_width,
                        self.block_height,
                        position[0]
                        + ((self.display_size[0] - self.block_width) * i),
                        position[1],
                        image_cache[image_path],
                    )
                    self.platform_list.add(platform)

    def grid_to_pixel(self, x, y):
        return ((x + 2) * self.block_width, (y + 1) * self.block_height)


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
