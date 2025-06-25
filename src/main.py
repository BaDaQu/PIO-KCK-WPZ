# src/main.py
import pygame
import sys
import menu_screen
import gameplay_screen
import game_logic
import name_input_screen
import instructions_screen
import game_over_screen
import settings_screen
import forfeit_confirm_screen  # <-- NOWY IMPORT
import pygame_widgets
from dice import Dice
import settings
import sound_manager

pygame.init()
sound_manager.load_sounds()

screen = pygame.display.set_mode((settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT))
pygame.display.set_caption(settings.SCREEN_TITLE)
game_logic.set_main_screen(screen)

try:
    game_icon = pygame.image.load(settings.IMAGE_PATH_ICON);
    pygame.display.set_icon(game_icon)
except Exception as e:
    print(f"Błąd ładowania ikony: {e}")

menu_screen.load_menu_resources(settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT)
menu_screen.setup_menu_ui_elements(settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT)
name_input_screen.setup_name_input_screen(settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT)
instructions_screen.load_instructions_resources(settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT)
instructions_screen.setup_instructions_ui(settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT,
                                          menu_screen.BUTTON_FONT_MENU)
# setup_settings_screen i setup_forfeit_confirm_screen są wywoływane w game_logic

dice_instance = Dice(initial_x_center=settings.LEFT_PANEL_WIDTH // 2,
                     initial_y_bottom_of_image=settings.GAMEPLAY_SCREEN_HEIGHT - 200)
clock = pygame.time.Clock()
sound_manager.play_music('menu')

running = True
while running:
    dt_seconds = clock.tick(settings.FPS) / 1000.0
    mouse_pos = pygame.mouse.get_pos()
    current_game_state_loop_start = game_logic.game_state
    current_overlay_state_loop_start = game_logic.overlay_state
    current_turn_phase_loop_start = game_logic.turn_phase

    pawn_in_motion = next((p for p in game_logic.all_pawn_objects if p.is_moving or p.is_repositioning), None)

    # Blokuj główny input, gdy są animacje LUB gdy jest aktywna jakakolwiek nakładka
    # lub gdy jest specjalna faza tury
    can_handle_main_game_input = not dice_instance.is_animating and not pawn_in_motion and \
                                 current_overlay_state_loop_start is None and \
                                 not (current_turn_phase_loop_start in ['SHOWING_RESULT_ON_CARD', 'PAWN_MOVING',
                                                                        'PROCESSING_AFTER_ACTION',
                                                                        'INTER_QUESTION_DELAY',
                                                                        'WAITING_FOR_PAWNS',
                                                                        'WAITING_FOR_PROFESSOR_MOVE',
                                                                        'GAME_ENDING_DELAY'])
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            continue

        key_event_handled_globally = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_logic.overlay_state == "SETTINGS":
                    sound_manager.play_sound('button_click');
                    game_logic.close_settings_overlay();
                    key_event_handled_globally = True
                elif game_logic.overlay_state == "CONFIRM_FORFEIT":  # Escape zamyka też potwierdzenie (działa jak "Nie")
                    sound_manager.play_sound('button_click');
                    game_logic.confirm_forfeit_action(False);
                    key_event_handled_globally = True
                elif game_logic.game_state == "GAMEPLAY":
                    pass
                elif game_logic.game_state != "MENU_GLOWNE":
                    sound_manager.play_sound('button_click');
                    game_logic.reset_to_main_menu();
                    key_event_handled_globally = True
                else:
                    print("Wyjście z gry (Esc z menu).");
                    running = False;
                    key_event_handled_globally = True

            elif event.key == pygame.K_s:
                if game_logic.game_state in ["MENU_GLOWNE", "GAMEPLAY"] and game_logic.overlay_state is None:
                    if not (game_logic.game_state == "GAMEPLAY" and game_logic.turn_phase == 'SHOWING_QUESTION'):
                        sound_manager.play_sound('button_click');
                        game_logic.open_settings_overlay()
                    key_event_handled_globally = True
                elif game_logic.overlay_state == "SETTINGS":  # Jeśli 'S' jest wciśnięte gdy ustawienia są otwarte, zamknij je
                    sound_manager.play_sound('button_click');
                    game_logic.close_settings_overlay()
                    key_event_handled_globally = True

            elif event.key == pygame.K_i:
                if game_logic.game_state == "MENU_GLOWNE" and game_logic.overlay_state is None:
                    sound_manager.play_sound('button_click');
                    game_logic.change_game_state("INSTRUCTIONS");
                    key_event_handled_globally = True

            elif event.key == pygame.K_n:
                if game_logic.game_state == "MENU_GLOWNE" and game_logic.overlay_state is None and can_handle_main_game_input:
                    sound_manager.play_sound('button_click');
                    game_logic.change_game_state("GETTING_PLAYER_NAMES");
                    key_event_handled_globally = True

            elif event.key == pygame.K_m:
                if game_logic.game_state != "GETTING_PLAYER_NAMES":
                    muted_state = sound_manager.toggle_mute_all_sounds()
                    print(f"Dźwięk globalnie {'WYCISZONY' if muted_state else 'ODCISZONY'}");
                    key_event_handled_globally = True

        if key_event_handled_globally: continue

        # --- Obsługa Nakładek ---
        if game_logic.overlay_state == "SETTINGS":
            action = settings_screen.handle_settings_input(events, mouse_pos)
            if action == "CLOSE_OVERLAY": sound_manager.play_sound('button_click'); game_logic.close_settings_overlay()
        elif game_logic.overlay_state == "CONFIRM_FORFEIT":
            action = forfeit_confirm_screen.handle_forfeit_confirm_input(event, mouse_pos)
            if action == "CONFIRM_YES":
                game_logic.confirm_forfeit_action(True)  # Dźwięk już w handle_forfeit_confirm_input
            elif action == "CONFIRM_NO":
                game_logic.confirm_forfeit_action(False)  # Dźwięk już w handle_forfeit_confirm_input
        else:  # Jeśli nie ma aktywnej nakładki, obsłuż główny stan gry
            if game_logic.game_state == "GAME_OVER":
                action = game_over_screen.handle_game_over_input(event, mouse_pos)
                if action == "BACK_TO_MENU": sound_manager.play_sound('button_click'); game_logic.reset_to_main_menu()
            elif game_logic.game_state == "GAMEPLAY" and game_logic.turn_phase == 'SHOWING_QUESTION':
                if game_logic.active_question_card:
                    chosen_answer_index = game_logic.active_question_card.handle_event(event, mouse_pos)
                    if chosen_answer_index is not None: game_logic.process_player_answer(chosen_answer_index)
            elif game_logic.game_state == "INSTRUCTIONS":
                action = instructions_screen.handle_instructions_input(event, mouse_pos)
                if action == "BACK_TO_MENU": sound_manager.play_sound('button_click'); game_logic.reset_to_main_menu()
            elif can_handle_main_game_input:
                if game_logic.game_state == "MENU_GLOWNE":
                    action = menu_screen.handle_menu_input(event, mouse_pos)
                    if action:
                        sound_manager.play_sound('button_click')
                        if action == "GAMEPLAY":
                            game_logic.change_game_state("GETTING_PLAYER_NAMES")
                        elif action == "INSTRUCTIONS":
                            game_logic.change_game_state("INSTRUCTIONS")
                        elif action == "SETTINGS":
                            game_logic.open_settings_overlay()
                        elif action == "QUIT":
                            running = False
                elif game_logic.game_state == "GETTING_PLAYER_NAMES":
                    action = name_input_screen.handle_name_input_events(event, mouse_pos)
                    if action == "START_GAME": sound_manager.play_sound('button_click'); game_logic.start_new_game(
                        name_input_screen.player_names_input)
                elif game_logic.game_state == "GAMEPLAY":
                    gameplay_action = gameplay_screen.handle_gameplay_input(event, mouse_pos)
                    if gameplay_action:
                        if gameplay_action == "ROLL_DICE_PANEL" and game_logic.turn_phase == 'WAITING_FOR_ROLL':
                            sound_manager.play_sound('dice_roll', loops=-1);
                            dice_instance.start_animation_and_roll();
                            game_logic.turn_phase = 'DICE_ROLLING'
                        elif gameplay_action == "FORFEIT_GAME":
                            # game_logic.forfeit_game() jest teraz wywoływane po potwierdzeniu
                            sound_manager.play_sound('button_click')
                            game_logic.forfeit_game()  # To teraz otwiera nakładkę potwierdzenia
                        elif gameplay_action == "OPEN_SETTINGS_OVERLAY":
                            sound_manager.play_sound('button_click');
                            game_logic.open_settings_overlay()

    # Aktualizacja Logiki
    if game_logic.overlay_state == "SETTINGS":
        settings_screen.update_volumes_from_sliders()
    # Nie ma potrzeby update dla CONFIRM_FORFEIT, bo to tylko input
    elif game_logic.game_state == "GAMEPLAY":
        is_dice_rolling_before_update = dice_instance.is_animating
        game_logic.update_game_logic(dt_seconds, dice_instance)
        if is_dice_rolling_before_update and not dice_instance.is_animating: sound_manager.stop_sound('dice_roll')
        gameplay_screen.update_gameplay_state(game_logic.current_player_id, dt_seconds)
        if game_logic.active_question_card: game_logic.active_question_card.update_hover(mouse_pos)
    elif game_logic.game_state == "GAME_OVER":
        game_over_screen.update_game_over_screen(dt_seconds)

    # Rysowanie
    screen.fill(settings.DEFAULT_BG_COLOR)

    state_to_draw_background = game_logic.previous_game_state if game_logic.overlay_state in ["SETTINGS",
                                                                                              "CONFIRM_FORFEIT"] else game_logic.game_state

    if state_to_draw_background == "MENU_GLOWNE":
        menu_screen.draw_menu_screen(screen, game_logic.current_screen_width, game_logic.current_screen_height,
                                     mouse_pos)
    elif state_to_draw_background == "GETTING_PLAYER_NAMES":
        name_input_screen.draw_name_input_screen(screen, game_logic.current_screen_width,
                                                 game_logic.current_screen_height, mouse_pos, dt_seconds)
    elif state_to_draw_background == "GAMEPLAY":
        gameplay_screen.draw_gameplay_screen(screen, mouse_pos, dice_instance)
        for pawn in game_logic.all_pawn_objects: pawn.draw(screen)
        if game_logic.active_question_card and game_logic.active_question_card.is_visible: game_logic.active_question_card.draw(
            screen)
    elif state_to_draw_background == "INSTRUCTIONS":
        instructions_screen.draw_instructions_screen(screen, mouse_pos)

    # Rysowanie nakładek NA WIERZCHU
    if game_logic.overlay_state == "SETTINGS":
        overlay_surface = pygame.Surface((game_logic.current_screen_width, game_logic.current_screen_height),
                                         pygame.SRCALPHA)
        overlay_surface.fill(settings.GAME_OVER_BG_COLOR);
        screen.blit(overlay_surface, (0, 0))
        settings_screen.draw_settings_screen(screen, mouse_pos);
        pygame_widgets.update(events)
    elif game_logic.overlay_state == "CONFIRM_FORFEIT":
        forfeit_confirm_screen.draw_forfeit_confirm_screen(screen, mouse_pos)

    if game_logic.game_state == "GAME_OVER" and game_logic.overlay_state is None:
        game_over_screen.draw_game_over_screen(screen, mouse_pos)

    pygame.display.flip()

pygame.quit()
sys.exit()