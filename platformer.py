import pygame
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.95
JUMP_STRENGTH = -16
MOVE_SPEED = 9

bg = pygame.image.load("src/main_window_background.png")


# Класс игрока
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


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()


class Level(object):
    def __init__(self, player):
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
        screen.blit(bg, (0, 0))

        for platform in self.platform_list:
            screen.blit(
                platform.image,
                (
                    platform.rect.x,
                    platform.rect.y,
                ),
            )


class Level_01(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        level = [
            [210, 32, 500, 500],
            [210, 32, 200, 400],
            [210, 32, 600, 300],
        ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


def main():
    pygame.init()
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Платформер")
    player = Player()
    level_list = []
    level_list.append(Level_01(player))
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    running = False

    clock = pygame.time.Clock()

    while not running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

            # В главном игровом цикле

        CAMERA_LEFT_MARGIN = SCREEN_WIDTH * 0.48
        CAMERA_RIGHT_MARGIN = SCREEN_WIDTH * 0.52

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
    sys.exit(main())
