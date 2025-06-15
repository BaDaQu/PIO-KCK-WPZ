# src/question_screen.py
import pygame
import settings
from button import Button

# --- Zmienne Modułu ---
question_background_surface = None
question_font = None
answer_font = None
answer_buttons = []
active_question_data = None


def load_question_resources():
    """Ładuje zasoby potrzebne do wyświetlenia ekranu pytania."""
    global question_font, answer_font
    try:
        # Możesz użyć różnych czcionek dla pytania i odpowiedzi
        question_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.QUESTION_FONT_SIZE)
        answer_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.ANSWER_FONT_SIZE)
    except Exception as e:
        print(f"Błąd ładowania czcionek dla ekranu pytania: {e}")
        question_font = pygame.font.SysFont(None, settings.QUESTION_FONT_SIZE + 4)
        answer_font = pygame.font.SysFont(None, settings.ANSWER_FONT_SIZE + 4)


def setup_question_ui(question_data, screen_width, screen_height):
    """
    Przygotowuje UI na podstawie danych konkretnego pytania.
    Tworzy klikalne przyciski dla każdej odpowiedzi.
    """
    global answer_buttons, active_question_data
    active_question_data = question_data
    answer_buttons = []

    if not active_question_data:
        return

    # Ustawienia karty pytania
    card_width = screen_width * 0.7  # 70% szerokości ekranu
    card_height = screen_height * 0.6  # 60% wysokości ekranu
    card_rect = pygame.Rect(0, 0, card_width, card_height)
    card_rect.center = (screen_width // 2, screen_height // 2)

    # Ustawienia przycisków odpowiedzi
    btn_width = card_width * 0.8  # 80% szerokości karty
    btn_height = 60  # Stała wysokość
    btn_spacing = 15

    # Pozycjonowanie przycisków
    # Zaczniemy od dołu karty i będziemy szli w górę lub od środka w dół
    start_y = card_rect.centery + 50  # Rozpocznij rysowanie przycisków poniżej środka karty

    for i, answer_text in enumerate(question_data["answers"]):
        btn_x = card_rect.centerx - btn_width // 2
        btn_y = start_y + i * (btn_height + btn_spacing)

        answer_btn = Button(
            x=btn_x, y=btn_y,
            width=btn_width, height=btn_height,
            text=answer_text, font=answer_font,
            base_color=settings.ANSWER_BUTTON_BASE_COLOR,
            hover_color=settings.ANSWER_BUTTON_HOVER_COLOR,
            text_color=settings.ANSWER_BUTTON_TEXT_COLOR,
            action=i,  # Akcja przycisku to indeks odpowiedzi (0, 1, 2, 3)
            border_radius=10
        )
        answer_buttons.append(answer_btn)


def handle_question_input(event, mouse_pos):
    """Sprawdza kliknięcia na przyciskach odpowiedzi."""
    for btn in answer_buttons:
        # Zwróci indeks odpowiedzi (0-3) jeśli kliknięty, w przeciwnym razie None
        action = btn.handle_event(event, mouse_pos)
        if action is not None:
            print(f"Wybrano odpowiedź o indeksie: {action}")
            return action
    return None


def draw_question_screen(surface, mouse_pos):
    """Rysuje całą kartę pytania."""
    if not active_question_data:
        return

    # Tło karty - półprzezroczysta nakładka
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Półprzezroczysta czerń
    surface.blit(overlay, (0, 0))

    # Rysowanie tła karty pytania
    card_width = surface.get_width() * 0.7
    card_height = surface.get_height() * 0.6
    card_rect = pygame.Rect(0, 0, card_width, card_height)
    card_rect.center = surface.get_rect().center
    pygame.draw.rect(surface, settings.QUESTION_CARD_BG_COLOR, card_rect, border_radius=20)
    pygame.draw.rect(surface, settings.QUESTION_CARD_BORDER_COLOR, card_rect, 4, border_radius=20)

    # Rysowanie tekstu pytania (z łamaniem linii)
    # Używamy tej samej funkcji co w board_screen.py lub dedykowanej
    from board_screen import Board  # Tymczasowy import do użycia metody
    text_surface = Board._render_text_multiline(None, active_question_data["question_text"], question_font,
                                                settings.QUESTION_TEXT_COLOR,
                                                card_width - 80)  # Szerokość tekstu to szerokość karty minus padding
    if text_surface:
        text_rect = text_surface.get_rect(centerx=card_rect.centerx, top=card_rect.top + 40)
        surface.blit(text_surface, text_rect)

    # Rysowanie przycisków odpowiedzi
    for btn in answer_buttons:
        btn.update_hover(mouse_pos)
        btn.draw(surface)