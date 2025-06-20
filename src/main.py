# src/main.py
import pygame
import sys
import menu_screen
import gameplay_screen
import game_logic
import name_input_screen
from dice import Dice
import settings

pygame.init()

# --- Inicjalizacja Okna ---
screen = pygame.display.set_mode((settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT))
pygame.display.set_caption(settings.SCREEN_TITLE)
game_logic.set_main_screen(screen)  # Przekaż instancję ekranu do logiki gry

try:
    game_icon = pygame.image.load(settings.IMAGE_PATH_ICON)
    pygame.display.set_icon(game_icon)
except Exception as e:
    print(f"Błąd ładowania ikony: {e}")

# Inicjalizacja zasobów dla początkowych ekranów
menu_screen.load_menu_resources(settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT)
menu_screen.setup_menu_ui_elements(settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT)
name_input_screen.setup_name_input_screen(settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT)

# --- Instancja Kostki i Zegar ---
dice_instance = Dice(
    initial_x_center=settings.LEFT_PANEL_WIDTH // 2,
    initial_y_bottom_of_image=settings.GAMEPLAY_SCREEN_HEIGHT - 200,
)
clock = pygame.time.Clock()

# --- Główna Pętla Gry ---
running = True
while running:
    # Pobierz aktualne wartości z modułu logiki
    dt_seconds = clock.tick(settings.FPS) / 1000.0
    mouse_pos = pygame.mouse.get_pos()
    current_game_state = game_logic.game_state
    current_turn_phase = game_logic.turn_phase

    # Sprawdzenie, czy można obsługiwać input
    pawn_in_motion = next((p for p in game_logic.all_pawn_objects if p.is_moving or p.is_repositioning), None)
    can_handle_input = not dice_instance.is_animating and not pawn_in_motion and not (
            current_turn_phase in ['SHOWING_QUESTION', 'SHOWING_FEEDBACK', 'PAWN_MOVING'])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Zdarzenia dla karty pytania są obsługiwane zawsze, gdy jest widoczna
        if current_game_state == "GAMEPLAY" and current_turn_phase == 'SHOWING_QUESTION':
            if game_logic.active_question_card:
                chosen_answer_index = game_logic.active_question_card.handle_event(event, mouse_pos)
                if chosen_answer_index is not None:
                    game_logic.process_player_answer(chosen_answer_index)

        # Pozostałe zdarzenia obsługuj tylko, gdy nie ma blokady
        elif can_handle_input:
            if current_game_state == "MENU_GLOWNE":
                action = menu_screen.handle_menu_input(event, mouse_pos)
                if action:
                    if action == "GAMEPLAY":
                        game_logic.change_game_state("GETTING_PLAYER_NAMES")
                    elif action == "INSTRUCTIONS":
                        game_logic.change_game_state("INSTRUCTIONS")
                    elif action == "QUIT":
                        running = False
            elif current_game_state == "GETTING_PLAYER_NAMES":
                action = name_input_screen.handle_name_input_events(event, mouse_pos)
                if action == "START_GAME": game_logic.start_new_game(name_input_screen.player_names_input)
            elif current_game_state == "GAMEPLAY" and current_turn_phase == 'WAITING_FOR_ROLL':
                gameplay_action = gameplay_screen.handle_gameplay_input(event, mouse_pos)
                if gameplay_action == "ROLL_DICE_PANEL":
                    dice_instance.start_animation_and_roll()
                    game_logic.turn_phase = 'DICE_ROLLING'
                elif gameplay_action == "BACK_TO_MENU":
                    game_logic.change_game_state("MENU_GLOWNE")
            elif current_game_state == "INSTRUCTIONS":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    game_logic.change_game_state("MENU_GLOWNE")

    # --- Aktualizacja Logiki ---
    if current_game_state == "GAMEPLAY":
        game_logic.update_game_logic(dt_seconds, dice_instance)
        gameplay_screen.update_gameplay_state(game_logic.current_player_id)
        if game_logic.active_question_card:
            game_logic.active_question_card.update_hover(mouse_pos)

    # --- Rysowanie ---
    screen.fill(settings.DEFAULT_BG_COLOR)

    if current_game_state == "MENU_GLOWNE":
        menu_screen.draw_menu_screen(screen, game_logic.current_screen_width, game_logic.current_screen_height,
                                     mouse_pos)
    elif current_game_state == "GETTING_PLAYER_NAMES":
        name_input_screen.draw_name_input_screen(screen, game_logic.current_screen_width,
                                                 game_logic.current_screen_height, mouse_pos)
    elif current_game_state == "GAMEPLAY":
        gameplay_screen.draw_gameplay_screen(screen, mouse_pos, dice_instance)
        for pawn in game_logic.all_pawn_objects:
            pawn.draw(screen)

        if game_logic.active_question_card and game_logic.active_question_card.is_visible:
            game_logic.active_question_card.draw(screen)
        elif game_logic.active_feedback_card and game_logic.active_feedback_card.is_visible:
            game_logic.active_feedback_card.draw(screen)

    elif current_game_state == "INSTRUCTIONS":
        screen.fill(settings.MENU_BG_FALLBACK_COLOR)
        if menu_screen.TITLE_FONT_MENU and menu_screen.BUTTON_FONT_MENU:
            title_instr = menu_screen.TITLE_FONT_MENU.render("Instrukcja", True, settings.MENU_TEXT_COLOR)
            title_instr_rect = title_instr.get_rect(
                center=(game_logic.current_screen_width // 2, game_logic.current_screen_height // 4))
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
                line_rect = line_surface.get_rect(center=(game_logic.current_screen_width // 2, line_y_offset + i * 45))
                screen.blit(line_surface, line_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()