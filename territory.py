import pygame
import enemy


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
    def __init__(self, player):
        super().__init__(player, "materials/backgrounds/world_background.png")

        platform_image = pygame.image.load(
            "materials/textures/0g.png"
        ).convert_alpha()

        level = [
            [50, 50, 350, 400],
            [50, 50, 300, 400],
        ]

        for platform in level:
            block = Platform(*platform, platform_image)
            self.platform_list.add(block)


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
