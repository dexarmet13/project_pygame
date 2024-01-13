import pygame
from const import *
import pyganim


class Player(pygame.sprite.Sprite):
    def __init__(self, image_path="src/hero_texture.png"):
        super().__init__()

        self.display_size = pygame.display.get_surface().get_size()

        self.image_right = pygame.Surface((128, 128))
        self.image = self.image_right
        self.image.fill(pygame.Color(COLOR))
        self.rect = self.image.get_rect()

        # self.image.set_colorkey(pygame.Color(COLOR))  #
        self.image_left = pygame.transform.flip(self.image_right, True, False)

        self.change_x = 0
        self.change_y = 0
        self.boost_timer = 0
        self.boost_cooldown = 10000  # время ожидания перед следующим рывком в миллисекундах
        self.is_boosting = False
        self.max_speed = 20
        self.speed = 9
        self.last_boost_time = 0

        self.level = None

        self.facing_right = True

        # animation_delay= []
        # for anim in ANIMATION_RIGHT:
        #     animation_delay.append((anim, ANIMATION_FPS))
        # self.animation_right = pyganim.PygAnimation(animation_delay)
        # self.animation_right.play()
        # animation_delay = []
        # for anim in ANIMATION_LEFT:
        #     animation_delay.append((anim, ANIMATION_FPS))
        # self.animation_left = pyganim.PygAnimation(animation_delay)
        # self.animation_left.play()
        # # self.delayAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        # # self.delayAnimStay.play()
        # # self.delayAnimStay.blit(self.image, (0, 0))
        # # self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        # # self.boltAnimJumpLeft.play()
        # # self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        # # self.boltAnimJumpRight.play()
        # # self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        # # self.boltAnimJump.play()

    def update(self, right=False, left=False, jump=False, stop=False, shift=False, dt=60):
        if jump:
            self.rect.y += 2
            platform_hit_list = pygame.sprite.spritecollide(
                self, self.level.platform_list, False
            )
            self.rect.y -= 2

            if platform_hit_list or self.rect.bottom >= self.display_size[1]:
                self.change_y = JUMP_STRENGTH
                # self.move_change_image(False, False, True)

        if left:
            self.image.fill(pygame.Color(COLOR))
            if shift:
                self.boost_timer += dt
                if self.boost_timer < 2000:
                    self.speed = min(self.speed + 0.01 * dt, self.max_speed)
                else:
                    shift = False
                    self.speed = 5
                    self.boost_timer = 0
                self.change_x = -self.speed
            else:
                self.change_x = -MOVE_SPEED
                # if jump:
                #     # self.boltAnimJumpLeft.blit(self.image, (0, 0))
                #     pass
                # else:
                #     self.animation_left.blit(self.image, (0, 0))


        if right:
            self.image.fill(pygame.Color(COLOR))
            if shift:
                self.boost_timer += dt
                if self.boost_timer < 2000:
                    self.speed = min(self.speed + 0.01 * dt, self.max_speed)
                else:
                    shift = False
                    self.speed = 5
                    self.boost_timer = 0
                self.change_x = self.speed
            else:
                self.change_x = MOVE_SPEED
                # if jump:
                #     pass
                #     # self.boltAnimJumpRight.blit(self.image, (0, 0))
                # else:
                #     self.animation_right.blit(self.image, (0, 0))

            # if not self.facing_right:
            #     self.image = self.image_right
            #     self.facing_right = True
            # self.move_change_image(True)

        if not (left or right):
            self.change_x = 0
            # if not jump:
            #     self.image.fill(pygame.Color(COLOR))
            #     # self.delayAnimStay.blit(self.image, (0, 0))

            # self.move_change_image()
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

    # def jump(self):
    #     self.rect.y += 2
    #     platform_hit_list = pygame.sprite.spritecollide(
    #         self, self.level.platform_list, False
    #     )
    #     self.rect.y -= 2
    #
    #     if platform_hit_list or self.rect.bottom >= self.display_size[1]:
    #         self.change_y = JUMP_STRENGTH
    #         # self.move_change_image(False, False, True)
    #
    # def go_left(self):
    #     self.change_x = -MOVE_SPEED
    #     if self.facing_right:
    #         self.image = self.image_left
    #         self.facing_right = False
    #         self.move_change_image(False, True)
    #
    # def go_right(self):
    #     self.change_x = MOVE_SPEED
    #     if not self.facing_right:
    #         self.image = self.image_right
    #         self.facing_right = True
    #         self.move_change_image(True)
    #
    # def stop(self):
    #     self.change_x = 0
    #     # self.move_change_image()
