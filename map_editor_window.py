import pygame


class PlatformTexture:
    def __init__(self, image_file, screen_size):
        self._screen_size = screen_size

        image = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(
            image,
            (int(self._screen_size[0] * 0.2), int(self._screen_size[1] * 0.2)),
        )


class MapEditorUI:
    def __init__(self, screen_size, font, bg_image, images):
        self.font = font
        self._screen_size = screen_size
        self.editor_surf = pygame.Surface(self._screen_size)
        self.bg = bg_image
        self.images = images

    def draw(self, screen):
        self.editor_surf.fill((255, 255, 255))
        self.editor_surf.blit(self.bg, (0, 0))

        text_surf = self.font.render("Объекты", True, (0, 0, 0))
        text_rect = text_surf.get_rect(
            center=(
                self._screen_size[0] * 0.85
                + self._screen_size[0] * 0.25 / 3.5,
                self._screen_size[1] * 0.05,
            )
        )

        for i in range(0, len(self.images)):
            self.editor_surf.blit(
                self.images[i],
                (
                    self._screen_size[0] * 0.88,
                    self._screen_size[1] * 0.08 * (i + 1),
                ),
            )

        self.editor_surf.blit(text_surf, text_rect)
        screen.blit(self.editor_surf, (0, 0))


class MapEditorWindow:
    def __init__(self, screen_size):
        pygame.init()

        self._screen_size = screen_size
        self.screen = pygame.display.set_mode(self._screen_size)

        self._font = pygame.font.Font(None, 36)

        self.bg = pygame.transform.scale(
            pygame.image.load(
                "src/main_window_background.png"
            ).convert_alpha(),
            (
                self._screen_size[0] * 0.85,
                self._screen_size[1] * 0.75,
            ),
        )

        self.images = [
            PlatformTexture(
                "src/ground_texture.png",
                (self._screen_size[0] * 0.4, self._screen_size[1] * 0.2),
            ).image,
            PlatformTexture(
                "src/ground_texture.png",
                (self._screen_size[0] * 0.4, self._screen_size[1] * 0.2),
            ).image,
            PlatformTexture(
                "src/ground_texture.png",
                (self._screen_size[0] * 0.4, self._screen_size[1] * 0.2),
            ).image,
            PlatformTexture(
                "src/ground_texture.png",
                (self._screen_size[0] * 0.4, self._screen_size[1] * 0.2),
            ).image,
            PlatformTexture(
                "src/ground_texture.png",
                (self._screen_size[0] * 0.4, self._screen_size[1] * 0.2),
            ).image,
            PlatformTexture(
                "src/ground_texture.png",
                (self._screen_size[0] * 0.4, self._screen_size[1] * 0.2),
            ).image,
            PlatformTexture(
                "src/ground_texture.png",
                (self._screen_size[0] * 0.4, self._screen_size[1] * 0.2),
            ).image,
            PlatformTexture(
                "src/ground_texture.png",
                (self._screen_size[0] * 0.4, self._screen_size[1] * 0.2),
            ).image,
        ]

        self.map_editor_ui = MapEditorUI(
            self._screen_size, self._font, self.bg, self.images
        )

    def main(self):
        pygame.display.set_caption("Редактор карт")

        level_list = []

        pygame.mixer.music.load("sounds/ost_soundtrack.mp3")
        pygame.mixer.music.play(-1, 0.0, 1)

        running = True
        flag_sountrack = False

        fixed_area = pygame.Rect(
            0,
            0,
            self._screen_size[0] * 0.85,
            self._screen_size[1] * 0.75,
        )

        while running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        flag_sountrack = not flag_sountrack
                        if flag_sountrack:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                    if event.key == pygame.K_ESCAPE:
                        running = False

            cursor_pos = pygame.mouse.get_pos()

            self.map_editor_ui.draw(self.screen)

            cursor_pos = pygame.mouse.get_pos()
            if fixed_area.collidepoint(cursor_pos):
                pygame.draw.rect(self.screen, (0, 255, 0), fixed_area)

            pygame.display.flip()

        pygame.quit()
