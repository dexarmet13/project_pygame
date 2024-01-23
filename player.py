import pygame
import time
from const import *
from territory import Trap
import pyganim


class Player(pygame.sprite.Sprite):
    RIGHT_IMAGE_PATH = "materials/characters/fox/128_lis.png"
    LEFT_IMAGE_PATH = "materials/characters/fox/128_lis_reverse.png"

    def __init__(self, screen):
        super().__init__()

        self.screen = screen

        self.right_image = pygame.image.load(
            Player.RIGHT_IMAGE_PATH
        ).convert_alpha()
        self.left_image = pygame.transform.flip(
            self.right_image, True, False
        ).convert_alpha()
        self.rect = self.right_image.get_rect()

        self.image = self.right_image

        self.left_anim = pyganim.PygAnimation([
            (f"materials/characters/fox/animations/left walk/left{i}.png", 0.1)
            for i in range(1, 14)
        ])
        self.right_anim = pyganim.PygAnimation([
            (
                f"materials/characters/fox/animations/right walk/right{i}.png",
                0.1,
            )
            for i in range(1, 14)
        ])
        self.left_jump_anim = pyganim.PygAnimation([
            (f"materials/characters/fox/animations/left jump/{i}{i}.png", 0.1)
            for i in range(1, 9)
        ])

        self.right_jump_anim = pyganim.PygAnimation([
            (f"materials/characters/fox/animations/right jump/{i}.png", 0.1)
            for i in range(1, 9)
        ])

        self.stayed_right_anim = pyganim.PygAnimation([
            (f"materials/characters/fox/animations/right idle/{i}.png", 0.1)
            for i in range(1, 7)
        ])

        self.stayed_left_anim = pyganim.PygAnimation([
            (f"materials/characters/fox/animations/left idle/{i}.png", 0.1)
            for i in range(1, 7)
        ])

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

        self.image.fill((0, 0, 0, 0))

        if self.change_y < 0:
            if self.facing_right:
                self.right_jump_anim.play()
                self.right_jump_anim.blit(self.image, (0, 0))
            else:
                self.left_jump_anim.play()
                self.left_jump_anim.blit(self.image, (0, 0))

        elif self.change_x != 0:
            if self.facing_right:
                self.right_anim.play()
                self.right_anim.blit(self.image, (0, 0))
            else:
                self.left_anim.play()
                self.left_anim.blit(self.image, (0, 0))
        else:
            if self.facing_right:
                self.stayed_right_anim.play()
                self.stayed_right_anim.blit(self.image, (0, 0))
            else:
                self.stayed_left_anim.play()
                self.stayed_left_anim.blit(self.image, (0, 0))

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
            if isinstance(block, Trap):
                self.teleport_player()
            elif self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

    def _handle_vertical_collisions(self):
        block_hit_list = pygame.sprite.spritecollide(
            self, self.level.platform_list, False
        )

        for block in block_hit_list:
            if isinstance(block, Trap):
                self.teleport_player()
            elif self.change_y > 0:
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
            self.facing_right = False

    def go_right(self):
        self.change_x = MOVE_SPEED
        if not self.facing_right:
            self.facing_right = True

    def stop(self):
        self.change_x = 0
        self.image = self.right_image

    def fade_out(self, duration):
        fade_surface = pygame.Surface(self.screen.get_size())
        fade_surface.fill((0, 0, 0))
        for alpha in range(0, 255, 10):
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(duration)

    def fade_in(self, duration):
        fade_surface = pygame.Surface(self.screen.get_size())
        fade_surface.fill((0, 0, 0))
        for alpha in range(255, -1, -10):
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(duration)

    def teleport_player(self):
        self.fade_out(25)

        self.rect.x = 0

        time.sleep(0.5)
        self.fade_in(25)
