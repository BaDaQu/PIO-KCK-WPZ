# src/game_over_screen.py
import pygame
import math
import settings
from button import Button
import menu_screen  # Potrzebne do czcionki przycisku
import text_utility  # Ważny import dla tekstu z obrysem

# Zmienne modułu
background_image = None
pawn1_image = None
pawn2_image = None
crown_image = None
back_to_menu_button = None
winner_player_index = -1
title_text = ""
reason_text = ""
animation_timer = 0.0


def setup_game_over_screen(screen_width, screen_height, winner_data):
    """Konfiguruje UI dla ekranu końca gry, używając spersonalizowanych komunikatów."""
    global background_image, pawn1_image, pawn2_image, crown_image, back_to_menu_button
    global winner_player_index, reason_text, title_text, animation_timer

    winner_player_index = -1
    animation_timer = 0.0

    # Pobieramy pełne dane o zwycięzcy
    winner_id = winner_data.get("id")
    winner_name = winner_data.get("name")  # Imię gracza
    reason_text = winner_data.get("reason", "Gra zakończona")

    if winner_id == "player_1":
        winner_player_index = 0
    elif winner_id == "player_2":
        winner_player_index = 1

    # Ustawiamy dynamiczny tytuł na podstawie imienia zwycięzcy
    if winner_name:
        title_text = f"{winner_name.upper()} WYGRYWA!"
    else:  # Fallback, np. przy błędzie
        title_text = "KONIEC GRY"

    try:
        # Ładowanie zasobów
        bg_img_raw = pygame.image.load(settings.IMAGE_PATH_GAME_OVER_BG).convert()
        background_image = pygame.transform.scale(bg_img_raw, (screen_width, screen_height))

        pawn1_raw = pygame.image.load(settings.IMAGE_PATH_PLAYER1_PAWN).convert_alpha()
        pawn2_raw = pygame.image.load(settings.IMAGE_PATH_PLAYER2_PAWN).convert_alpha()
        crown_raw = pygame.image.load(settings.IMAGE_PATH_WINNER_CROWN).convert_alpha()

        # Skalowanie obrazków na podstawie stałych z settings.py
        scale_pawn = settings.GAMEOVER_PAWN_SCALE_FACTOR
        pawn1_size = (int(pawn1_raw.get_width() * scale_pawn), int(pawn1_raw.get_height() * scale_pawn))
        pawn2_size = (int(pawn2_raw.get_width() * scale_pawn), int(pawn2_raw.get_height() * scale_pawn))

        scale_crown = settings.GAMEOVER_CROWN_SCALE_FACTOR
        crown_size = (int(crown_raw.get_width() * scale_crown), int(crown_raw.get_height() * scale_crown))

        pawn1_image = pygame.transform.smoothscale(pawn1_raw, pawn1_size)
        pawn2_image = pygame.transform.smoothscale(pawn2_raw, pawn2_size)
        crown_image = pygame.transform.smoothscale(crown_raw, crown_size)

    except Exception as e:
        print(f"Błąd ładowania obrazków dla ekranu końca gry: {e}")

    # Nie ładujemy już czcionek tutaj, bo `text_utility` zrobi to za nas

    # Konfiguracja przycisku
    if menu_screen.BUTTON_FONT_MENU:  # Upewnij się, że czcionka z menu jest załadowana
        back_to_menu_button = Button(
            x=(screen_width - settings.MENU_BUTTON_WIDTH) // 2,
            y=screen_height // 2 + settings.GAMEOVER_BUTTON_Y_OFFSET,
            width=settings.MENU_BUTTON_WIDTH, height=settings.MENU_BUTTON_HEIGHT,
            text="Powrót do Menu", font=menu_screen.BUTTON_FONT_MENU,
            base_color=settings.MENU_BUTTON_BASE_COLOR, hover_color=settings.MENU_BUTTON_HOVER_COLOR,
            text_color=settings.MENU_TEXT_COLOR, action="BACK_TO_MENU", border_radius=15
        )


def handle_game_over_input(event, mouse_pos):
    """Obsługuje input dla ekranu końca gry, w tym Enter/Escape."""
    if back_to_menu_button:
        action = back_to_menu_button.handle_event(event, mouse_pos)
        if action:
            # sound_manager.play_sound('button_click') # Dźwięk kliknięcia jest w main.py
            return action
    if event.type == pygame.KEYDOWN and (
            event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE or event.key == pygame.K_KP_ENTER):
        # sound_manager.play_sound('button_click') # Dźwięk kliknięcia jest w main.py
        return "BACK_TO_MENU"
    return None


def update_game_over_screen(dt_seconds):
    """Aktualizuje animacje na ekranie końca gry."""
    global animation_timer
    animation_timer = (animation_timer + dt_seconds) % settings.CROWN_ANIM_DURATION_SECONDS


def draw_game_over_screen(surface, mouse_pos):
    """Rysuje ekran końca gry z dynamicznym skalowaniem tekstu i obrysem."""
    if background_image:
        surface.blit(background_image, (0, 0))
    else:
        surface.fill((40, 30, 20))  # Kolor fallback, jeśli tło się nie załaduje

    screen_center_x = surface.get_rect().centerx
    screen_center_y = surface.get_rect().centery

    pawn_y_center = screen_center_y + settings.GAMEOVER_PAWN_Y_OFFSET

    pawn1_rect, pawn2_rect = None, None  # Inicjalizacja, aby uniknąć błędu, jeśli obrazki się nie załadują
    if pawn1_image:
        pawn1_rect = pawn1_image.get_rect(center=(screen_center_x - settings.GAMEOVER_PAWN_SPACING // 2, pawn_y_center))
        surface.blit(pawn1_image, pawn1_rect)
    if pawn2_image:
        pawn2_rect = pawn2_image.get_rect(center=(screen_center_x + settings.GAMEOVER_PAWN_SPACING // 2, pawn_y_center))
        surface.blit(pawn2_image, pawn2_rect)

    if crown_image and winner_player_index != -1 and pawn1_rect and pawn2_rect:
        winner_pawn_rect = pawn1_rect if winner_player_index == 0 else pawn2_rect
        crown_x = winner_pawn_rect.centerx
        progress = (animation_timer / settings.CROWN_ANIM_DURATION_SECONDS) * 2 * math.pi
        crown_y_anim_offset = math.sin(progress) * settings.CROWN_ANIM_AMPLITUDE
        crown_y = winner_pawn_rect.top + settings.CROWN_Y_OFFSET_FROM_PAWN + crown_y_anim_offset
        crown_rect = crown_image.get_rect(center=(crown_x, crown_y))
        surface.blit(crown_image, crown_rect)

    # Definiujemy prostokąt, w którym ma się zmieścić tytuł
    title_area_rect = pygame.Rect(
        0, 0,
        surface.get_width() - 100,  # Margines 50px z każdej strony
        200  # Maksymalna wysokość dla tytułu
    )
    title_area_rect.centerx = screen_center_x
    title_area_rect.centery = screen_center_y + settings.GAMEOVER_TITLE_Y_OFFSET

    # Renderujemy tytuł z obrysem i dynamicznym dopasowaniem
    text_utility.render_text(
        surface=surface, text=title_text,
        font_path=settings.FONT_PATH_PT_SERIF_REGULAR,
        initial_font_size=settings.GAME_OVER_TITLE_FONT_SIZE,
        color=settings.GAME_OVER_TEXT_COLOR,
        rect=title_area_rect,
        outline_color=settings.INSTRUCTIONS_OUTLINE_COLOR,
        outline_width=settings.INSTRUCTIONS_OUTLINE_WIDTH + 1,  # Grubszy obrys dla tytułu
        padding=10
    )

    # Definiujemy prostokąt, w którym ma się zmieścić powód
    reason_area_rect = pygame.Rect(0, 0, surface.get_width() - 200, 100)
    reason_area_rect.centerx = screen_center_x
    reason_area_rect.centery = screen_center_y + settings.GAMEOVER_REASON_Y_OFFSET

    # Renderujemy powód z obrysem i dynamicznym dopasowaniem
    text_utility.render_text(
        surface=surface, text=reason_text,
        font_path=settings.FONT_PATH_PT_SERIF_REGULAR,
        initial_font_size=settings.GAME_OVER_REASON_FONT_SIZE,
        color=settings.WHITE,
        rect=reason_area_rect,
        outline_color=settings.INSTRUCTIONS_OUTLINE_COLOR,
        outline_width=settings.INSTRUCTIONS_OUTLINE_WIDTH,
        padding=5
    )

    if back_to_menu_button:
        back_to_menu_button.update_hover(mouse_pos)
        back_to_menu_button.draw(surface)