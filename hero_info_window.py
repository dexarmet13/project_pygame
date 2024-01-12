import pygame


class HeroInfoWindow:
    def __init__(self, color, screen_size, font):
        self.is_visible = False
        self.font = font
        self.color = color
        self.menu_bg = pygame.Surface(screen_size)

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_visible = False

    def draw(self, screen):
        if self.is_visible:
            health_text = self.font.render(
                "Health: 100%", True, (255, 255, 255)
            )

            self.menu_bg.fill(self.color)
            self.menu_bg.blit(health_text, (10, 10))

            menu_rect = self.menu_bg.get_rect(center=screen.get_rect().center)

            screen.blit(self.menu_bg, menu_rect.topleft)
