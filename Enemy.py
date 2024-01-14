import pygame
import random
from const import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((ENEMY_WITDH, ENEMY_WITDH))
        # self.image.fill(Color(COLOR))
        self.rect = pygame.Rect(x, y, ENEMY_WITDH, ENEMY_HEIGHT)
        # self.image.set_colorkey(Color(COLOR))
        self.startX = x
        self.startY = y
        self.maxLengthLeft = 3
        self.maxLengthUp = 3
        self.change_x = 3
        self.change_y = 3
        self.level = None

    def update(self, platforms):  # по принципу героя

        self.image.fill(pygame.Color(COLOR))

        self.rect.x += self.change_x
        self._handle_horizontal_collisions()

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.change_x = -self.change_x

    def _handle_horizontal_collisions(self):
        block_hit_list = pygame.sprite.spritecollide(
            self, self.level.platform_list, False
        )
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

