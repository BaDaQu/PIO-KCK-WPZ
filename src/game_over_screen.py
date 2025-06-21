# src/game_over_screen.py
import pygame
import settings
from button import Button
import menu_screen  # Potrzebne do czcionki przycisku

# Zmienne modułu
title_font = None
subtitle_font = None
back_to_menu_button = None
title_text = ""
winner_name_text = ""
reason_text = ""


def setup_game_over_screen(screen_width, screen_height, winner_name, reason_for_game_over):
    """Konfiguruje UI dla ekranu końca gry na podstawie wyniku."""
    global title_font, subtitle_font, back_to_menu_button, title_text, winner_name_text, reason_text

    # Ustaw teksty na podstawie wyniku
    title_text = settings.GAME_OVER_WIN_TEXT if winner_name else settings.GAME_OVER_LOSE_TEXT
    winner_name_text = f"Gratulacje, {winner_name}!" if winner_name else ""
    reason_text = reason_for_game_over

    # Załaduj czcionki
    try:
        title_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.GAME_OVER_TITLE_FONT_SIZE)
        subtitle_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.GAME_OVER_SUBTITLE_FONT_SIZE)
    except Exception as e:
        print(f"Błąd ładowania czcionek dla ekranu końca gry: {e}")
        title_font = pygame.font.SysFont(None, settings.GAME_OVER_TITLE_FONT_SIZE)
        subtitle_font = pygame.font.SysFont(None, settings.GAME_OVER_SUBTITLE_FONT_SIZE)

    # Skonfiguruj przycisk
    back_to_menu_button = Button(
        x=(screen_width - settings.MENU_BUTTON_WIDTH) // 2,
        y=int(screen_height * 0.7),
        width=settings.MENU_BUTTON_WIDTH,
        height=settings.MENU_BUTTON_HEIGHT,
        text="Powrót do Menu",
        font=menu_screen.BUTTON_FONT_MENU,  # Użyjemy załadowanej czcionki z menu
        base_color=settings.MENU_BUTTON_BASE_COLOR,
        hover_color=settings.MENU_BUTTON_HOVER_COLOR,
        text_color=settings.MENU_TEXT_COLOR,
        action="BACK_TO_MENU",
        border_radius=15
    )


def handle_game_over_input(event, mouse_pos):
    """Obsługuje input dla ekranu końca gry."""
    if back_to_menu_button:
        action = back_to_menu_button.handle_event(event, mouse_pos)
        if action: return action
    return None


def draw_game_over_screen(surface, mouse_pos):
    """Rysuje ekran końca gry."""
    # Rysuj półprzezroczyste tło, które przyciemnia ekran gry pod spodem
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill(settings.GAME_OVER_BG_COLOR)
    surface.blit(overlay, (0, 0))

    # Renderuj i rysuj tytuł (ZWYCIĘSTWO! / PORAŻKA...)
    if title_font:
        title_surface = title_font.render(title_text, True, settings.GAME_OVER_TEXT_COLOR)
        title_rect = title_surface.get_rect(centerx=surface.get_rect().centerx,
                                            centery=surface.get_rect().centery - 150)
        surface.blit(title_surface, title_rect)

    # Renderuj i rysuj podtytuły (imię zwycięzcy i powód)
    if subtitle_font:
        # Imię zwycięzcy
        if winner_name_text:
            winner_surface = subtitle_font.render(winner_name_text, True, settings.WHITE)
            winner_rect = winner_surface.get_rect(centerx=title_rect.centerx, top=title_rect.bottom + 10)
            surface.blit(winner_surface, winner_rect)

        # Powód zakończenia gry
        if reason_text:
            reason_surface = subtitle_font.render(reason_text, True, settings.WHITE)
            # Pozycja zależy od tego, czy jest imię zwycięzcy
            top_position = winner_rect.bottom + 5 if winner_name_text else title_rect.bottom + 10
            reason_rect = reason_surface.get_rect(centerx=title_rect.centerx, top=top_position)
            surface.blit(reason_surface, reason_rect)

    # Rysuj przycisk powrotu
    if back_to_menu_button:
        back_to_menu_button.update_hover(mouse_pos)
        back_to_menu_button.draw(surface)