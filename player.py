import pygame
from const import MOVE_SPEED, JUMP_STRENGTH, GRAVITY


class Player(pygame.sprite.Sprite):
    def __init__(self, image_path="src/hero_texture.png"):
        super().__init__()
        self.display_size = pygame.display.get_surface().get_size()

        self.image_right = pygame.image.load(image_path)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.image_left = pygame.transform.flip(self.image_right, True, False)

        self.change_x = 0
        self.change_y = 0

        self.level = None

        self.facing_right = True

        # delayAnim= []
        # for anim in ANIMATION_RIGHT:
        #     delayAnim.append((anim, ANIMATION_FPS))
        # self.delayAnimRight = pyganim.PygAnimation(delayAnim)
        # self.delayAnimRight.play()
        # delayAnim = []
        # for anim in ANIMATION_LEFT:
        #     delayAnim.append((anim, ANIMATION_FPS))
        # self.delayAnimLeft = pyganim.PygAnimation(delayAnim)
        # self.delayAnimLeft.play()
        #
        # self.delayAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        # self.delayAnimStay.play()
        # self.delayAnimStay.blit(self.image, (0, 0))
        #
        # self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        # self.boltAnimJumpLeft.play()
        #
        # self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        # self.boltAnimJumpRight.play()
        #
        # self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        # self.boltAnimJump.play()

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
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(
            self, self.level.platform_list, False
        )
        self.rect.y -= 2

        if platform_hit_list or self.rect.bottom >= self.display_size[1]:
            self.change_y = JUMP_STRENGTH
            # self.move_change_image(False, False, True)

    def go_left(self):
        self.change_x = -MOVE_SPEED
        if self.facing_right:
            self.image = self.image_left
            self.facing_right = False
            self.move_change_image(False, True)

    def go_right(self):
        self.change_x = MOVE_SPEED
        if not self.facing_right:
            self.image = self.image_right
            self.facing_right = True
            self.move_change_image(True)

    def stop(self):
        self.change_x = 0
        # self.move_change_image()

    def move_change_image(self, right=False, left=False, up=False, stop=False):
        pass
        # if up:
        #     self.image.fill(pygame.Color(COLOR))
        #     self.boltAnimJump.blit(self.image, (0, 0))
        #
        # if left:
        #     self.image.fill(pygame.Color(COLOR))
        #     if up:
        #         self.boltAnimJumpLeft.blit(self.image, (0, 0))
        #     else:
        #         self.delayAnimLeft.blit(self.image, (0, 0))
        #
        # if right:
        #     self.image.fill(pygame.Color(COLOR))
        #     if up:
        #         self.boltAnimJumpRight.blit(self.image, (0, 0))
        #     else:
        #         self.delayAnimRight.blit(self.image, (0, 0))
        #
        # if not (left or right):
        #     if not up:
        #         self.image.fill(pygame.Color(COLOR))
        #         self.boltAnimStay.blit(self.image, (0, 0))
