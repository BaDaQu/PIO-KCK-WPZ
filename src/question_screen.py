# src/question_screen.py
import pygame
import settings
import text_utility
import sound_manager


# --- Funkcja Pomocnicza (pozostaje bez zmian) ---
def apply_rounded_corners_mask(image, radius):
    """Zwraca nową powierzchnię z obrazkiem, który ma zaokrąglone rogi."""
    if radius <= 0:
        return image.copy()

    rounded_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    rect = image.get_rect()

    mask = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 0))
    pygame.draw.rect(mask, (255, 255, 255, 255), rect, border_radius=radius)

    rounded_image.blit(image, (0, 0))
    rounded_image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    return rounded_image


class QuestionCard:
    def __init__(self, question_data, subject_name):
        self.question_data = question_data
        self.subject_name = subject_name
        self.is_visible = True
        self.answer_buttons = []
        self.state = 'ANSWERING'  # Możliwe stany: 'ANSWERING', 'SHOWING_RESULT'
        self.result_timer = 0.0  # Timer dla pokazywania wyniku
        self.player_choice_index = None  # Indeks odpowiedzi wybranej przez gracza
        self._load_assets()
        self._setup_layout()

    def _load_assets(self):
        """Ładuje zasoby potrzebne dla karty pytania."""
        try:
            # Ładujemy oryginalny, prostokątny obrazek
            original_card_bg_image = pygame.image.load(settings.IMAGE_PATH_QUESTION_CARD_BG).convert_alpha()
            # Stosujemy zaokrąglenie
            self.card_bg_image = apply_rounded_corners_mask(
                original_card_bg_image,
                settings.QUESTION_CARD_BORDER_RADIUS
            )
        except Exception as e:
            print(f"Błąd ładowania lub przetwarzania tła karty pytania: {e}")
            # Tworzenie zastępczego, już zaokrąglonego prostokąta
            self.card_bg_image = pygame.Surface((settings.QUESTION_CARD_WIDTH, settings.QUESTION_CARD_HEIGHT),
                                                pygame.SRCALPHA)
            pygame.draw.rect(self.card_bg_image, settings.QUESTION_CARD_BG_COLOR, self.card_bg_image.get_rect(),
                             border_radius=settings.QUESTION_CARD_BORDER_RADIUS)

        # Ładowanie czcionki dla etykiet A, B, C, D (pozostaje bez zmian)
        try:
            self.answer_label_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR,
                                                      settings.QUESTION_CARD_ANSWER_LABEL_FONT_SIZE)
        except Exception as e:
            print(f"Błąd ładowania czcionki dla etykiet odpowiedzi: {e}")
            self.answer_label_font = pygame.font.SysFont(None, settings.QUESTION_CARD_ANSWER_LABEL_FONT_SIZE)

    def _setup_layout(self):
        """Ustawia pozycje i prostokąty dla tekstu i przycisków na podstawie `settings`."""
        self.card_rect = self.card_bg_image.get_rect(
            center=(settings.GAMEPLAY_SCREEN_WIDTH // 2, settings.GAMEPLAY_SCREEN_HEIGHT // 2)
        )
        self.question_text_screen_rect = settings.QUESTION_TEXT_AREA_RECT.move(self.card_rect.left, self.card_rect.top)

        # Użyj indywidualnych prostokątów z settings
        self.answer_buttons = []
        local_answer_rects = [
            settings.ANSWER_A_CLICK_RECT, settings.ANSWER_B_CLICK_RECT,
            settings.ANSWER_C_CLICK_RECT, settings.ANSWER_D_CLICK_RECT
        ]
        for i, local_rect in enumerate(local_answer_rects):
            screen_rect = local_rect.move(self.card_rect.left, self.card_rect.top)
            self.answer_buttons.append({"rect": screen_rect, "index": i, "hover": False})

    def show_result(self, player_choice_idx):
        """Zmienia stan karty na pokazywanie wyniku i zapisuje wybór gracza."""
        self.state = 'SHOWING_RESULT'
        self.player_choice_index = player_choice_idx
        self.result_timer = 0.0  # Resetuj timer dla czasu wyświetlania wyniku

    def update(self, dt_seconds):
        """Aktualizuje logikę karty, np. timer dla pokazywania wyniku."""
        if self.state == 'SHOWING_RESULT':
            self.result_timer += dt_seconds
            if self.result_timer >= settings.FEEDBACK_DURATION_SECONDS:
                self.is_visible = False  # Karta powinna zniknąć po upływie czasu

    def handle_event(self, event, mouse_pos):
        """Obsługuje input dla karty pytania (tylko w stanie 'ANSWERING')."""
        if not self.is_visible or self.state != 'ANSWERING':
            return None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.answer_buttons:
                if button["rect"].collidepoint(mouse_pos):
                    # Dźwięk kliknięcia jest teraz odtwarzany w game_logic.process_player_answer
                    # lub bezpośrednio przed wywołaniem process_player_answer w main.py
                    return button["index"]  # Zwróć tylko indeks, logikę przenosimy

        if event.type == pygame.KEYDOWN:
            chosen_index_key = -1
            if event.key == pygame.K_a or event.key == pygame.K_1 or event.key == pygame.K_KP_1:
                chosen_index_key = 0
            elif event.key == pygame.K_b or event.key == pygame.K_2 or event.key == pygame.K_KP_2:
                chosen_index_key = 1
            elif event.key == pygame.K_c or event.key == pygame.K_3 or event.key == pygame.K_KP_3:
                chosen_index_key = 2
            elif event.key == pygame.K_d or event.key == pygame.K_4 or event.key == pygame.K_KP_4:
                chosen_index_key = 3

            if chosen_index_key != -1:
                return chosen_index_key  # Zwróć indeks wybranej odpowiedzi

        return None

    def update_hover(self, mouse_pos):
        """Aktualizuje stan najechania myszą na przyciski odpowiedzi (tylko w stanie 'ANSWERING')."""
        if not self.is_visible or self.state != 'ANSWERING':
            for button in self.answer_buttons: button["hover"] = False  # Wyłącz hover, gdy nie odpowiadamy
            return
        for button in self.answer_buttons:
            button["hover"] = button["rect"].collidepoint(mouse_pos)

    def draw(self, surface):
        """Rysuje kartę pytania na podanej powierzchni."""
        if not self.is_visible:
            return

        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Półprzezroczyste tło
        surface.blit(overlay, (0, 0))

        surface.blit(self.card_bg_image, self.card_rect)  # Tło karty

        # Rysowanie Tekstu Pytania
        text_utility.render_text(
            surface=surface,
            text=self.question_data["question_text"],
            font_path=settings.FONT_PATH_HUNINN_REGULAR,
            initial_font_size=settings.QUESTION_CARD_QUESTION_FONT_SIZE,
            color=settings.QUESTION_CARD_TEXT_COLOR,
            rect=self.question_text_screen_rect,
            vertical_align='center'
        )

        # Rysowanie Odpowiedzi
        answer_labels = ["A", "B", "C", "D"]
        correct_answer_idx = self.question_data["correct_answer_index"]

        for i, answer_text in enumerate(self.question_data["answers"]):
            button_info = self.answer_buttons[i]

            # Rysowanie tła dla odpowiedzi (feedback lub hover)
            if self.state == 'SHOWING_RESULT':
                if i == correct_answer_idx:
                    pygame.draw.rect(surface, settings.ANSWER_CORRECT_COLOR, button_info["rect"],
                                     border_radius=settings.ANSWER_HOVER_BORDER_RADIUS)
                elif i == self.player_choice_index:  # Podświetl błędny wybór gracza
                    pygame.draw.rect(surface, settings.ANSWER_INCORRECT_COLOR, button_info["rect"],
                                     border_radius=settings.ANSWER_HOVER_BORDER_RADIUS)
            elif self.state == 'ANSWERING' and button_info["hover"]:
                pygame.draw.rect(surface, settings.ANSWER_BUTTON_HOVER_COLOR, button_info["rect"],
                                 border_radius=settings.ANSWER_HOVER_BORDER_RADIUS)

            # Rysowanie etykiet A, B, C, D
            label_surf = self.answer_label_font.render(answer_labels[i], True, settings.QUESTION_CARD_TEXT_COLOR)
            label_rect = label_surf.get_rect(
                centerx=button_info["rect"].left + settings.ANSWER_LABEL_CENTER_X,
                centery=button_info["rect"].centery
            )
            surface.blit(label_surf, label_rect)

            # Definiowanie obszaru dla tekstu odpowiedzi
            answer_text_area = button_info["rect"].inflate(
                -settings.ANSWER_TEXT_AREA_PADDING_X * 2,
                -settings.ANSWER_TEXT_AREA_PADDING_Y * 2
            )
            answer_text_area.left = button_info["rect"].left + settings.ANSWER_TEXT_AREA_PADDING_X

            # Renderowanie tekstu odpowiedzi
            text_utility.render_text(
                surface=surface,
                text=answer_text,
                font_path=settings.FONT_PATH_HUNINN_REGULAR,
                initial_font_size=settings.QUESTION_CARD_ANSWER_FONT_SIZE,
                color=settings.QUESTION_CARD_TEXT_COLOR,
                rect=answer_text_area,
                vertical_align='center'
            )