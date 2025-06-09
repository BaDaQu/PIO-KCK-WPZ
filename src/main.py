# src/main.py
import pygame
import sys
# Nie potrzebujemy już bezpośrednio Board tutaj, bo gameplay_screen się tym zajmie
import menu_screen
import gameplay_screen  # NOWY IMPORT
from button import Button  # Zakładamy, że button.py istnieje

pygame.init()

INITIAL_SCREEN_WIDTH = 1436
INITIAL_SCREEN_HEIGHT = 1024
SCREEN_TITLE = "Wyścig po Zaliczenie"
GAMEPLAY_SCREEN_WIDTH = 1436  # Pełna szerokość dla stanu gameplay
GAMEPLAY_SCREEN_HEIGHT = 1024

current_screen_width = INITIAL_SCREEN_WIDTH
current_screen_height = INITIAL_SCREEN_HEIGHT

pygame.display.set_caption(SCREEN_TITLE)
screen = pygame.display.set_mode((current_screen_width, current_screen_height))

FONT_PATH = "../assets/fonts/PTSerif-Regular.ttf"
MENU_BG_PATH = "../assets/images/MENU_GLOWNE.png"
ICON_PATH = "../assets/images/IKONA_GRY.png"
LEFT_PANEL_BG_PATH = "../assets/images/GAMEBOARD_LEFT_PANEL.png"  # Używane w gameplay_screen

try:
    game_icon = pygame.image.load(ICON_PATH)
    pygame.display.set_icon(game_icon)
except Exception as e:
    print(f"Błąd ładowania ikony: {e}")

# Inicjalizacja zasobów dla menu
menu_screen.load_menu_resources(current_screen_width, current_screen_height, FONT_PATH, FONT_PATH, MENU_BG_PATH)
menu_screen.setup_menu_ui_elements(current_screen_width, current_screen_height)

clock = pygame.time.Clock()
FPS = 60
game_state = "MENU_GLOWNE"


def set_screen_mode(width, height):
    global screen, current_screen_width, current_screen_height
    current_screen_width = width
    current_screen_height = height
    screen = pygame.display.set_mode((current_screen_width, current_screen_height))

    if game_state == "MENU_GLOWNE":
        menu_screen.load_menu_resources(current_screen_width, current_screen_height, FONT_PATH, FONT_PATH, MENU_BG_PATH)
        menu_screen.setup_menu_ui_elements(current_screen_width, current_screen_height)
    elif game_state == "GAMEPLAY":
        gameplay_screen.load_gameplay_resources(current_screen_width, current_screen_height, FONT_PATH,
                                                LEFT_PANEL_BG_PATH)
        gameplay_screen.setup_gameplay_ui_elements(
            current_screen_height)  # Przekazujemy wysokość dla pozycjonowania przycisków
    elif game_state == "INSTRUCTIONS":
        menu_screen.load_menu_resources(current_screen_width, current_screen_height, FONT_PATH, FONT_PATH, MENU_BG_PATH)
        # TODO: Dedykowana funkcja setup dla instrukcji w menu_screen lub nowym module


running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "MENU_GLOWNE":
            action = menu_screen.handle_menu_input(event, mouse_pos)
            if action:
                if action == "GAMEPLAY":
                    game_state = "GAMEPLAY"
                    if current_screen_width != GAMEPLAY_SCREEN_WIDTH or current_screen_height != GAMEPLAY_SCREEN_HEIGHT:
                        set_screen_mode(GAMEPLAY_SCREEN_WIDTH, GAMEPLAY_SCREEN_HEIGHT)
                    else:  # Tylko załaduj zasoby, jeśli rozmiar jest już poprawny
                        gameplay_screen.load_gameplay_resources(current_screen_width, current_screen_height, FONT_PATH,
                                                                LEFT_PANEL_BG_PATH)
                        gameplay_screen.setup_gameplay_ui_elements(current_screen_height)
                elif action == "INSTRUCTIONS":
                    game_state = "INSTRUCTIONS"
                    if current_screen_width != INITIAL_SCREEN_WIDTH or current_screen_height != INITIAL_SCREEN_HEIGHT:
                        set_screen_mode(INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT)
                elif action == "QUIT":
                    running = False

        elif game_state == "GAMEPLAY":
            action_gp = gameplay_screen.handle_gameplay_input(event, mouse_pos)
            if action_gp == "BACK_TO_MENU":
                game_state = "MENU_GLOWNE"
                if current_screen_width != INITIAL_SCREEN_WIDTH or current_screen_height != INITIAL_SCREEN_HEIGHT:
                    set_screen_mode(INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT)
            # TODO: Pozostała obsługa zdarzeń dla rozgrywki

        elif game_state == "INSTRUCTIONS":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game_state = "MENU_GLOWNE"
                    if current_screen_width != INITIAL_SCREEN_WIDTH or current_screen_height != INITIAL_SCREEN_HEIGHT:
                        set_screen_mode(INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT)

    # Aktualizacja logiki per stan
    if game_state == "GAMEPLAY":
        gameplay_screen.update_gameplay_state()
    # TODO: Inne stany update_...()

    # Rysowanie
    screen.fill(menu_screen.BLACK)  # Domyślne tło, jeśli nic innego nie jest rysowane

    if game_state == "MENU_GLOWNE":
        menu_screen.draw_menu_screen(screen, current_screen_width, current_screen_height, mouse_pos)
    elif game_state == "GAMEPLAY":
        gameplay_screen.draw_gameplay_screen(screen, mouse_pos)
    elif game_state == "INSTRUCTIONS":
        # Prosty ekran instrukcji (może być przeniesiony do menu_screen lub własnego modułu)
        # screen.fill((50, 50, 150)) # Tło dla instrukcji (obsługiwane w menu_screen lub nowym module)
        if hasattr(menu_screen, 'TITLE_FONT') and menu_screen.TITLE_FONT:
            title_instr = menu_screen.TITLE_FONT.render("Instrukcja", True,
                                                        menu_screen.WHITE)  # Użyj kolorów z menu_screen
            title_instr_rect = title_instr.get_rect(center=(current_screen_width // 2, current_screen_height // 4))
            screen.blit(title_instr, title_instr_rect)

        if hasattr(menu_screen, 'BUTTON_FONT') and menu_screen.BUTTON_FONT:
            info_text_lines = [
                "Witaj w Wyścigu po Zaliczenie!", "Rzuć kostką, aby się poruszyć.",
                "Odpowiadaj na pytania na polach przedmiotowych.", "Uważaj na Profesora i pola 'Poprawka'!",
                "Zbieraj 'Stypendia Naukowe'!", "Celem jest dotarcie do mety jako pierwszy.",
                "", "(Kliknij, aby wrócić do menu)"
            ]
            line_y_offset = title_instr_rect.bottom + 30
            for i, line in enumerate(info_text_lines):
                line_surface = menu_screen.BUTTON_FONT.render(line, True, menu_screen.WHITE)
                line_rect = line_surface.get_rect(center=(current_screen_width // 2, line_y_offset + i * 45))
                screen.blit(line_surface, line_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()