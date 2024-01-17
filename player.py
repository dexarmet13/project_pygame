import pygame
from const import *

# import pyganim


class Player(pygame.sprite.Sprite):
    RIGHT_IMAGE_PATH = "materials/characters/128_lis.png"

    def __init__(self):
        super().__init__()

        self.right_image = pygame.image.load(Player.RIGHT_IMAGE_PATH)
        self.rect = self.right_image.get_rect()
        self.left_image = pygame.transform.flip(self.right_image, True, False)

        self.image = self.right_image

        self.change_x = 0
        self.change_y = 0

        self.level = None

        self.facing_right = True

        self.display_size = pygame.display.get_surface().get_size()

    def update(self):
        self._calc_grav()

        self.rect.x += self.change_x
        self._handle_horizontal_collisions()

        self.rect.y += self.change_y
        self._handle_vertical_collisions()

    def _initialize_animations(self):
        pass

    def _calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += GRAVITY

        if self.rect.bottom >= self.display_size[1] and self.change_y >= 0:
            self.change_y = 0
            self.rect.bottom = self.display_size[1]

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
        if self._prepare_for_jump():
            self.change_y = -JUMP_STRENGTH

    def _prepare_for_jump(self):
        if not self.level or not hasattr(self.level, "platform_list"):
            return False

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(
            self, self.level.platform_list, False
        )
        self.rect.y -= 2

        return bool(
            platform_hit_list or self.rect.bottom >= self.display_size[1]
        )

    def go_left(self):
        self.change_x = -MOVE_SPEED
        if self.facing_right:
            self.image = self.left_image
            self.facing_right = False

    def go_right(self):
        self.change_x = MOVE_SPEED
        if not self.facing_right:
            self.image = self.right_image
            self.facing_right = True

    def stop(self):
        self.change_x = 0
