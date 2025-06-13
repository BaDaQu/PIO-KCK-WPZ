# src/board_screen.py
import pygame
import settings  # <-- NOWY IMPORT


class Board:
    def __init__(self, screen_width_gameplay, screen_height_gameplay):
        self.board_render_width = settings.BOARD_RENDER_WIDTH
        self.board_render_height = settings.BOARD_RENDER_HEIGHT

        self.board_offset_x_on_screen = screen_width_gameplay - self.board_render_width
        self.board_offset_y_on_screen = (screen_height_gameplay - self.board_render_height) // 2

        self.background_image = None
        self.fields_data = []
        self.field_label_font = None

        self._load_assets()
        self._define_field_labels_and_geometry()

    def _load_assets(self):
        try:
            self.background_image = pygame.image.load(settings.IMAGE_PATH_BOARD_BG).convert()
            print("Plansza załadowana.")
        except Exception as e:
            print(f"Błąd ładowania obrazka planszy: {e}")
            self.background_image = pygame.Surface((self.board_render_width, self.board_render_height))
            self.background_image.fill(settings.BOARD_BG_FALLBACK_COLOR)

        try:
            self.field_label_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR,
                                                     settings.BOARD_LABEL_FONT_SIZE)
        except Exception as e:
            print(f"Błąd ładowania czcionki dla etykiet pól: {e}")
            self.field_label_font = pygame.font.SysFont(None, settings.BOARD_LABEL_FONT_SIZE + 4)

    def _define_field_labels_and_geometry(self):
        field_labels_text_internal = [
            "START", "ANALIZA MAT. I", "ALGEBRA LINIOWA", "OPROGRAMOWANIE UŻYTKOWE", "STYPENDIUM",
            "PROGRAMOWANIE SKRYPTOWE", "BHP", "FIZYKA", "EGZAMIN", "MATEMATYKA DYSKRETNA",
            "PODSTAWY ELEKTROTECHNIKI", "PODSTAWY PROGRAMOWANIA I", "POPRAWKA", "PODSTAWY PROGRAMOWANIA II",
            "SYSTEMY OPERACYJNE I", "ANALIZA MAT. II", "EGZAMIN", "PODSTAWY GRAFIKI KOMP.",
            "SYSTEMY OPERACYJNE II", "ALGORYTMY I STRUKTURY DANYCH", "STYPENDIUM", "METODY PROBABILISTYCZNE",
            "METODY NUMERYCZNE", "TECHNIKA CYFROWA", "EGZAMIN", "PROGRAMOWANIE OBIEKTOWE I",
            "ARCHITEKTURA KOMPUTERÓW", "DESIGN THINKING", "POPRAWKA", "JĘZYK ANGIELSKI",
            "SIECI KOMPUTEROWE", "BAZY DANYCH"
        ]
        self.fields_data = [
            {"rect": pygame.Rect(30, 30, 140, 140), "label": field_labels_text_internal[0]},
            {"rect": pygame.Rect(165, 30, 110, 140), "label": field_labels_text_internal[1]},
            {"rect": pygame.Rect(270, 30, 110, 140), "label": field_labels_text_internal[2]},
            {"rect": pygame.Rect(375, 30, 110, 140), "label": field_labels_text_internal[3]},
            {"rect": pygame.Rect(480, 30, 63, 140), "label": field_labels_text_internal[4]},
            {"rect": pygame.Rect(539, 30, 105, 140), "label": field_labels_text_internal[5]},
            {"rect": pygame.Rect(640, 30, 112, 140), "label": field_labels_text_internal[6]},
            {"rect": pygame.Rect(748, 30, 110, 140), "label": field_labels_text_internal[7]},
            {"rect": pygame.Rect(854, 30, 140, 140), "label": field_labels_text_internal[8]},
            {"rect": pygame.Rect(854, 164, 140, 110), "label": field_labels_text_internal[9]},
            {"rect": pygame.Rect(854, 269, 140, 110), "label": field_labels_text_internal[10]},
            {"rect": pygame.Rect(854, 374, 140, 110), "label": field_labels_text_internal[11]},
            {"rect": pygame.Rect(854, 478, 140, 70), "label": field_labels_text_internal[12]},
            {"rect": pygame.Rect(854, 543, 140, 110), "label": field_labels_text_internal[13]},
            {"rect": pygame.Rect(854, 648, 140, 110), "label": field_labels_text_internal[14]},
            {"rect": pygame.Rect(854, 753, 140, 107), "label": field_labels_text_internal[15]},
            {"rect": pygame.Rect(854, 854, 140, 140), "label": field_labels_text_internal[16]},
            {"rect": pygame.Rect(748, 856, 110, 138), "label": field_labels_text_internal[17]},
            {"rect": pygame.Rect(641, 856, 110, 138), "label": field_labels_text_internal[18]},
            {"rect": pygame.Rect(540, 856, 105, 138), "label": field_labels_text_internal[19]},
            {"rect": pygame.Rect(480, 856, 65, 138), "label": field_labels_text_internal[20]},
            {"rect": pygame.Rect(375, 856, 110, 138), "label": field_labels_text_internal[21]},
            {"rect": pygame.Rect(270, 856, 110, 138), "label": field_labels_text_internal[22]},
            {"rect": pygame.Rect(165, 856, 110, 138), "label": field_labels_text_internal[23]},
            {"rect": pygame.Rect(30, 855, 140, 140), "label": field_labels_text_internal[24]},
            {"rect": pygame.Rect(30, 754, 140, 107), "label": field_labels_text_internal[25]},
            {"rect": pygame.Rect(30, 649, 140, 108), "label": field_labels_text_internal[26]},
            {"rect": pygame.Rect(30, 543, 140, 110), "label": field_labels_text_internal[27]},
            {"rect": pygame.Rect(30, 480, 140, 68), "label": field_labels_text_internal[28]},
            {"rect": pygame.Rect(30, 375, 140, 110), "label": field_labels_text_internal[29]},
            {"rect": pygame.Rect(30, 269, 140, 110), "label": field_labels_text_internal[30]},
            {"rect": pygame.Rect(30, 165, 140, 108), "label": field_labels_text_internal[31]},
        ]
        print(f"Zdefiniowano geometrię dla {len(self.fields_data)} pól na planszy.")
        if len(self.fields_data) != len(field_labels_text_internal) and field_labels_text_internal:
            print(f"OSTRZEŻENIE: Niezgodność liczby pól i etykiet!")

    def _render_text_multiline(self, text, font, color, max_width, bg_color=None, line_spacing_multiplier=0.85,
                               padding=2):
        words = text.replace('\n', ' \n ').split(' ')
        lines_text_processed = []
        current_line_text = ""
        for word in words:
            if word == '\n':
                if current_line_text: lines_text_processed.append(current_line_text.strip())
                lines_text_processed.append("")
                current_line_text = ""
                continue
            test_line = current_line_text + word + " "
            if font.size(test_line.strip())[0] <= max_width - 2 * padding:
                current_line_text = test_line
            else:
                if current_line_text.strip():
                    lines_text_processed.append(current_line_text.strip())
                if font.size(word)[0] > max_width - 2 * padding:
                    lines_text_processed.append(word)
                    current_line_text = ""
                else:
                    current_line_text = word + " "
        if current_line_text.strip():
            lines_text_processed.append(current_line_text.strip())
        if not lines_text_processed: return None
        rendered_line_surfaces = [font.render(line, True, color) for line in lines_text_processed if line.strip()]
        if not rendered_line_surfaces: return None
        actual_line_height = font.get_linesize()
        line_height_with_spacing = int(actual_line_height * line_spacing_multiplier)
        final_surface_width = 0
        for surf in rendered_line_surfaces:
            if surf.get_width() > final_surface_width: final_surface_width = surf.get_width()
        final_surface_width = min(final_surface_width + 2 * padding, max_width)
        total_height = (len(rendered_line_surfaces) - 1) * line_height_with_spacing + actual_line_height + 2 * padding
        total_height = max(total_height, actual_line_height + 2 * padding)
        final_surface = pygame.Surface((final_surface_width, total_height), pygame.SRCALPHA)
        if bg_color: final_surface.fill(bg_color)
        current_y = padding
        for line_surface in rendered_line_surfaces:
            line_x = (final_surface_width - line_surface.get_width()) // 2
            final_surface.blit(line_surface, (line_x, current_y))
            current_y += line_height_with_spacing
        return final_surface

    def draw(self, surface):
        if self.background_image:
            surface.blit(self.background_image, (self.board_offset_x_on_screen, self.board_offset_y_on_screen))

        if not self.field_label_font or not self.fields_data: return

        for field_data in self.fields_data:
            local_field_rect = field_data["rect"]
            label_text = field_data["label"]
            field_screen_rect = local_field_rect.move(self.board_offset_x_on_screen, self.board_offset_y_on_screen)

            label_bg_color = settings.FIELD_LABEL_BG_COLOR_SUBJECT  # Użyj stałych z settings
            if "STYPENDIUM" in label_text.upper() or "START" in label_text.upper():
                label_bg_color = settings.FIELD_LABEL_BG_COLOR_START
            elif "POPRAWKA" in label_text.upper() or "EGZAMIN" in label_text.upper():
                label_bg_color = settings.FIELD_LABEL_BG_COLOR_SPECIAL

            label_rect_for_text_bg = field_screen_rect.inflate(-8, -8)
            pygame.draw.rect(surface, label_bg_color, label_rect_for_text_bg, border_radius=5)
            pygame.draw.rect(surface, settings.FIELD_LABEL_TEXT_COLOR, label_rect_for_text_bg, 1, border_radius=5)

            if label_text:
                text_surface = self._render_text_multiline(label_text, self.field_label_font,
                                                           settings.FIELD_LABEL_TEXT_COLOR,
                                                           label_rect_for_text_bg.width,
                                                           padding=2)
                if text_surface:
                    text_rect = text_surface.get_rect(center=label_rect_for_text_bg.center)
                    surface.blit(text_surface, text_rect)


    def get_field_screen_rect(self, field_index):
        if 0 <= field_index < len(self.fields_data):
            local_field_rect = self.fields_data[field_index]["rect"]
            return local_field_rect.move(self.board_offset_x_on_screen, self.board_offset_y_on_screen)
        return None

    def get_field_screen_center(self, field_index):
        rect = self.get_field_screen_rect(field_index)
        if rect: return rect.center
        return None

    def get_total_fields(self):
        return len(self.fields_data)