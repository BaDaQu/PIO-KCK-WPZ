# src/main.py
import pygame
import sys
import menu_screen
import gameplay_screen
import game_logic  # <-- NOWY IMPORT
from dice import Dice
import settings

pygame.init()

# --- Inicjalizacja Okna ---
current_screen_width = settings.INITIAL_SCREEN_WIDTH
current_screen_height = settings.INITIAL_SCREEN_HEIGHT
pygame.display.set_caption(settings.SCREEN_TITLE)
screen = pygame.display.set_mode((current_screen_width, current_screen_height))

try:
    game_icon = pygame.image.load(settings.IMAGE_PATH_ICON)
    pygame.display.set_icon(game_icon)
except Exception as e:
    print(f"Błąd ładowania ikony: {e}")

# Inicjalizacja zasobów dla menu
menu_screen.load_menu_resources(current_screen_width, current_screen_height)
menu_screen.setup_menu_ui_elements(current_screen_width, current_screen_height)

# --- Instancje Obiektów Głównych ---
dice_instance = Dice(
    initial_x_center=settings.LEFT_PANEL_WIDTH // 2,
    initial_y_bottom_of_image=settings.GAMEPLAY_SCREEN_HEIGHT - 200,
    dice_images_base_path=settings.DICE_IMAGES_BASE_PATH
)
clock = pygame.time.Clock()
game_state = "MENU_GLOWNE"


# -----------------------------------

def set_screen_mode(width, height):
    """Zmienia tryb ekranu i deleguje inicjalizację zasobów."""
    global screen, current_screen_width, current_screen_height
    current_screen_width = width;
    current_screen_height = height
    screen = pygame.display.set_mode((current_screen_width, current_screen_height))
    print(f"Tryb ekranu zmieniony na: {width}x{height}")

    if game_state == "MENU_GLOWNE":
        menu_screen.load_menu_resources(current_screen_width, current_screen_height)
        menu_screen.setup_menu_ui_elements(current_screen_width, current_screen_height)
    elif game_state == "GAMEPLAY":
        game_logic.initialize_game_logic_and_pawns()
    elif game_state == "INSTRUCTIONS":
        menu_screen.load_menu_resources(current_screen_width, current_screen_height)


def initialize_gameplay():
    """Funkcja, która przygotowuje wszystko do rozpoczęcia nowej gry."""
    print("Rozpoczynam inicjalizację rozgrywki...")
    gameplay_screen.load_gameplay_resources(current_screen_width, current_screen_height)
    gameplay_screen.setup_gameplay_ui_elements(current_screen_height)
    game_logic.initialize_game_logic_and_pawns()


running = True
while running:
    dt_seconds = clock.tick(settings.FPS) / 1000.0
    mouse_pos = pygame.mouse.get_pos()

    pawn_in_motion = next((p for p in game_logic.all_pawn_objects if p.is_moving or p.is_repositioning), None)
    can_handle_input = not dice_instance.is_animating and not pawn_in_motion

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

        if can_handle_input:
            if game_state == "MENU_GLOWNE":
                action = menu_screen.handle_menu_input(event, mouse_pos)
                if action:
                    if action == "GAMEPLAY":
                        game_state = "GAMEPLAY"
                        if current_screen_width != settings.GAMEPLAY_SCREEN_WIDTH or current_screen_height != settings.GAMEPLAY_SCREEN_HEIGHT:
                            set_screen_mode(settings.GAMEPLAY_SCREEN_WIDTH, settings.GAMEPLAY_SCREEN_HEIGHT)
                        else:
                            initialize_gameplay()  # Inicjalizuj grę bez zmiany ekranu
                    elif action == "INSTRUCTIONS":
                        game_state = "INSTRUCTIONS"
                        if current_screen_width != settings.INITIAL_SCREEN_WIDTH or current_screen_height != settings.INITIAL_SCREEN_HEIGHT:
                            set_screen_mode(settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT)
                    elif action == "QUIT":
                        running = False

            elif game_state == "GAMEPLAY":
                if game_logic.turn_phase == 'WAITING_FOR_ROLL':
                    gameplay_action = gameplay_screen.handle_gameplay_input(event, mouse_pos)
                    if gameplay_action == "ROLL_DICE_PANEL":
                        dice_instance.start_animation_and_roll()
                        game_logic.turn_phase = 'DICE_ROLLING'
                    elif gameplay_action == "BACK_TO_MENU":
                        game_state = "MENU_GLOWNE"
                        if current_screen_width != settings.INITIAL_SCREEN_WIDTH or current_screen_height != settings.INITIAL_SCREEN_HEIGHT:
                            set_screen_mode(settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT)

            elif game_state == "INSTRUCTIONS":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    game_state = "MENU_GLOWNE"
                    if current_screen_width != settings.INITIAL_SCREEN_WIDTH or current_screen_height != settings.INITIAL_SCREEN_HEIGHT:
                        set_screen_mode(settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT)

    # --- Aktualizacja Logiki ---
    if game_state == "GAMEPLAY":
        game_logic.update_game_logic(dt_seconds, dice_instance)

    # --- Rysowanie ---
    screen.fill(settings.DEFAULT_BG_COLOR)
    if game_state == "MENU_GLOWNE":
        menu_screen.draw_menu_screen(screen, current_screen_width, current_screen_height, mouse_pos)
    elif game_state == "GAMEPLAY":
        gameplay_screen.draw_gameplay_screen(screen, mouse_pos, dice_instance)
        game_logic.all_sprites_group.draw(screen)
    elif game_state == "INSTRUCTIONS":
        if menu_screen.TITLE_FONT_MENU and menu_screen.BUTTON_FONT_MENU:
            screen.fill(settings.MENU_BG_FALLBACK_COLOR)
            title_instr = menu_screen.TITLE_FONT_MENU.render("Instrukcja", True, settings.MENU_TEXT_COLOR)
            title_instr_rect = title_instr.get_rect(center=(current_screen_width // 2, current_screen_height // 4))
            screen.blit(title_instr, title_instr_rect)
            info_text_lines = [
                "Witaj w Wyścigu po Zaliczenie!", "Rzuć kostką, aby się poruszyć.",
                "Odpowiadaj na pytania na polach przedmiotowych.", "Uważaj na Profesora i pola 'Poprawka'!",
                "Zbieraj 'Stypendia Naukowe'!", "Celem jest dotarcie do mety jako pierwszy.",
                "", "(Kliknij, aby wrócić do menu)"
            ]
            line_y_offset = title_instr_rect.bottom + 30
            for i, line in enumerate(info_text_lines):
                line_surface = menu_screen.BUTTON_FONT_MENU.render(line, True, settings.MENU_TEXT_COLOR)
                line_rect = line_surface.get_rect(center=(current_screen_width // 2, line_y_offset + i * 45))
                screen.blit(line_surface, line_rect)
        else:
            fallback_font = pygame.font.SysFont(None, 30)
            info_text = fallback_font.render("(Kliknij, aby wrócić)", True, settings.WHITE)
            screen.blit(info_text, (50, 50))

    pygame.display.flip()

pygame.quit()
sys.exit()