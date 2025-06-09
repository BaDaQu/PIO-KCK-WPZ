# src/menu_screen.py
import pygame
from button import Button # Zaimportuj klasę Button

# --- Stałe (mogą być też w głównym pliku lub settings.py) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (240, 190, 100)
BUTTON_HOVER_COLOR = (255, 210, 120)
TEXT_COLOR = (80, 50, 20)

menu_background_img = None
TITLE_FONT = None
BUTTON_FONT = None
menu_buttons_list = [] # Zmieniono nazwę na listę obiektów Button

# --- Funkcje Inicjalizacyjne Menu ---
def load_menu_resources(screen_width, screen_height, title_font_path, button_font_path, background_image_path):
    global menu_background_img, TITLE_FONT, BUTTON_FONT
    try:
        TITLE_FONT = pygame.font.Font(title_font_path, 90)
        BUTTON_FONT = pygame.font.Font(button_font_path, 40)
    except pygame.error as e:
        print(f"Błąd ładowania czcionki dla menu: {e}")
        TITLE_FONT = pygame.font.SysFont(None, 100)
        BUTTON_FONT = pygame.font.SysFont(None, 50)

    try:
        menu_background_img = pygame.image.load(background_image_path).convert()
        menu_background_img = pygame.transform.scale(menu_background_img, (screen_width, screen_height))
    except pygame.error as e:
        print(f"Błąd ładowania obrazka tła menu: {e}")
        menu_background_img = None

def setup_menu_ui_elements(screen_width, screen_height):
    global menu_buttons_list
    menu_buttons_list = [] # Czyścimy listę

    button_width = 470
    button_height = 115
    button_spacing = 25

    # Pozycje X i Y dla pierwszego przycisku
    start_x = (screen_width - button_width) - 140
    start_y = screen_height - 280 - button_height - button_spacing

    # Tworzenie obiektów Button
    new_game_btn = Button(
        x=start_x, y=start_y,
        width=button_width, height=button_height,
        text="NOWA GRA", font=BUTTON_FONT,
        base_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, text_color=TEXT_COLOR,
        action="GAMEPLAY"
    )
    menu_buttons_list.append(new_game_btn)

    instructions_btn = Button(
        x=start_x, y=new_game_btn.rect.bottom + button_spacing,
        width=button_width, height=button_height,
        text="INSTRUKCJA", font=BUTTON_FONT,
        base_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, text_color=TEXT_COLOR,
        action="INSTRUCTIONS"
    )
    menu_buttons_list.append(instructions_btn)

    exit_btn = Button(
        x=start_x, y=instructions_btn.rect.bottom + button_spacing,
        width=button_width, height=button_height,
        text="WYJDŹ", font=BUTTON_FONT,
        base_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, text_color=TEXT_COLOR,
        action="QUIT"
    )
    menu_buttons_list.append(exit_btn)


# --- Funkcja Obsługi Zdarzeń Menu ---
def handle_menu_input(event, mouse_pos):
    for btn in menu_buttons_list:
        action = btn.handle_event(event, mouse_pos)
        if action:
            return action
    return None


# --- Funkcja Rysowania Menu ---
def draw_menu_screen(surface, screen_width, screen_height, mouse_pos):
    if menu_background_img:
        if menu_background_img.get_size() != (screen_width, screen_height):
             current_bg = pygame.transform.scale(menu_background_img, (screen_width, screen_height))
             surface.blit(current_bg, (0,0))
        else:
            surface.blit(menu_background_img, (0, 0))
    else:
        surface.fill((200, 180, 160))



    for btn in menu_buttons_list:
        btn.update_hover(mouse_pos) # Aktualizuj stan hover przed rysowaniem
        btn.draw(surface)