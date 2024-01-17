import pygame


class PlatformTexture:
    _cache = {}

    @classmethod
    def get_texture(cls, image_file, fixed_size):
        if image_file not in cls._cache:
            image = pygame.image.load(image_file).convert_alpha()
            image = pygame.transform.scale(image, fixed_size)
            cls._cache[image_file] = image
        return cls._cache[image_file]


class MapEditorUI:
    def __init__(self, screen_size, font, bg_image, images, cell_size):
        self.font = font
        self._screen_size = screen_size
        self.editor_surf = pygame.Surface(self._screen_size)
        self.bg = bg_image
        self.images = [img for img in images]
        self.padding = self._screen_size[0] * 0.02
        self.cell_width = cell_size[0]
        self.cell_height = cell_size[1]
        self.slide_rects = [
            pygame.Rect(
                self._screen_size[0] * 0.08,
                self._screen_size[1] * 0.79,
                self._screen_size[0] * 0.15,
                self._screen_size[1] * 0.15,
            ),
            pygame.Rect(
                self._screen_size[0] * 0.31,
                self._screen_size[1] * 0.79,
                self._screen_size[0] * 0.15,
                self._screen_size[1] * 0.15,
            ),
            pygame.Rect(
                self._screen_size[0] * 0.54,
                self._screen_size[1] * 0.79,
                self._screen_size[0] * 0.15,
                self._screen_size[1] * 0.15,
            ),
            pygame.Rect(
                self._screen_size[0] * 0.77,
                self._screen_size[1] * 0.79,
                self._screen_size[0] * 0.15,
                self._screen_size[1] * 0.15,
            ),
        ]

        self.texture_rects = self._generate_texture_rects()
        self.GRID_LINE_COLOR = (0, 0, 0)
        self.TEXT_COLOR = (0, 0, 0)
        self.BG_COLOR = (255, 255, 255)

    def _generate_texture_rects(self):
        rects = []
        for i, image in enumerate(self.images):
            top = self._screen_size[1] * 0.08 * (i + 1) + self.padding * i
            width = int(self.cell_width * 1.25)
            height = int(self.cell_height * 1.25)
            right = self._screen_size[0] * 0.95
            left = right - width

            rect = pygame.Rect(left, top, width, height)
            rects.append(rect)
        return rects

    def draw(self, screen):
        self.editor_surf.fill(self.BG_COLOR)
        self.editor_surf.blit(self.bg, (0, 0))
        self._draw_grid_lines(5, 10)
        self._draw_text()
        self._draw_images()
        self._draw_rects((0, 255, 0))
        screen.blit(self.editor_surf, (0, 0))

    def _draw_text(self):
        text_surf = self.font.render("Объекты", True, self.TEXT_COLOR)
        text_rect = text_surf.get_rect(
            center=(
                self._screen_size[0] * 0.85
                + self._screen_size[0] * 0.25 / 3.5,
                self._screen_size[1] * 0.05,
            )
        )
        self.editor_surf.blit(text_surf, text_rect)

    def _draw_images(self):
        for img, rect in zip(self.images, self.texture_rects):
            self.editor_surf.blit(
                pygame.transform.scale(
                    img,
                    (
                        int(self.cell_width * 1.25),
                        int(self.cell_height * 1.25),
                    ),
                ),
                rect,
            )

    def _draw_grid_lines(self, interval_x, interval_y):
        for y in range(0, 101, interval_y):
            pygame.draw.line(
                self.editor_surf,
                self.GRID_LINE_COLOR,
                (0, y * self._screen_size[1] * 0.75 / 100),
                (
                    self._screen_size[0] * 0.85,
                    y * self._screen_size[1] * 0.75 / 100,
                ),
            )
        for x in range(0, 101, interval_x):
            pygame.draw.line(
                self.editor_surf,
                self.GRID_LINE_COLOR,
                (x * self._screen_size[0] * 0.85 / 100, 0),
                (
                    x * self._screen_size[0] * 0.85 / 100,
                    self._screen_size[1] * 0.75,
                ),
            )

    def _draw_rects(self, color):
        for rect in self.slide_rects:
            pygame.draw.rect(self.editor_surf, color, rect)

    def check_texture_selection(self, mouse_pos):
        for i, rect in enumerate(self.texture_rects):
            if rect.collidepoint(mouse_pos):
                return i
        return None

    def check_slide_selection(self, mouse_pos):
        for i, rect in enumerate(self.slide_rects):
            if rect.collidepoint(mouse_pos):
                return i
        return None


class MapEditorWindow:
    def __init__(self, screen_size):
        pygame.init()

        self._screen_size = screen_size
        self.screen = pygame.display.set_mode(self._screen_size)

        self.levels = []

        self.cell_width = int(self._screen_size[0] * 0.85 / 100 * 5 + 1)
        self.cell_height = int(self._screen_size[1] * 0.75 / 100 * 10)

        self.selected_cells = {}

        self._font = pygame.font.Font(None, 46)

        self.bg = pygame.transform.scale(
            pygame.image.load(
                "materials/backgrounds/map_editor_background.png"
            ).convert_alpha(),
            (
                self._screen_size[0] * 0.85,
                self._screen_size[1] * 0.75,
            ),
        )

        self.selected_texture = None
        self.selected_texture_rect = None

        self.load_images()

        self.map_editor_ui = MapEditorUI(
            self._screen_size,
            self._font,
            self.bg,
            self.images,
            (self.cell_width, self.cell_height),
        )

    def load_images(self):
        texture_paths = [
            "materials/textures/green_ground_texture.png",
            "materials/textures/green_rock_texture.png",
            "materials/textures/dirt_ground_texture.png",
            "materials/textures/rock_ground_texture.png",
            "materials/textures/lava_ground_texture.png",
            "materials/textures/snow_ground_texture.png",
        ]
        texture_size = (self.cell_width, self.cell_height)
        self.images = [
            PlatformTexture.get_texture(texture_file, texture_size)
            for texture_file in texture_paths
        ]

    def toggle_soundtrack(self, flag_soundtrack):
        if flag_soundtrack:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def main(self):
        pygame.display.set_caption("Редактор карт")

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
        is_deleting = False
        selected_texture_index = None
        selected_slide = None

        while running:
            events = pygame.event.get()

            self.map_editor_ui.draw(self.screen)
            self.redraw_selected_cells()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    selection_start = pygame.mouse.get_pos()

                    if event.button == 1:
                        if not is_deleting:
                            if (
                                fixed_area.collidepoint(selection_start)
                                and selected_texture_index is not None
                            ):
                                is_selecting = True
                            else:
                                is_selecting = False

                    elif event.button == 3:
                        if fixed_area.collidepoint(selection_start):
                            is_deleting = True
                            start_delete_selection = selection_start
                        else:
                            is_deleting = False

                if event.type == pygame.MOUSEBUTTONUP:
                    current_mouse_pos = pygame.mouse.get_pos()

                    if event.button == 1:
                        if (
                            is_selecting
                            and fixed_area.collidepoint(selection_start)
                            and fixed_area.collidepoint(current_mouse_pos)
                        ):
                            self.select_cells(
                                selection_start, current_mouse_pos
                            )
                        is_selecting = False

                        if not fixed_area.collidepoint(current_mouse_pos):
                            selected_texture_index = (
                                self.map_editor_ui.check_texture_selection(
                                    current_mouse_pos
                                )
                            )

                        if selected_texture_index is not None:
                            self.selected_texture = self.images[
                                selected_texture_index
                            ]
                            self.selected_texture_rect = (
                                self.map_editor_ui.texture_rects[
                                    selected_texture_index
                                ]
                            )

                        else:
                            selected_slide = (
                                self.map_editor_ui.check_slide_selection(
                                    current_mouse_pos
                                )
                            )
                            if selected_slide is not None:
                                color = (255, 0, 0)
                                rect = pygame.Rect(0, 0, 50, 50)
                                pygame.draw.rect(self.screen, color, rect)
                            else:
                                self.selected_texture = None
                                self.selected_texture_rect = None

                    elif event.button == 3:
                        if (
                            is_deleting
                            and fixed_area.collidepoint(start_delete_selection)
                            and fixed_area.collidepoint(current_mouse_pos)
                        ):
                            self.select_cells(
                                start_delete_selection, current_mouse_pos, True
                            )
                        is_deleting = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self.toggle_soundtrack(flag_soundtrack)
                        flag_soundtrack = not flag_soundtrack

                    elif event.key == pygame.K_ESCAPE:
                        running = False

            if fixed_area.collidepoint(pygame.mouse.get_pos()):
                current_mouse_pos = pygame.mouse.get_pos()
                if is_selecting:
                    self.highlight_selection_area(
                        selection_start, current_mouse_pos
                    )
                elif is_deleting:
                    self.highlight_selection_area(
                        start_delete_selection, current_mouse_pos
                    )

            if self.selected_texture_rect is not None:
                border_color = (255, 0, 0)
                self.draw_border(
                    self.screen, self.selected_texture_rect, border_color
                )

            pygame.display.flip()

        pygame.quit()

    def grid_position(self, screen_position):
        grid_x = screen_position[0] // self.cell_width
        grid_y = screen_position[1] // self.cell_height
        return grid_x, grid_y

    def highlight_selection_area(self, start_pos, current_pos):
        rect = pygame.Rect(
            min(start_pos[0], current_pos[0]),
            min(start_pos[1], current_pos[1]),
            abs(start_pos[0] - current_pos[0]),
            abs(start_pos[1] - current_pos[1]),
        )

        pygame.draw.rect(self.screen, (0, 255, 0), rect, 1)

    def select_cells(self, start_pos, end_pos, delete=False):
        start_grid_pos = self.grid_position(start_pos)
        end_grid_pos = self.grid_position(end_pos)

        for x in range(
            min(start_grid_pos[0], end_grid_pos[0]),
            max(start_grid_pos[0], end_grid_pos[0]) + 1,
        ):
            for y in range(
                min(start_grid_pos[1], end_grid_pos[1]),
                max(start_grid_pos[1], end_grid_pos[1]) + 1,
            ):
                cell = (x, y)
                if delete:
                    if cell in self.selected_cells:
                        del self.selected_cells[cell]
                else:
                    self.selected_cells[cell] = self.selected_texture
                    self.draw_texture(cell, self.selected_texture)

    def draw_texture(self, cell, texture):
        x, y = cell
        cell_rect = pygame.Rect(
            x * self.cell_width - 1,
            y * self.cell_height,
            self.cell_width,
            self.cell_height,
        )
        self.screen.blit(texture, cell_rect.topleft)

    def draw_border(self, screen, rect, color, border_width=3):
        pygame.draw.rect(screen, color, rect, border_width)

    def redraw_selected_cells(self):
        cells_to_delete = []

        for cell, texture in self.selected_cells.items():
            if texture is not None:
                self.draw_texture(cell, texture)
            else:
                cells_to_delete.append(cell)

        for cell in cells_to_delete:
            del self.selected_cells[cell]
