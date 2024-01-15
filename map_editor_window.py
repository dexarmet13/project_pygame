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

        self.editor_surf.blit(text_surf, text_rect)
        screen.blit(self.editor_surf, (0, 0))


class MapEditorWindow:
    def __init__(self, screen_size):
        pygame.init()

        self._screen_size = screen_size
        self.screen = pygame.display.set_mode(self._screen_size)

        self.cell_width = self._screen_size[0] * 0.85 / 100 * 5
        self.cell_height = self._screen_size[1] * 0.75 / 100 * 5

        self.selected_cells = []

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

        is_selecting = False
        selection_start = None

        while running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        is_selecting = True
                        selection_start = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        is_selecting = False
                        current_mouse_pos = pygame.mouse.get_pos()

                        if fixed_area.collidepoint(
                            current_mouse_pos
                        ) and fixed_area.collidepoint(selection_start):
                            self.select_cells(
                                selection_start, current_mouse_pos
                            )

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self.toggle_soundtrack(flag_soundtrack)
                        flag_soundtrack = not flag_soundtrack

                    elif event.key == pygame.K_ESCAPE:
                        running = False

            self.map_editor_ui.draw(self.screen)

            self.redraw_selected_cells()

            if is_selecting:
                current_mouse_pos = pygame.mouse.get_pos()
                if fixed_area.collidepoint(
                    current_mouse_pos
                ) and fixed_area.collidepoint(selection_start):
                    self.highlight_selection_area(
                        selection_start, current_mouse_pos
                    )

            pygame.display.flip()

        pygame.quit()

    def grid_position(self, screen_position):
        grid_x = int(screen_position[0] // self.cell_width)
        grid_y = int(screen_position[1] // self.cell_height)
        return grid_x, grid_y

    def highlight_selection_area(self, start_pos, current_pos):
        rect = pygame.Rect(
            min(start_pos[0], current_pos[0]),
            min(start_pos[1], current_pos[1]),
            abs(start_pos[0] - current_pos[0]),
            abs(start_pos[1] - current_pos[1]),
        )

        pygame.draw.rect(self.screen, (0, 255, 0), rect, 1)

    def select_cells(self, start_pos, end_pos):
        start_grid_pos = self.grid_position(start_pos)
        end_grid_pos = self.grid_position(end_pos)

        new_selected_cells = []
        for x in range(
            min(start_grid_pos[0], end_grid_pos[0]),
            max(start_grid_pos[0], end_grid_pos[0]) + 1,
        ):
            for y in range(
                min(start_grid_pos[1], end_grid_pos[1]),
                max(start_grid_pos[1], end_grid_pos[1]) + 1,
            ):
                new_selected_cells.append((x, y))

        self.selected_cells.extend(new_selected_cells)

        for cell in self.selected_cells:
            self.draw_cell(cell, color=(0, 255, 0))

    def draw_cell(self, cell, color):
        x, y = cell
        cell_rect = pygame.Rect(
            x * self.cell_width + 1,
            y * self.cell_height,
            self.cell_width,
            self.cell_height,
        )
        pygame.draw.rect(self.screen, color, cell_rect)

    def redraw_selected_cells(self):
        for cell in self.selected_cells:
            self.draw_cell(cell, color=(0, 255, 0))
