# src/board_screen.py
import pygame

# Stałe dla kolorów etykiet (możesz dostosować)
FIELD_LABEL_TEXT_COLOR = (10, 10, 10)  # Bardzo ciemny szary/czarny
FIELD_LABEL_BG_COLOR_SUBJECT = (230, 230, 210)  # Jasny beż dla przedmiotów
FIELD_LABEL_BG_COLOR_SPECIAL = (200, 220, 240)  # Jasny niebieski dla specjalnych
FIELD_LABEL_BG_COLOR_START = (180, 240, 180)  # Jasny zielony dla startu


class Board:
    def __init__(self, screen_width_gameplay, screen_height_gameplay):
        self.board_render_width = 1024
        self.board_render_height = 1024
        self.display_surface_width = screen_width_gameplay
        self.display_surface_height = screen_height_gameplay

        self.background_image = None
        self.fields_rects = []
        self.field_labels_text = []
        self.field_label_font = None

        self._load_assets()
        self._define_field_labels()
        self._define_fields_geometry()

    def _load_assets(self):
        try:
            self.background_image = pygame.image.load("../assets/images/PLANSZA_GRY.png").convert()
            self.background_image = pygame.transform.scale(self.background_image,
                                                           (self.board_render_width, self.board_render_height))
            print("Plansza załadowana i przeskalowana do 1024x1024.")
        except Exception as e:
            print(f"Błąd ładowania obrazka planszy: {e}")
            self.background_image = pygame.Surface((self.board_render_width, self.board_render_height))
            self.background_image.fill((200, 180, 160))

        try:
            self.field_label_font = pygame.font.Font("../assets/fonts/PTSerif-Regular.ttf", 16)  # Dostosuj rozmiar!
        except Exception as e:
            print(f"Błąd ładowania czcionki dla etykiet pól: {e}")
            self.field_label_font = pygame.font.SysFont(None, 20)

    def _define_field_labels(self):
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

    def _define_fields_geometry(self):
        self.fields_rects = []
        if not self.field_labels_text:
            print("OSTRZEŻENIE: Brak etykiet, nie można zdefiniować geometrii pól!")
            return

        num_fields_total = len(self.field_labels_text)

        # Przykład dla 32 pól: 10 na górze/dole (w tym rogi), 8 po bokach (w tym rogi)
        # To oznacza 9 pól "środkowych" na górze/dole i 7 pól "środkowych" po bokach
        fields_on_top_edge = 10  # Łącznie z rogami
        fields_on_side_edge = 8  # Łącznie z rogami

        # Wymiary pola - dostosuj tak, aby zmieściły się na Twojej grafice planszy 1024x1024
        field_w = self.board_render_width // fields_on_top_edge
        field_h = self.board_render_height // fields_on_side_edge
        # Użyj mniejszego z nich dla kwadratowych pól, lub dostosuj indywidualnie
        field_dim = min(field_w, field_h) - 4  # -4 dla małego marginesu między polami
        field_w = field_dim
        field_h = field_dim

        # Marginesy, aby wycentrować siatkę pól na obrazku planszy (jeśli potrzeba)
        # Te wartości mogą wymagać precyzyjnego dostrojenia do Twojej grafiki
        # Tutaj zakładamy, że pola wypełniają większość planszy 1024x1024
        outer_margin_x = (self.board_render_width - (fields_on_top_edge * field_w + (fields_on_top_edge - 1) * 2)) // 2
        outer_margin_y = (self.board_render_height - (
                    fields_on_side_edge * field_h + (fields_on_side_edge - 1) * 2)) // 2
        outer_margin_x = max(5, outer_margin_x)  # Minimalny margines
        outer_margin_y = max(5, outer_margin_y)

        current_field_idx = 0

        # Górna krawędź (od lewej do prawej)
        y = outer_margin_y
        for i in range(fields_on_top_edge):
            if current_field_idx >= num_fields_total: break
            x = outer_margin_x + i * (field_w + 2)  # +2 to mały odstęp
            self.fields_rects.append(pygame.Rect(x, y, field_w, field_h))
            current_field_idx += 1

        # Prawa krawędź (z góry na dół, pomijając już dodany róg)
        # Ostatnie dodane pole to prawy górny róg
        start_x_right = self.fields_rects[-1].left
        for i in range(1, fields_on_side_edge):  # Zaczynamy od 1, bo róg już jest
            if current_field_idx >= num_fields_total: break
            y = outer_margin_y + i * (field_h + 2)
            self.fields_rects.append(pygame.Rect(start_x_right, y, field_w, field_h))
            current_field_idx += 1

        # Dolna krawędź (od prawej do lewej, pomijając już dodany róg)
        start_y_bottom = self.fields_rects[-1].top
        for i in range(1, fields_on_top_edge):  # Zaczynamy od 1
            if current_field_idx >= num_fields_total: break
            x = outer_margin_x + (fields_on_top_edge - 1 - i) * (field_w + 2)  # Od prawej
            self.fields_rects.append(pygame.Rect(x, start_y_bottom, field_w, field_h))
            current_field_idx += 1

        # Lewa krawędź (z dołu do góry, pomijając już dodane rogi)
        start_x_left = self.fields_rects[0].left  # X pola START
        for i in range(1, fields_on_side_edge - 1):  # -1 bo pomijamy dolny i górny róg
            if current_field_idx >= num_fields_total: break
            y = outer_margin_y + (fields_on_side_edge - 1 - i) * (field_h + 2)  # Od dołu
            self.fields_rects.append(pygame.Rect(start_x_left, y, field_w, field_h))
            current_field_idx += 1

        print(f"Zdefiniowano geometrię dla {len(self.fields_rects)} pól na planszy.")
        if len(self.fields_rects) != num_fields_total and num_fields_total > 0:
            print(
                f"OSTRZEŻENIE: Liczba zdefiniowanych prostokątów pól ({len(self.fields_rects)}) nie zgadza się z liczbą etykiet ({num_fields_total})!")

    def _render_text_multiline(self, text, rect, font, color, bg_color=None, original_text_for_recursion_check=None):
        lines = text.splitlines()
        if not lines:
            if text.strip():
                lines = [text.strip()]
            else:
                return None, None

        rendered_lines = []
        max_width = 0
        total_height_calculated = 0  # Zmieniono nazwę z total_height
        line_spacing = font.get_linesize() * 0.85  # Można dostosować

        for line_text in lines:
            line_surface = font.render(line_text, True, color)
            rendered_lines.append(line_surface)
            if line_surface.get_width() > max_width:
                max_width = line_surface.get_width()
            total_height_calculated += int(line_spacing)

        if not rendered_lines: return None, None

        padding = 4
        available_width = rect.width - 2 * padding

        if original_text_for_recursion_check == text and max_width > available_width:
            # print(f"OSTRZEŻENIE Rekurencji: Tekst '{text}' zbyt szeroki i nie uległ zmianie.")
            # Przechodzimy do renderowania bez dalszej rekurencji
            pass  # Pozwól kodowi poniżej wyrenderować to, co jest

        elif max_width > available_width:
            words = text.replace('\n', ' ').split(' ')
            new_lines_text = []
            current_line_text = ""  # Zmieniono nazwę z current_line
            for word in words:
                # Sprawdź, czy pojedyncze słowo nie jest za długie
                word_width = font.size(word)[0]
                if word_width > available_width:
                    # Jeśli słowo jest za długie, dodajemy je w nowej linii (może być obcięte przez Pygame)
                    # Można by tu dodać logikę dzielenia słów, ale to bardziej skomplikowane
                    if current_line_text.strip():
                        new_lines_text.append(current_line_text.strip())
                    new_lines_text.append(word)  # Dodaj zbyt długie słowo, aby je zobaczyć
                    current_line_text = ""
                    continue  # Przejdź do następnego słowa

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

            # Zapobiegaj rekurencji, jeśli tekst się nie zmienił po przetworzeniu
            if processed_text == text:
                # print(f"OSTRZEŻENIE Rekurencji (2): Tekst '{text}' nie zmienił się po próbie łamania.")
                pass  # Pozwól kodowi poniżej wyrenderować
            else:
                return self._render_text_multiline(processed_text, rect, font, color, bg_color,
                                                   original_text_for_recursion_check=text)

        # Upewnij się, że jest co najmniej jedna linia, aby uniknąć ujemnej wysokości
        actual_num_lines = len(rendered_lines) if rendered_lines else 1
        final_surface_height = int((actual_num_lines - 1) * line_spacing + font.get_height())
        final_surface_height = max(font.get_height(), final_surface_height)  # Nie mniejsza niż wysokość jednej linii

        final_surface = pygame.Surface((max_width, final_surface_height), pygame.SRCALPHA)
        if bg_color:
            final_surface.fill(bg_color)

        current_y = 0
        for line_surface in rendered_lines:
            line_x = (max_width - line_surface.get_width()) // 2
            final_surface.blit(line_surface, (line_x, current_y))
            current_y += int(line_spacing)

        final_rect = final_surface.get_rect(center=rect.center)
        return final_surface, final_rect

    def draw(self, surface):
        board_offset_x = self.display_surface_width - self.board_render_width
        board_offset_y = (self.display_surface_height - self.board_render_height) // 2

        if self.background_image:
            surface.blit(self.background_image, (board_offset_x, board_offset_y))

        if not self.field_label_font or not self.fields_rects:  # Dodatkowe sprawdzenie
            # print("Nie można rysować etykiet: brak czcionki lub geometrii pól.")
            return

        for i, field_local_rect in enumerate(self.fields_rects):
            if i >= len(self.field_labels_text):  # Zabezpieczenie przed wyjściem poza zakres etykiet
                # print(f"Brak etykiety dla pola {i}")
                continue

            field_screen_rect = field_local_rect.move(board_offset_x, board_offset_y)
            label_text = self.field_labels_text[i]

            label_bg_color = FIELD_LABEL_BG_COLOR_SUBJECT
            if "STYPENDIUM" in label_text.upper() or "START" in label_text.upper():
                label_bg_color = FIELD_LABEL_BG_COLOR_START
            elif "POPRAWKA" in label_text.upper() or "EGZAMIN" in label_text.upper():
                label_bg_color = FIELD_LABEL_BG_COLOR_SPECIAL

            label_rect_bg = field_screen_rect.inflate(-8, -8)
            pygame.draw.rect(surface, label_bg_color, label_rect_bg, border_radius=5)
            pygame.draw.rect(surface, FIELD_LABEL_TEXT_COLOR, label_rect_bg, 1, border_radius=5)

            if label_text:
                text_surface, text_rect = self._render_text_multiline(label_text, label_rect_bg, self.field_label_font,
                                                                      FIELD_LABEL_TEXT_COLOR,
                                                                      original_text_for_recursion_check=None)
                if text_surface and text_rect:
                    surface.blit(text_surface, text_rect)

            # Debugowanie numerów pól (możesz odkomentować w razie potrzeby)
            # num_font = pygame.font.SysFont(None, 18)
            # num_text_surface = num_font.render(str(i), True, (255,0,0))
            # surface.blit(num_text_surface, (field_screen_rect.x + 2, field_screen_rect.y + 2))

    def get_field_screen_rect(self, field_index):
        if 0 <= field_index < len(self.fields_rects):
            local_field_rect = self.fields_rects[field_index]
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
        return len(self.fields_rects)