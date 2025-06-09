# src/gameplay_screen.py
import pygame
from board_screen import Board
from button import Button # Zakładamy, że klasa Button jest w button.py

# Stałe dla tego modułu (można je też przenieść do globalnego pliku settings.py)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LEFT_PANEL_FALLBACK_COLOR = (40, 40, 40)
BOARD_FALLBACK_COLOR = (30, 30, 30)

# Kolory przycisków i tekstów (można zaimportować z menu_screen lub settings)
# Dla uproszczenia, zdefiniujemy je tutaj, ale lepiej mieć je w jednym miejscu
BUTTON_BASE_COLOR = (218, 112, 32) # Twój pomarańczowy
BUTTON_HOVER_COLOR = (238, 132, 52)
BUTTON_TEXT_COLOR = (255, 255, 255) # Biały tekst na pomarańczowym

game_board_instance = None
left_panel_background_img = None
gameplay_buttons_list = []
BUTTON_FONT_GAMEPLAY = None # Czcionka dla przycisków w gameplay

# Wymiary panelu i planszy wewnątrz ekranu rozgrywki
LEFT_PANEL_WIDTH = 412
BOARD_RENDER_WIDTH = 1024 # Plansza renderowana jako 1024x1024

def load_gameplay_resources(screen_width, screen_height, font_path, left_panel_img_path):
    global game_board_instance, left_panel_background_img, BUTTON_FONT_GAMEPLAY

    # Inicjalizuj/Przeładuj planszę
    # Klasa Board sama zajmie się pozycjonowaniem planszy 1024x1024 na ekranie o podanej szerokości
    if game_board_instance is None or \
       game_board_instance.display_surface_width != screen_width or \
       game_board_instance.display_surface_height != screen_height:
        game_board_instance = Board(screen_width, screen_height) # Przekazujemy pełne wymiary ekranu rozgrywki

    # Załaduj tło lewego panelu
    try:
        if left_panel_img_path:
            left_panel_background_img = pygame.image.load(left_panel_img_path).convert()
            # Oczekujemy, że obrazek panelu ma już poprawne wymiary (412 x wysokość ekranu)
            # Jeśli nie, można dodać skalowanie, ale lepiej przygotować zasób.
            if left_panel_background_img.get_width() != LEFT_PANEL_WIDTH or \
               left_panel_background_img.get_height() != screen_height:
                print(f"OSTRZEŻENIE: Lewy panel ma wymiary {left_panel_background_img.get_size()}, oczekiwano {LEFT_PANEL_WIDTH}x{screen_height}. Skalowanie...")
                left_panel_background_img = pygame.transform.scale(left_panel_background_img, (LEFT_PANEL_WIDTH, screen_height))
        print("Lewy panel załadowany.")
    except Exception as e:
        print(f"Błąd ładowania obrazka lewego panelu: {e}")
        left_panel_background_img = None

    # Załaduj czcionkę dla przycisków gameplay (jeśli inna niż w menu)
    try:
        BUTTON_FONT_GAMEPLAY = pygame.font.Font(font_path, 30) # Mniejsza czcionka dla przycisku na panelu
    except Exception as e:
        print(f"Błąd ładowania czcionki dla gameplay: {e}")
        BUTTON_FONT_GAMEPLAY = pygame.font.SysFont(None, 35)


def setup_gameplay_ui_elements(screen_height): # screen_width lewego panelu jest stały (412)
    global gameplay_buttons_list

    gameplay_buttons_list = [] # Czyścimy listę

    btn_width = 300
    btn_height = 70
    # Wycentrowany na lewym panelu (szerokość panelu LEFT_PANEL_WIDTH)
    btn_x = (LEFT_PANEL_WIDTH - btn_width) // 2
    btn_y = screen_height - btn_height - 50 # Na dole panelu z marginesem

    quit_game_btn = Button(
        x=btn_x, y=btn_y,
        width=btn_width, height=btn_height,
        text="Zakończ Grę", font=BUTTON_FONT_GAMEPLAY,
        base_color=BUTTON_BASE_COLOR, hover_color=BUTTON_HOVER_COLOR, text_color=BUTTON_TEXT_COLOR,
        action="BACK_TO_MENU"
    )
    gameplay_buttons_list.append(quit_game_btn)
    # TODO: Dodaj inne przyciski dla ekranu rozgrywki (np. "Rzuć Kostką")


def handle_gameplay_input(event, mouse_pos):
    for btn in gameplay_buttons_list:
        action = btn.handle_event(event, mouse_pos)
        if action:
            return action
    # TODO: Obsługa innych zdarzeń specyficznych dla rozgrywki (np. kliknięcie na pole)
    return None


def update_gameplay_state():
    # TODO: Logika aktualizacji stanu gry (ruch pionków, AI profesora, sprawdzanie warunków itp.)
    pass


def draw_gameplay_screen(surface, mouse_pos):
    # Rysowanie lewego panelu
    if left_panel_background_img:
        surface.blit(left_panel_background_img, (0, 0))
    else:
        pygame.draw.rect(surface, LEFT_PANEL_FALLBACK_COLOR, (0, 0, LEFT_PANEL_WIDTH, surface.get_height()))

    # Rysowanie planszy (klasa Board sama zarządza swoim offsetem)
    if game_board_instance:
        game_board_instance.draw(surface)
    else:
        # Awaryjne rysowanie, jeśli plansza nie istnieje
        board_placeholder_x = surface.get_width() - BOARD_RENDER_WIDTH
        board_placeholder_y = (surface.get_height() - BOARD_RENDER_WIDTH) // 2 # BOARD_RENDER_WIDTH bo kwadrat
        pygame.draw.rect(surface, BOARD_FALLBACK_COLOR, (board_placeholder_x, board_placeholder_y, BOARD_RENDER_WIDTH, BOARD_RENDER_WIDTH))

    # Rysowanie przycisków na ekranie rozgrywki
    for btn in gameplay_buttons_list:
        btn.update_hover(mouse_pos)
        btn.draw(surface)

    # TODO: Rysowanie pionków, kostki, HUD z informacjami o graczach, aktualnego pytania itp.
