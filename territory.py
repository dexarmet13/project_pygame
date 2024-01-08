import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()


class Level(object):
    def __init__(self, player):
        self.bg = pygame.image.load("src/main_window_background.png")
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
            [210, 32, 500, 475],
            [210, 32, 175, 400],
            [210, 32, 575, 300],
        ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
