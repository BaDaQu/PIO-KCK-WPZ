# src/board_screen.py
import pygame

# Stałe dla kolorów etykiet (możesz dostosować)
FIELD_LABEL_TEXT_COLOR = (10, 10, 10)
FIELD_LABEL_BG_COLOR_SUBJECT = (230, 230, 210)
FIELD_LABEL_BG_COLOR_SPECIAL = (200, 220, 240)
FIELD_LABEL_BG_COLOR_START = (180, 240, 180)


class Board:
    def __init__(self, screen_width_gameplay, screen_height_gameplay):
        self.board_render_width = 1024  # Szerokość obrazka tła planszy
        self.board_render_height = 1024  # Wysokość obrazka tła planszy
        self.display_surface_width = screen_width_gameplay  # Szerokość powierzchni, na której plansza jest rysowana
        self.display_surface_height = screen_height_gameplay  # Wysokość powierzchni

        self.background_image = None
        self.fields_data = []  # Zmieniono z fields_rects na fields_data
        self.field_labels_text = []
        self.field_label_font = None

        self._load_assets()
        self._define_field_labels_and_geometry()  # Połączono dwie funkcje

    def _load_assets(self):
        try:
            # Pamiętaj, aby ścieżka była poprawna względem uruchamianego skryptu main.py
            self.background_image = pygame.image.load("../assets/images/PLANSZA_GRY.png").convert()
            # Skalujemy obrazek tła planszy do docelowych wymiarów renderowania
            self.background_image = pygame.transform.scale(self.background_image,
                                                           (self.board_render_width, self.board_render_height))
            print("Plansza załadowana i przeskalowana.")
        except Exception as e:
            print(f"Błąd ładowania obrazka planszy: {e}")
            self.background_image = pygame.Surface((self.board_render_width, self.board_render_height))
            self.background_image.fill((200, 180, 160))  # Kolor awaryjny

        try:
            self.field_label_font = pygame.font.Font("../assets/fonts/PTSerif-Regular.ttf", 16)
        except Exception as e:
            print(f"Błąd ładowania czcionki dla etykiet pól: {e}")
            self.field_label_font = pygame.font.SysFont(None, 20)

    def _define_field_labels_and_geometry(self):
        """
        Definiuje etykiety pól oraz ich indywidualne prostokąty (x, y, width, height)
        Współrzędne (x, y) są względem lewego górnego rogu obrazka planszy (0,0) o wymiarach
        self.board_render_width x self.board_render_height.
        """
        self.field_labels_text = [
            "START", "ANALIZA MAT. I", "ALGEBRA LINIOWA", "OPROGRAMOWANIE UŻYTKOWE", "STYPENDIUM",
            "PROGRAMOWANIE SKRYPTOWE", "BHP", "FIZYKA", "EGZAMIN", "MATEMATYKA DYSKRETNA",
            "PODSTAWY ELEKTROTECHNIKI", "PODSTAWY PROGRAMOWANIA I", "POPRAWKA", "PODSTAWY PROGRAMOWANIA II",
            "SYSTEMY OPERACYJNE I", "ANALIZA MAT. II", "EGZAMIN", "PODSTAWY GRAFIKI KOMP.",
            "SYSTEMY OPERACYJNE II", "ALGORYTMY I STRUKTURY DANYCH", "STYPENDIUM", "METODY PROBABILISTYCZNE",
            "METODY NUMERYCZNE", "TECHNIKA CYFROWA", "EGZAMIN", "PROGRAMOWANIE OBIEKTOWE I",
            "ARCHITEKTURA KOMPUTERÓW", "DESIGN THINKING", "POPRAWKA", "JĘZYK ANGIELSKI",
            "SIECI KOMPUTEROWE", "BAZY DANYCH"
        ]
        print(f"Zdefiniowano {len(self.field_labels_text)} etykiet pól.")


        # Przykładowe wymiary dla pól
        default_field_width = 1
        default_field_height = 1

        self.fields_data = [
            # Górna krawędź (pola 0-9)
            {"rect": pygame.Rect(30, 30, 140, 140),
             "label": self.field_labels_text[0]},  # START
            {"rect": pygame.Rect(165, 30, 110, 140),
             "label": self.field_labels_text[1]}, # ANALIZA MAT. I
            {"rect": pygame.Rect(270, 30, 110, 140  ),
             "label": self.field_labels_text[2]}, # ALGEBRA LINIOWA
            {"rect": pygame.Rect(375, 30, 110, 140),
             "label": self.field_labels_text[3]}, # OPROGRAMOWANIE UŻYTKOWE
            {"rect": pygame.Rect(480, 30, 63, 140),
             "label": self.field_labels_text[4]},  # STYPENDIUM
            {"rect": pygame.Rect(539, 30, 105 , 140),
             "label": self.field_labels_text[5]}, # PROGRAMOWANIE SKRYPTOWE
            {"rect": pygame.Rect(640, 30, 112, 140),
             "label": self.field_labels_text[6]}, # BHP
            {"rect": pygame.Rect(748, 30, 110, 140),
             "label": self.field_labels_text[7]}, # FIZYKA
            {"rect": pygame.Rect(854, 30, 140, 140),
             "label": self.field_labels_text[8]},  # EGZAMIN
            {"rect": pygame.Rect(854, 164, 140, 110),
             "label": self.field_labels_text[9]}, # MATEMATYKA DYSKRETNA


            {"rect": pygame.Rect(854, 269, 140, 110),
             "label": self.field_labels_text[10]}, # PODSTAWY ELEKTROTECHNIKI
            {"rect": pygame.Rect(854, 374, 140, 110),
             "label": self.field_labels_text[11]}, # PODSTAWY PROGRAMOWANIA I
            {"rect": pygame.Rect(854, 478, 140, 70),
             "label": self.field_labels_text[12]},  # POPRAWKA
            {"rect": pygame.Rect(854, 543, 140, 110),
             "label": self.field_labels_text[13]}, # PODSTAWY PROGRAMOWANIA II
            {"rect": pygame.Rect(854, 648, 140, 110),
             "label": self.field_labels_text[14]}, # SYSTEMY OPERACYJNE I
            {"rect": pygame.Rect(854, 753, 140, 107),
             "label": self.field_labels_text[15]}, # ANALIZA MAT. II
            {"rect": pygame.Rect(854, 854, 140, 140),
             "label": self.field_labels_text[16]},  # EGZAMIN


            {"rect": pygame.Rect(748, 856, 110, 138),
             "label": self.field_labels_text[17]}, # PODSTAWY GRAFIKI KOMP.
            {"rect": pygame.Rect(641, 856, 110, 138),
             "label": self.field_labels_text[18]}, # SYSTEMY OPERACYJNE II
            {"rect": pygame.Rect(540, 856, 105, 138),
             "label": self.field_labels_text[19]}, # ALGORYTMY I STRUKTURY DANYCH
            {"rect": pygame.Rect(480, 856, 65, 138),
             "label": self.field_labels_text[20]},  # STYPENDIUM
            {"rect": pygame.Rect(375, 856, 110, 138),
             "label": self.field_labels_text[21]}, # METODY PROBABILISTYCZNE
            {"rect": pygame.Rect(270, 856, 110, 138),
             "label": self.field_labels_text[22]}, # METODY NUMERYCZNE
            {"rect": pygame.Rect(165, 856, 110, 138),
             "label": self.field_labels_text[23]}, # TECHNIKA CYFROWA
            {"rect": pygame.Rect(30, 855, 140, 140),
             "label": self.field_labels_text[24]},  # EGZAMIN
            {"rect": pygame.Rect(30, 754, 140, 107),
             "label": self.field_labels_text[25]},  # PROGRAMOWANIE OBIEKTOWE I

            {"rect": pygame.Rect(30, 649, 140, 108),
             "label": self.field_labels_text[26]}, # ARCHITEKTURA KOMPUTERÓW
            {"rect": pygame.Rect(30, 543, 140, 110),
             "label": self.field_labels_text[27]}, # DESIGN THINKING
            {"rect": pygame.Rect(30, 480, 140, 68),
             "label": self.field_labels_text[28]},  # POPRAWKA
            {"rect": pygame.Rect(30, 375, 140, 110),
             "label": self.field_labels_text[29]}, # JĘZYK ANGIELSKI
            {"rect": pygame.Rect(30, 269, 140, 110),
             "label": self.field_labels_text[30]}, # SIECI KOMPUTEROWE
            {"rect": pygame.Rect(30, 165, 140, 108),
             "label": self.field_labels_text[31]}, # BAZY DANYCH
        ]
        # =================================================

        print(f"Zdefiniowano geometrię dla {len(self.fields_data)} pól na planszy.")
        if len(self.fields_data) != len(self.field_labels_text) and self.field_labels_text:
            print(
                f"OSTRZEŻENIE: Liczba zdefiniowanych prostokątów pól ({len(self.fields_data)}) "
                f"nie zgadza się z liczbą etykiet ({len(self.field_labels_text)})!"
            )

    def _render_text_multiline(self, text, rect, font, color, bg_color=None, original_text_for_recursion_check=None):
        # ... (ta funkcja pozostaje bez większych zmian, ale upewnij się, że działa poprawnie) ...
        # Możesz chcieć dodać marginesy wewnętrzne dla tekstu w polu.
        # W tej wersji zakładamy, że rect przekazany do tej funkcji to już pomniejszony prostokąt
        # na etykietę, a nie cały prostokąt pola.
        lines = text.splitlines()
        if not lines:
            if text.strip():
                lines = [text.strip()]
            else:
                return None, None

        rendered_lines = []
        max_width = 0
        total_height_calculated = 0
        line_spacing = font.get_linesize() * 0.85

        for line_text in lines:
            line_surface = font.render(line_text, True, color)
            rendered_lines.append(line_surface)
            if line_surface.get_width() > max_width:
                max_width = line_surface.get_width()
            total_height_calculated += int(line_spacing)

        if not rendered_lines: return None, None

        padding = 2  # Mniejszy padding, bo rect jest już mniejszy
        available_width = rect.width - 2 * padding

        if original_text_for_recursion_check == text and max_width > available_width:
            pass
        elif max_width > available_width:
            words = text.replace('\n', ' ').split(' ')
            new_lines_text = []
            current_line_text = ""
            for word in words:
                word_width = font.size(word)[0]
                if word_width > available_width:
                    if current_line_text.strip():
                        new_lines_text.append(current_line_text.strip())
                    new_lines_text.append(word)
                    current_line_text = ""
                    continue

                test_line = current_line_text + word + " "
                if font.size(test_line)[0] < available_width:
                    current_line_text = test_line
                else:
                    if current_line_text.strip():
                        new_lines_text.append(current_line_text.strip())
                    current_line_text = word + " "
            if current_line_text.strip():
                new_lines_text.append(current_line_text.strip())
            processed_text = "\n".join(filter(None, new_lines_text))
            if processed_text == text:
                pass
            else:
                return self._render_text_multiline(processed_text, rect, font, color, bg_color,
                                                   original_text_for_recursion_check=text)

        actual_num_lines = len(rendered_lines) if rendered_lines else 1
        final_surface_height = int((actual_num_lines - 1) * line_spacing + font.get_height())
        final_surface_height = max(font.get_height(), final_surface_height)

        final_surface = pygame.Surface((max_width, final_surface_height), pygame.SRCALPHA)
        if bg_color:  # bg_color jest teraz stosowany do final_surface, nie do indywidualnych linii
            final_surface.fill(bg_color)  # To może nie być potrzebne jeśli label_rect_bg jest rysowany osobno

        current_y = 0
        for line_surface in rendered_lines:
            line_x = (max_width - line_surface.get_width()) // 2
            final_surface.blit(line_surface, (line_x, current_y))
            current_y += int(line_spacing)

        final_rect = final_surface.get_rect(center=rect.center)
        return final_surface, final_rect

    def draw(self, surface):
        # Obliczanie offsetu, aby plansza 1024x1024 była rysowana po prawej stronie
        # ekranu rozgrywki (zakładając, że lewy panel ma szerokość LEFT_PANEL_WIDTH)
        # W gameplay_screen.py LEFT_PANEL_WIDTH = 412, a plansza ma być po prawej.
        # Więc x_offset planszy to po prostu szerokość lewego panelu.
        board_offset_x = self.display_surface_width - self.board_render_width
        board_offset_y = (self.display_surface_height - self.board_render_height) // 2  # Wycentrowanie w pionie

        if self.background_image:
            surface.blit(self.background_image, (board_offset_x, board_offset_y))

        if not self.field_label_font or not self.fields_data:
            return

        for i, field_info in enumerate(self.fields_data):
            # field_local_rect to prostokąt zdefiniowany w self.fields_data,
            # jego współrzędne są względem obrazka planszy (0,0)
            field_local_rect = field_info["rect"]
            label_text = field_info["label"]

            # Przesuń lokalny prostokąt pola o offset planszy na ekranie
            field_screen_rect = field_local_rect.move(board_offset_x, board_offset_y)

            label_bg_color = FIELD_LABEL_BG_COLOR_SUBJECT
            if "STYPENDIUM" in label_text.upper() or "START" in label_text.upper():
                label_bg_color = FIELD_LABEL_BG_COLOR_START
            elif "POPRAWKA" in label_text.upper() or "EGZAMIN" in label_text.upper():
                label_bg_color = FIELD_LABEL_BG_COLOR_SPECIAL

            # Prostokąt dla tła etykiety (nieco mniejszy niż całe pole)
            label_rect_bg = field_screen_rect.inflate(-8, -8)  # Pomniejsz o 4px z każdej strony
            pygame.draw.rect(surface, label_bg_color, label_rect_bg, border_radius=5)
            pygame.draw.rect(surface, FIELD_LABEL_TEXT_COLOR, label_rect_bg, 1, border_radius=5)  # Ramka

            if label_text:
                # Przekazujemy label_rect_bg do render_text_multiline, aby tekst był wycentrowany w tym mniejszym prostokącie
                text_surface, text_rect = self._render_text_multiline(label_text, label_rect_bg, self.field_label_font,
                                                                      FIELD_LABEL_TEXT_COLOR,
                                                                      original_text_for_recursion_check=None)
                if text_surface and text_rect:
                    surface.blit(text_surface, text_rect)

    def get_field_screen_rect(self, field_index):
        if 0 <= field_index < len(self.fields_data):
            local_field_rect = self.fields_data[field_index]["rect"]
            board_offset_x = self.display_surface_width - self.board_render_width
            board_offset_y = (self.display_surface_height - self.board_render_height) // 2
            return local_field_rect.move(board_offset_x, board_offset_y)
        return None

    def get_field_screen_center(self, field_index):
        rect = self.get_field_screen_rect(field_index)
        if rect:
            return rect.center
        return None

    def get_total_fields(self):
        return len(self.fields_data)