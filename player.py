import pygame
from const import *


class Player(pygame.sprite.Sprite):
    def __init__(self, image_path="src/hero_texture.png"):
        super().__init__()

        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.level = None
        self.facing_right = True

    def update(self):
        self._calc_grav()

        self.rect.x += self.change_x
        self._handle_horizontal_collisions()

        self.rect.y += self.change_y
        self._handle_vertical_collisions()

    def _calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += GRAVITY

        if self.rect.bottom >= SCREEN_HEIGHT and self.change_y >= 0:
            self.change_y = 0
            self.rect.bottom = SCREEN_HEIGHT

    def _handle_horizontal_collisions(self):
        block_hit_list = pygame.sprite.spritecollide(
            self, self.level.platform_list, False
        )
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

    def _handle_vertical_collisions(self):
        block_hit_list = pygame.sprite.spritecollide(
            self, self.level.platform_list, False
        )
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0

    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(
            self, self.level.platform_list, False
        )
        self.rect.y -= 2

        if platform_hit_list or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = JUMP_STRENGTH

    def go_left(self):
        self.change_x = -MOVE_SPEED
        if self.facing_right:
            self.flip()
            self.facing_right = False

    def go_right(self):
        self.change_x = MOVE_SPEED
        if not self.facing_right:
            self.flip()
            self.facing_right = True

    def stop(self):
        self.change_x = 0

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)
