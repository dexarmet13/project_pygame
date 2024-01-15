import pygame


class PlatformTexture:
    _cache = {}

    @classmethod
    def get_texture(cls, image_file, screen_size):
        if image_file not in cls._cache:
            image = pygame.image.load(image_file).convert_alpha()
            image = pygame.transform.scale(
                image,
                (int(screen_size[0] * 0.2), int(screen_size[1] * 0.2)),
            )
            cls._cache[image_file] = image
        return cls._cache[image_file]


class MapEditorUI:
    def __init__(self, screen_size, font, bg_image, images):
        self.font = font
        self._screen_size = screen_size
        self.editor_surf = pygame.Surface(self._screen_size)
        self.bg = bg_image
        self.images = images

    def draw(self, screen, highlight_fixed_area=False, fixed_area_rect=None):
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

        for y in range(0, 101, 5):
            for x in range(0, 101, 5):
                pygame.draw.line(
                    self.editor_surf,
                    (0, 0, 0),
                    (
                        x * self._screen_size[0] * 0.85 / 100,
                        y * self._screen_size[1] * 0.75 / 100,
                    ),
                    (
                        self._screen_size[0] * 0.85,
                        y * self._screen_size[1] * 0.75 / 100,
                    ),
                )

                pygame.draw.line(
                    self.editor_surf,
                    (0, 0, 0),
                    (x * self._screen_size[0] * 0.85 / 100, 0),
                    (
                        x * self._screen_size[0] * 0.85 / 100,
                        self._screen_size[1] * 0.75,
                    ),
                )

        if highlight_fixed_area and fixed_area_rect is not None:
            pygame.draw.rect(
                self.editor_surf, (0, 255, 0), fixed_area_rect, 2
            )  # added a thickness of 2 for the border

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

        self.load_images()

        self.map_editor_ui = MapEditorUI(
            self._screen_size, self._font, self.bg, self.images
        )

    def load_images(self):
        texture_file = "src/ground_texture.png"
        texture_size = (self._screen_size[0] * 0.4, self._screen_size[1] * 0.2)
        self.images = [
            PlatformTexture.get_texture(texture_file, texture_size)
            for _ in range(8)
        ]

    def toggle_soundtrack(self, flag_soundtrack):
        if flag_soundtrack:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def main(self):
        pygame.display.set_caption("Редактор карт")

        level_list = []

        pygame.mixer.music.load("sounds/ost_soundtrack.mp3")
        pygame.mixer.music.play(-1, 0.0, 1)

        running = True
        flag_soundtrack = False

        fixed_area = pygame.Rect(
            0,
            0,
            self._screen_size[0] * 0.85,
            self._screen_size[1] * 0.75,
        )

        self.map_editor_ui.draw(self.screen)

        while running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self.toggle_soundtrack(flag_soundtrack)
                        flag_soundtrack = not flag_soundtrack

                    if event.key == pygame.K_ESCAPE:
                        running = False

            cursor_pos = pygame.mouse.get_pos()
            highlight_area = fixed_area.collidepoint(cursor_pos)

            self.map_editor_ui.draw(self.screen, highlight_area, fixed_area)

            pygame.display.flip()

        pygame.quit()
