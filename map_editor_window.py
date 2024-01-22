import pygame
import numpy as np
import sys
from PyQt5.QtWidgets import QMessageBox


class ObjectTexture:
    _cache = {}

    @classmethod
    def get_texture(cls, image_file, fixed_size):
        if image_file not in cls._cache:
            image = pygame.image.load(image_file).convert_alpha()
            image = pygame.transform.scale(image, fixed_size)
            cls._cache[image_file] = image
        return cls._cache[image_file]


class MapEditorUI:
    def __init__(
        self,
        screen_size,
        font,
        bg_image,
        platform_images,
        objects_images,
        cell_size,
        slide_image,
    ):
        self._font = font

        self._screen_size = screen_size
        self.editor_surf = pygame.Surface(self._screen_size)

        self.bg = bg_image
        self.platform_images = [img for img in platform_images]
        self.objects_images = [img for img in objects_images]

        self.padding = self._screen_size[0] * 0.02
        self.interval_x = 5
        self.interval_y = 7.7

        self.cell_width = cell_size[0]
        self.cell_height = cell_size[1]

        self.slide_image = pygame.transform.scale(
            slide_image,
            (
                self._screen_size[0] * 0.15,
                self._screen_size[1] * 0.15,
            ),
        )
        self.slide_rects = []

        self.platform_texture_rects = self._generate_platform_texture_rects()
        self.object_texture_rects = self._generate_object_texture_rects()

        self.GRID_LINE_COLOR = (0, 0, 0)
        self.TEXT_COLOR = (0, 0, 0)
        self.BG_COLOR = (255, 255, 255)

    def _generate_platform_texture_rects(self):
        rects = []
        for i in range(len(self.platform_images)):
            top = self._screen_size[1] * 0.08 * (i + 1) + self.padding * i
            width = int(self.cell_width * 1.25)
            height = int(self.cell_height * 1.25)
            right = self._screen_size[0] * 0.945
            left = right - width

            rect = pygame.Rect(left, top, width, height)
            rects.append(rect)
        return rects

    def _generate_object_texture_rects(self):
        rects = []
        for i in range(len(self.objects_images)):
            top = self._screen_size[1] * 0.08 * (i + 1) + self.padding * i
            width = int(self.cell_width * 1.25)
            height = int(self.cell_height * 1.25)
            right = self._screen_size[0] * 0.095
            left = right - width

            rect = pygame.Rect(left, top, width, height)
            rects.append(rect)
        return rects

    def draw(self, screen):
        self.editor_surf.fill(self.BG_COLOR)
        self.editor_surf.blit(self.bg, (self._screen_size[0] * 0.15, 0))
        self._draw_grid_lines(self.interval_x, self.interval_y)
        self._draw_text()
        self._draw_platforms_images()
        self._draw_objects_images()
        self._draw_slide_images()
        screen.blit(self.editor_surf, (0, 0))

    def _draw_text(self):
        platform_text_surf = self._font.render(
            "Платформы", True, self.TEXT_COLOR
        )
        platform_text_rect = platform_text_surf.get_rect(
            center=(
                self._screen_size[0] * 0.85
                + self._screen_size[0] * 0.25 / 3.5,
                self._screen_size[1] * 0.04,
            )
        )

        objects_text_surf = self._font.render("Объекты", True, self.TEXT_COLOR)
        object_text_rect = objects_text_surf.get_rect(
            center=(
                self._screen_size[0] * 0.075,
                self._screen_size[1] * 0.04,
            )
        )

        self.editor_surf.blit(platform_text_surf, platform_text_rect)
        self.editor_surf.blit(objects_text_surf, object_text_rect)

    def _draw_grid_lines(self, interval_x, interval_y):
        for y in np.arange(0, interval_y * 14, interval_y):
            line_y = y * self._screen_size[1] * 0.75 / 100
            pygame.draw.line(
                self.editor_surf,
                self.GRID_LINE_COLOR,
                (self._screen_size[0] * 0.15, line_y),
                (self._screen_size[0] * 0.85, line_y),
                3,
            )

        for x in np.arange(0, interval_x * 21, interval_x):
            line_x = (
                self._screen_size[0] * 0.15
                + x * self._screen_size[0] * 0.70 / 100
            )
            pygame.draw.line(
                self.editor_surf,
                self.GRID_LINE_COLOR,
                (line_x, 0),
                (line_x, self._screen_size[1] * 0.75),
                3,
            )

    def _draw_platforms_images(self):
        for img, rect in zip(
            self.platform_images, self.platform_texture_rects
        ):
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

    def _draw_objects_images(self):
        for img, rect in zip(self.objects_images, self.object_texture_rects):
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

    def _draw_slide_images(self):
        image_positions = [
            (
                self._screen_size[0] * 0.08,
                self._screen_size[1] * 0.79,
            ),
            (
                self._screen_size[0] * 0.31,
                self._screen_size[1] * 0.79,
            ),
            (
                self._screen_size[0] * 0.54,
                self._screen_size[1] * 0.79,
            ),
            (
                self._screen_size[0] * 0.77,
                self._screen_size[1] * 0.79,
            ),
        ]
        for i, position in enumerate(image_positions):
            image_rect = self.slide_image.get_rect()
            image_rect.topleft = position

            self.slide_rects.append(image_rect)

            text = f"Слайд {i + 1}"
            text_color = pygame.Color("white")
            text_surface = self._font.render(text, True, text_color)

            text_rect = text_surface.get_rect(center=image_rect.center)

            self.editor_surf.blit(self.slide_image, image_rect)
            self.editor_surf.blit(text_surface, text_rect)

    def check_texture_selection(self, mouse_pos):
        for i, rect in enumerate(self.platform_texture_rects):
            if rect.collidepoint(mouse_pos):
                return i
        return None

    def check_object_selection(self, mouse_pos):
        for i, rect in enumerate(self.object_texture_rects):
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

        self.texture_places = [None, None, None, None]

        self.cell_width = self._screen_size[0] * 0.70 * 0.05
        self.cell_height = self._screen_size[1] * 0.75 * 0.077

        self.selected_cells = {}

        self._font = pygame.font.Font(None, 50)

        self.fixed_area = pygame.Rect(
            self._screen_size[0] * 0.15,
            0,
            self._screen_size[0] * 0.70,
            self._screen_size[1] * 0.75,
        )

        self.bg = pygame.transform.scale(
            pygame.image.load(
                "materials/backgrounds/map_editor_background.png"
            ).convert_alpha(),
            (
                self._screen_size[0] * 0.70,
                self._screen_size[1] * 0.75,
            ),
        )

        self.slide_image = pygame.image.load(
            "materials/button_bg/slide_button.png"
        ).convert_alpha()

        self.selected_texture = None
        self.selected_texture_rect = None

        self.current_selected_slide = 0

        self.load_platform_images()
        self.load_objects_images()

        self.map_editor_ui = MapEditorUI(
            self._screen_size,
            self._font,
            self.bg,
            self.platform_images,
            self.objects_images,
            (self.cell_width, self.cell_height),
            self.slide_image,
        )

    def load_platform_images(self):
        texture_paths = [
            "materials/textures/green_ground_texture.png",
            "materials/textures/colored_ground_texture.png",
            "materials/textures/dirt_ground_texture.png",
            "materials/textures/rock_ground_texture.png",
            "materials/textures/lava_ground_texture.png",
            "materials/textures/snow_ground_texture.png",
        ]
        texture_size = (self.cell_width, self.cell_height)
        self.platform_images = [
            ObjectTexture.get_texture(texture_file, texture_size)
            for texture_file in texture_paths
        ]

    def load_objects_images(self):
        texture_paths = [
            "materials/details/bush.png",
            "materials/details/firefly.png",
            "materials/details/flower.png",
            "materials/details/grass.png",
            "materials/details/pixel_grass.png",
        ]
        texture_size = (self.cell_width, self.cell_height)
        self.objects_images = [
            ObjectTexture.get_texture(texture_file, texture_size)
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

        is_selecting = False
        is_deleting = False
        selected_texture_index = None
        selected_object_index = None
        previous_selected_slide = 0

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
                            if self.fixed_area.collidepoint(
                                selection_start
                            ) and (
                                selected_texture_index is not None
                                or selected_object_index is not None
                            ):
                                is_selecting = True
                            else:
                                is_selecting = False

                    elif event.button == 3:
                        if self.fixed_area.collidepoint(selection_start):
                            is_deleting = True
                            start_delete_selection = selection_start
                        else:
                            is_deleting = False

                if event.type == pygame.MOUSEBUTTONUP:
                    current_mouse_pos = pygame.mouse.get_pos()

                    if event.button == 1:
                        if (
                            is_selecting
                            and self.fixed_area.collidepoint(selection_start)
                            and self.fixed_area.collidepoint(current_mouse_pos)
                        ):
                            self.select_cells(
                                selection_start, current_mouse_pos
                            )
                        is_selecting = False

                        if not self.fixed_area.collidepoint(current_mouse_pos):
                            selected_texture_index = (
                                self.map_editor_ui.check_texture_selection(
                                    current_mouse_pos
                                )
                            )

                            selected_object_index = (
                                self.map_editor_ui.check_object_selection(
                                    current_mouse_pos
                                )
                            )

                        if (
                            selected_texture_index is not None
                            and not selected_object_index
                        ):
                            self.selected_texture = self.platform_images[
                                selected_texture_index
                            ]
                            self.selected_texture_rect = (
                                self.map_editor_ui.platform_texture_rects[
                                    selected_texture_index
                                ]
                            )

                        elif (
                            selected_object_index is not None
                            and not selected_texture_index
                        ):
                            self.selected_texture = self.objects_images[
                                selected_object_index
                            ]
                            self.selected_texture_rect = (
                                self.map_editor_ui.object_texture_rects[
                                    selected_object_index
                                ]
                            )
                        else:
                            self.selected_texture = None
                            self.selected_texture_rect = None

                        new_selected_slide = (
                            self.map_editor_ui.check_slide_selection(
                                current_mouse_pos
                            )
                        )

                        if new_selected_slide is not None:
                            self.current_selected_slide = new_selected_slide

                        if (
                            self.current_selected_slide is not None
                            and self.current_selected_slide
                            != previous_selected_slide
                        ):
                            surf_of_cell = {}

                            for cell, surf in self.selected_cells.items():
                                surf_of_cell[cell] = surf

                            if previous_selected_slide is not None:
                                self.texture_places[
                                    previous_selected_slide
                                ] = surf_of_cell.copy()

                                self.clear_all_cells()
                                surf_of_cell.clear()

                                if (
                                    self.texture_places[
                                        self.current_selected_slide
                                    ]
                                    is not None
                                ):
                                    self.selected_cells = self.texture_places[
                                        self.current_selected_slide
                                    ].copy()

                            previous_selected_slide = (
                                self.current_selected_slide
                            )

                    elif event.button == 3:
                        if (
                            is_deleting
                            and self.fixed_area.collidepoint(
                                start_delete_selection
                            )
                            and self.fixed_area.collidepoint(current_mouse_pos)
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
                    break

            if self.fixed_area.collidepoint(pygame.mouse.get_pos()):
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

            if self.current_selected_slide is not None:
                border_color = (255, 0, 0)
                self.draw_border(
                    self.screen,
                    self.map_editor_ui.slide_rects[
                        self.current_selected_slide
                    ],
                    border_color,
                )

            pygame.display.flip()

        pygame.quit()

    def grid_position(self, screen_position):
        grid_x = int(
            (screen_position[0] - self._screen_size[0] * 0.15)
            / self.cell_width
        )
        grid_y = int(screen_position[1] / self.cell_height)

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
            x * self.cell_width + self._screen_size[0] * 0.15,
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

    def clear_all_cells(self):
        for cell in self.selected_cells:
            self.selected_cells[cell] = None

    def save_textures(self):
        image_path_of_cell = {}

        for i in range(len(self.texture_places)):
            if self.texture_places[i]:
                for cell, value in self.texture_places[i].items():
                    for (
                        path,
                        surf,
                    ) in ObjectTexture._cache.items():
                        if value == surf:
                            if path not in image_path_of_cell:
                                image_path_of_cell[path] = [cell]
                            else:
                                image_path_of_cell[path] += [cell]

                self.levels.append(image_path_of_cell.copy())
                image_path_of_cell.clear()

        return self.levels
