# src/game_logic.py
import pygame
import settings
import gameplay_screen
import menu_screen
from pawn import PlayerPawn, ProfessorPawn
import question_manager
from question_screen import QuestionCard
from feedback_card import FeedbackCard # <-- NOWY IMPORT

# --- Stałe ---
SPECIAL_FIELDS = ["START", "STYPENDIUM", "EGZAMIN", "POPRAWKA"]

# --- Zmienne Stanu ---
game_state = "MENU_GLOWNE"
current_screen_width = settings.INITIAL_SCREEN_WIDTH
current_screen_height = settings.INITIAL_SCREEN_HEIGHT
screen = None

all_sprites_group = pygame.sprite.Group()
pawns_on_fields_map = {}
all_pawn_objects = []
current_player_id = "player_1"
turn_phase = 'WAITING_FOR_ROLL'
pawn_that_was_moving = None
final_player_names = []
active_question_card = None
active_feedback_card = None # <-- NOWA ZMIENNA

def set_main_screen(main_screen_surface):
    global screen
    screen = main_screen_surface

def change_game_state(new_state):
    global game_state
    if game_state == new_state: return
    print(f"Zmiana stanu gry z '{game_state}' na '{new_state}'")
    game_state = new_state
    if new_state == "GAMEPLAY":
        if current_screen_width != settings.GAMEPLAY_SCREEN_WIDTH or current_screen_height != settings.GAMEPLAY_SCREEN_HEIGHT:
            set_screen_mode(settings.GAMEPLAY_SCREEN_WIDTH, settings.GAMEPLAY_SCREEN_HEIGHT)
        else:
            initialize_gameplay()
    elif new_state in ["MENU_GLOWNE", "INSTRUCTIONS", "GETTING_PLAYER_NAMES"]:
        if current_screen_width != settings.INITIAL_SCREEN_WIDTH or current_screen_height != settings.INITIAL_SCREEN_HEIGHT:
            set_screen_mode(settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT)
        else:
            if new_state == "GETTING_PLAYER_NAMES":
                import name_input_screen
                name_input_screen.setup_name_input_screen(current_screen_width, current_screen_height)

def set_screen_mode(width, height):
    global screen, current_screen_width, current_screen_height
    current_screen_width = width; current_screen_height = height
    screen = pygame.display.set_mode((current_screen_width, current_screen_height))
    print(f"Tryb ekranu zmieniony na: {width}x{height}")
    if game_state == "MENU_GLOWNE":
        menu_screen.load_menu_resources(current_screen_width, current_screen_height)
        menu_screen.setup_menu_ui_elements(current_screen_width, current_screen_height)
    elif game_state == "GAMEPLAY": initialize_gameplay()
    elif game_state == "INSTRUCTIONS": menu_screen.load_menu_resources(current_screen_width, current_screen_height)
    elif game_state == "GETTING_PLAYER_NAMES":
        import name_input_screen
        name_input_screen.setup_name_input_screen(current_screen_width, current_screen_height)

def initialize_gameplay():
    global final_player_names
    print("Rozpoczynam inicjalizację rozgrywki...")
    question_manager.reset_available_questions()
    gameplay_screen.load_gameplay_resources(current_screen_width, current_screen_height)
    gameplay_screen.setup_gameplay_ui_elements(current_screen_height, final_player_names)
    initialize_game_logic_and_pawns()

def start_new_game(player_names_from_input):
    global final_player_names
    final_player_names = [name.strip() if name.strip() else f"Gracz {i+1}" for i, name in enumerate(player_names_from_input)]
    print(f"Ostateczne imiona graczy: {final_player_names}")
    change_game_state("GAMEPLAY")

def update_active_pawn_indicator():
    for pawn in all_pawn_objects:
        pawn.set_active(pawn.pawn_id.startswith("player_") and pawn.pawn_id == current_player_id)

def initialize_game_logic_and_pawns():
    global all_sprites_group, pawns_on_fields_map, all_pawn_objects, current_player_id, turn_phase, pawn_that_was_moving
    all_sprites_group.empty(); pawns_on_fields_map.clear(); all_pawn_objects.clear()
    current_player_id = "player_1"; turn_phase = 'WAITING_FOR_ROLL'; pawn_that_was_moving = None
    if gameplay_screen.game_board_instance:
        try:
            player1 = PlayerPawn(1, settings.IMAGE_PATH_PLAYER1_PAWN, 0, gameplay_screen.game_board_instance)
            add_pawn_to_field_map(player1, 0); all_sprites_group.add(player1); all_pawn_objects.append(player1)
            player2 = PlayerPawn(2, settings.IMAGE_PATH_PLAYER2_PAWN, 0, gameplay_screen.game_board_instance)
            add_pawn_to_field_map(player2, 0); all_sprites_group.add(player2); all_pawn_objects.append(player2)
            professor = ProfessorPawn(settings.IMAGE_PATH_PROFESSOR_PAWN, 0, gameplay_screen.game_board_instance)
            add_pawn_to_field_map(professor, 0); all_sprites_group.add(professor); all_pawn_objects.append(professor)
            start_pawns_repositioning_on_field(0); update_active_pawn_indicator()
            print("Logika gry i pionki zainicjalizowane.")
        except Exception as e: print(f"Błąd krytyczny podczas inicjalizacji pionków: {e}")
    else: print("BŁĄD KRYTYCZNY: game_board_instance nie istnieje.")

def add_pawn_to_field_map(pawn_obj, field_index):
    if field_index not in pawns_on_fields_map: pawns_on_fields_map[field_index] = []
    if pawn_obj not in pawns_on_fields_map[field_index]: pawns_on_fields_map[field_index].append(pawn_obj)

def remove_pawn_from_field_map(pawn_obj_to_remove, field_index):
    if field_index in pawns_on_fields_map:
        pawns_on_fields_map[field_index] = [p for p in pawns_on_fields_map[field_index] if p.pawn_id != pawn_obj_to_remove.pawn_id]
        if not pawns_on_fields_map[field_index]: del pawns_on_fields_map[field_index]

def get_pawn_objects_on_field(field_index): return pawns_on_fields_map.get(field_index, [])

def start_pawns_repositioning_on_field(field_index):
    pawn_objects_on_field = get_pawn_objects_on_field(field_index)
    if not pawn_objects_on_field: return
    pawn_ids_on_field = [p.pawn_id for p in pawn_objects_on_field]
    for pawn_obj in pawn_objects_on_field: pawn_obj.update_visual_position_on_field(field_index, pawn_ids_on_field)

def start_pawn_move(roll_value):
    global turn_phase, pawn_that_was_moving
    pawn_to_move = next((p for p in all_pawn_objects if p.pawn_id == current_player_id), None)
    if not pawn_to_move or not gameplay_screen.game_board_instance: switch_turn(); return
    total_fields = gameplay_screen.game_board_instance.get_total_fields()
    if total_fields == 0 or roll_value == 0: switch_turn(); return
    path_indices = []; start_idx = pawn_to_move.board_field_index; current_idx_in_path = start_idx
    for _ in range(roll_value):
        current_idx_in_path = (current_idx_in_path + 1) % total_fields;
        path_indices.append(current_idx_in_path)
    if not path_indices: switch_turn(); return
    pawn_that_was_moving = pawn_to_move; pawn_that_was_moving.start_move_animation(path_indices)
    turn_phase = 'PAWN_MOVING'; print(f"Pionek {current_player_id} (z pola {start_idx}) rozpoczyna ruch o {roll_value} pól.")

def switch_turn():
    global current_player_id, turn_phase
    if current_player_id == "player_1": current_player_id = "player_2"
    elif current_player_id == "player_2": current_player_id = "player_1"
    print(f"--- Następna tura: Gracz {current_player_id} ---")
    turn_phase = 'WAITING_FOR_ROLL'; update_active_pawn_indicator()

def handle_field_action():
    global turn_phase, active_question_card
    active_pawn = next((p for p in all_pawn_objects if p.pawn_id == current_player_id), None)
    if not (active_pawn and gameplay_screen.game_board_instance): print(f"Błąd: Nie można wykonać akcji pola dla {current_player_id}."); switch_turn(); return
    field_data = gameplay_screen.game_board_instance.get_field_data(active_pawn.board_field_index)
    if field_data:
        subject_name = field_data["label"]
        if subject_name.upper() not in SPECIAL_FIELDS:
            question = question_manager.get_random_question_for_subject(subject_name)
            if question:
                print(f"POLE Z PYTANIEM! Przedmiot: {subject_name}")
                active_question_card = QuestionCard(question, subject_name); turn_phase = 'SHOWING_QUESTION'
            else: print(f"Brak dostępnych pytań dla: {subject_name}."); switch_turn()
        else: print(f"Wylądowano na polu specjalnym: {subject_name}."); switch_turn()
    else: print(f"Brak danych dla pola {active_pawn.board_field_index}"); switch_turn()


def process_player_answer(chosen_answer_index):
    """Weryfikuje odpowiedź gracza i przygotowuje do następnej tury."""
    global turn_phase, active_question_card, active_feedback_card
    if not active_question_card: return

    correct_index = active_question_card.question_data["correct_answer_index"]

    if chosen_answer_index == correct_index:
        print("ODPOWIEDŹ POPRAWNA!")
        active_feedback_card = FeedbackCard("POPRAWNA ODPOWIEDŹ!", 'success')
      
    else:
        print("ODPOWIEDŹ BŁĘDNA!")
        active_feedback_card = FeedbackCard("BŁĘDNA ODPOWIEDŹ!", 'error')


    active_question_card = None  # Usuń kartę pytania
    turn_phase = 'SHOWING_FEEDBACK'  # Zmień stan na pokazywanie feedbacku

def update_game_logic(dt_seconds, dice_instance):
    global turn_phase, pawn_that_was_moving, active_feedback_card
    all_sprites_group.update(dt_seconds); dice_instance.update(dt_seconds)
    if turn_phase == 'DICE_ROLLING' and not dice_instance.is_animating:
        roll_value = dice_instance.get_final_roll_result(); start_pawn_move(roll_value)
    elif turn_phase == 'PAWN_MOVING' and pawn_that_was_moving and not pawn_that_was_moving.is_moving:
        final_board_index = pawn_that_was_moving.board_field_index
        total_fields = gameplay_screen.game_board_instance.get_total_fields()
        roll_amount = dice_instance.current_roll
        old_board_index = (final_board_index - roll_amount + total_fields) % total_fields
        remove_pawn_from_field_map(pawn_that_was_moving, old_board_index)
        add_pawn_to_field_map(pawn_that_was_moving, final_board_index)
        start_pawns_repositioning_on_field(old_board_index); start_pawns_repositioning_on_field(final_board_index)
        turn_phase = 'FIELD_ACTION'; pawn_that_was_moving = None
    elif turn_phase == 'FIELD_ACTION':
        any_pawn_repositioning = next((p for p in all_pawn_objects if p.is_repositioning), None)
        if not any_pawn_repositioning: handle_field_action()
    elif turn_phase == 'SHOWING_FEEDBACK':
        if active_feedback_card:
            active_feedback_card.update(dt_seconds)
            if not active_feedback_card.is_visible: active_feedback_card = None; turn_phase = 'WAITING_FOR_PAWNS_AFTER_FEEDBACK'
    elif turn_phase == 'WAITING_FOR_PAWNS_AFTER_FEEDBACK':
        any_pawn_moving = next((p for p in all_pawn_objects if p.is_moving or p.is_repositioning), None)
        if not any_pawn_moving:
            professor = next((p for p in all_pawn_objects if p.pawn_id == 'professor'), None)
            if professor: start_pawns_repositioning_on_field(professor.board_field_index)
            switch_turn()