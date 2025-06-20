# src/feedback_card.py
import pygame
import settings
import text_utility


class FeedbackCard:
    def __init__(self, message, feedback_type='success'):
        """
        Inicjalizuje kartę informacji zwrotnej.
        :param message: Tekst do wyświetlenia.
        :param feedback_type: 'success' (zielona) lub 'error' (czerwona).
        """
        self.message = message
        self.feedback_type = feedback_type
        self.is_visible = True
        self.animation_timer = 0.0  # W sekundach
        self.duration = settings.FEEDBACK_DURATION_SECONDS

        self._setup_appearance()
        self._setup_layout()

    def _setup_appearance(self):
        """Ustawia kolory i czcionkę na podstawie typu feedbacku."""
        if self.feedback_type == 'success':
            self.bg_color = settings.FEEDBACK_SUCCESS_BG_COLOR
            self.border_color = settings.FEEDBACK_SUCCESS_BORDER_COLOR
        else:  # 'error'
            self.bg_color = settings.FEEDBACK_ERROR_BG_COLOR
            self.border_color = settings.FEEDBACK_ERROR_BORDER_COLOR

        try:
            self.font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.FEEDBACK_FONT_SIZE)
        except Exception as e:
            print(f"Błąd ładowania czcionki dla feedbacku: {e}")
            self.font = pygame.font.SysFont(None, settings.FEEDBACK_FONT_SIZE)

    def _setup_layout(self):
        """Ustawia pozycję karty na ekranie."""
        width = settings.FEEDBACK_CARD_WIDTH
        height = settings.FEEDBACK_CARD_HEIGHT
        self.card_rect = pygame.Rect(
            (settings.GAMEPLAY_SCREEN_WIDTH - width) // 2,
            (settings.GAMEPLAY_SCREEN_HEIGHT - height) // 2,
            width,
            height
        )

    def update(self, dt_seconds):
        """Aktualizuje timer i ukrywa kartę po upływie czasu."""
        if self.is_visible:
            self.animation_timer += dt_seconds
            if self.animation_timer >= self.duration:
                self.is_visible = False
                print("FeedbackCard: Czas minął, ukrywam kartę.")

    def draw(self, surface):
        """Rysuje kartę na podanej powierzchni."""
        if not self.is_visible:
            return

        # Użyj SRCALPHA, aby poprawnie obsłużyć przezroczystość kolorów
        card_surface = pygame.Surface(self.card_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(card_surface, self.bg_color, card_surface.get_rect(),
                         border_radius=settings.FEEDBACK_CARD_BORDER_RADIUS)
        pygame.draw.rect(card_surface, self.border_color, card_surface.get_rect(), 4,
                         border_radius=settings.FEEDBACK_CARD_BORDER_RADIUS)

        # Renderuj tekst na tej tymczasowej powierzchni
        text_utility.render_text_in_rect(
            surface=card_surface,
            text=self.message,
            font_path=settings.FONT_PATH_PT_SERIF_REGULAR,  # Przekaż ścieżkę
            initial_font_size=settings.FEEDBACK_FONT_SIZE,  # Przekaż rozmiar
            color=settings.FEEDBACK_TEXT_COLOR,
            rect=card_surface.get_rect(),
            vertical_align='center'
        )

        surface.blit(card_surface, self.card_rect)