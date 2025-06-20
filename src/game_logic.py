# src/game_logic.py
import pygame
import settings
import gameplay_screen
import menu_screen
from pawn import PlayerPawn, ProfessorPawn
import question_manager
from question_screen import QuestionCard

# --- Stałe dla Logiki Gry ---
SPECIAL_FIELDS = ["START", "STYPENDIUM", "EGZAMIN", "POPRAWKA"]

# --- Zmienne Stanu Aplikacji (zarządzane centralnie) ---
game_state = "MENU_GLOWNE"
current_screen_width = settings.INITIAL_SCREEN_WIDTH
current_screen_height = settings.INITIAL_SCREEN_HEIGHT
screen = None

# --- Zmienne Logiki Gry ---
all_sprites_group = pygame.sprite.Group()
pawns_on_fields_map = {}
all_pawn_objects = []
current_player_id = "player_1"
turn_phase = 'WAITING_FOR_ROLL'
pawn_that_was_moving = None
final_player_names = []
active_question_card = None
player_points = {}
exam_mode_active = False
exam_questions_left = 0
professor_move_pending = 0
delay_timer = 0.0
points_to_animate = 0


def set_main_screen(main_screen_surface):
    global screen
    screen = main_screen_surface


def change_game_state(new_state):
    global game_state
    if game_state == new_state: return
    print(f"Zmiana stanu gry z '{game_state}' na '{new_state}'")
    game_state = new_state
    if new_state == "GAMEPLAY" and (
            current_screen_width != settings.GAMEPLAY_SCREEN_WIDTH or current_screen_height != settings.GAMEPLAY_SCREEN_HEIGHT):
        set_screen_mode(settings.GAMEPLAY_SCREEN_WIDTH, settings.GAMEPLAY_SCREEN_HEIGHT)
    elif new_state in ["MENU_GLOWNE", "INSTRUCTIONS", "GETTING_PLAYER_NAMES"] and (
            current_screen_width != settings.INITIAL_SCREEN_WIDTH or current_screen_height != settings.INITIAL_SCREEN_HEIGHT):
        set_screen_mode(settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT)
    else:
        if new_state == "GETTING_PLAYER_NAMES":
            import name_input_screen; name_input_screen.setup_name_input_screen(current_screen_width,
                                                                                current_screen_height)
        elif new_state == "GAMEPLAY":
            initialize_gameplay()


def set_screen_mode(width, height):
    global screen, current_screen_width, current_screen_height
    current_screen_width = width;
    current_screen_height = height
    screen = pygame.display.set_mode((current_screen_width, current_screen_height))
    print(f"Tryb ekranu zmieniony na: {width}x{height}")
    if game_state == "MENU_GLOWNE":
        menu_screen.load_menu_resources(current_screen_width,
                                        current_screen_height); menu_screen.setup_menu_ui_elements(current_screen_width,
                                                                                                   current_screen_height)
    elif game_state == "GAMEPLAY":
        initialize_gameplay()
    elif game_state == "INSTRUCTIONS":
        menu_screen.load_menu_resources(current_screen_width, current_screen_height)
    elif game_state == "GETTING_PLAYER_NAMES":
        import name_input_screen; name_input_screen.setup_name_input_screen(current_screen_width, current_screen_height)


def initialize_gameplay():
    global final_player_names;
    print("Rozpoczynam inicjalizację rozgrywki...")
    question_manager.reset_available_questions()
    gameplay_screen.load_gameplay_resources(current_screen_width, current_screen_height)
    gameplay_screen.setup_gameplay_ui_elements(current_screen_height, final_player_names)
    initialize_game_logic_and_pawns()


def start_new_game(player_names_from_input):
    global final_player_names;
    final_player_names = [name.strip() if name.strip() else f"Gracz {i + 1}" for i, name in
                          enumerate(player_names_from_input)]
    print(f"Ostateczne imiona graczy: {final_player_names}");
    change_game_state("GAMEPLAY")


# === PRZYWRÓCONA FUNKCJA ===
def add_points_to_player(player_id, points_to_change):
    """TYLKO aktualizuje logiczną wartość punktów w słowniku i zwraca faktyczną zmianę."""
    global player_points
    current_points = player_points.get(player_id, 0)

    # Oblicz, jaka będzie faktyczna zmiana, uwzględniając, że punkty nie mogą być ujemne
    actual_change = points_to_change
    if current_points + points_to_change < 0:
        actual_change = -current_points

    player_points[player_id] += actual_change

    # Zwraca, o ile FAKTYCZNIE zmieniły się punkty
    return actual_change


# ===========================

def trigger_points_animation(player_id, points_value_to_show):
    """Uruchamia animację "pływającego tekstu" w odpowiednim widgecie z DOKŁADNĄ wartością do pokazania."""
    if points_value_to_show == 0: return
    try:
        player_index = int(player_id.split('_')[1]) - 1
        if 0 <= player_index < len(gameplay_screen.player_widgets):
            gameplay_screen.player_widgets[player_index].start_points_animation(points_value_to_show)
    except (IndexError, ValueError) as e:
        print(f"Błąd przy uruchamianiu animacji punktów dla ID '{player_id}': {e}")


def update_player_widgets_points():
    """Aktualizuje wyświetlaną liczbę punktów w widgetach na podstawie słownika player_points."""
    if gameplay_screen.player_widgets:
        for i, widget in enumerate(gameplay_screen.player_widgets):
            player_id = f"player_{i + 1}"
            widget.points = player_points.get(player_id, 0)


def update_active_pawn_indicator():
    """Ustawia flagę `is_active_turn` dla widgetów i pionków."""
    # Aktualizuj widgety
    for widget in gameplay_screen.player_widgets:
        widget.set_active(widget.player_id == current_player_id)
    # Aktualizuj obiekty pionków
    for pawn in all_pawn_objects:
        pawn.set_active(pawn.pawn_id == current_player_id)


def initialize_game_logic_and_pawns():
    global all_sprites_group, pawns_on_fields_map, all_pawn_objects, current_player_id, turn_phase, pawn_that_was_moving, player_points, professor_move_pending, points_to_animate
    all_sprites_group.empty();
    pawns_on_fields_map.clear();
    all_pawn_objects.clear()
    current_player_id = "player_1";
    turn_phase = 'WAITING_FOR_ROLL';
    pawn_that_was_moving = None
    professor_move_pending = 0;
    points_to_animate = 0
    player_points = {"player_1": 0, "player_2": 0};
    update_player_widgets_points()
    if gameplay_screen.game_board_instance:
        try:
            player1 = PlayerPawn(1, settings.IMAGE_PATH_PLAYER1_PAWN, 0, gameplay_screen.game_board_instance);
            add_pawn_to_field_map(player1, 0);
            all_sprites_group.add(player1);
            all_pawn_objects.append(player1)
            player2 = PlayerPawn(2, settings.IMAGE_PATH_PLAYER2_PAWN, 0, gameplay_screen.game_board_instance);
            add_pawn_to_field_map(player2, 0);
            all_sprites_group.add(player2);
            all_pawn_objects.append(player2)
            professor = ProfessorPawn(settings.IMAGE_PATH_PROFESSOR_PAWN, 0, gameplay_screen.game_board_instance);
            add_pawn_to_field_map(professor, 0);
            all_sprites_group.add(professor);
            all_pawn_objects.append(professor)
            start_pawns_repositioning_on_field(0);
            update_active_pawn_indicator();
            print("Logika gry i pionki zainicjalizowane.")
        except Exception as e:
            print(f"Błąd krytyczny podczas inicjalizacji pionków: {e}")
    else:
        print("BŁĄD KRYTYCZNY: game_board_instance nie istnieje.")


def move_professor(steps=1):
    global turn_phase
    professor = next((p for p in all_pawn_objects if p.pawn_id == "professor"), None)
    if professor and gameplay_screen.game_board_instance:
        total_fields = gameplay_screen.game_board_instance.get_total_fields();
        old_prof_index = professor.board_field_index
        path = [(old_prof_index + i + 1) % total_fields for i in range(steps)];
        if not path: turn_phase = 'PROCESSING_AFTER_ACTION'; return
        professor.start_move_animation(path.copy())
        new_prof_index = path[-1]
        remove_pawn_from_field_map(professor, old_prof_index);
        add_pawn_to_field_map(professor, new_prof_index)
        turn_phase = 'PROCESSING_AFTER_ACTION'
        print(f"Profesor przesuwa się na pole {new_prof_index}")


def add_pawn_to_field_map(pawn_obj, field_index):
    if field_index not in pawns_on_fields_map: pawns_on_fields_map[field_index] = []
    if pawn_obj not in pawns_on_fields_map[field_index]: pawns_on_fields_map[field_index].append(pawn_obj)


def remove_pawn_from_field_map(pawn_obj_to_remove, field_index):
    if field_index in pawns_on_fields_map:
        pawns_on_fields_map[field_index] = [p for p in pawns_on_fields_map[field_index] if
                                            p.pawn_id != pawn_obj_to_remove.pawn_id]
        if not pawns_on_fields_map[field_index]: del pawns_on_fields_map[field_index]


def get_pawn_objects_on_field(field_index): return pawns_on_fields_map.get(field_index, [])


def start_pawns_repositioning_on_field(field_index):
    pawn_objects_on_field = get_pawn_objects_on_field(field_index);
    if not pawn_objects_on_field: return
    pawn_ids_on_field = [p.pawn_id for p in pawn_objects_on_field]
    for pawn_obj in pawn_objects_on_field: pawn_obj.update_visual_position_on_field(field_index, pawn_ids_on_field)


def start_pawn_move(roll_value):
    global turn_phase, pawn_that_was_moving
    pawn_to_move = next((p for p in all_pawn_objects if p.pawn_id == current_player_id), None)
    if not pawn_to_move or not gameplay_screen.game_board_instance: switch_turn(); return
    total_fields = gameplay_screen.game_board_instance.get_total_fields()
    if total_fields == 0 or roll_value == 0: switch_turn(); return
    path_indices = [];
    start_idx = pawn_to_move.board_field_index;
    current_idx_in_path = start_idx
    for _ in range(roll_value): current_idx_in_path = (current_idx_in_path + 1) % total_fields; path_indices.append(
        current_idx_in_path)
    if not path_indices: switch_turn(); return
    pawn_that_was_moving = pawn_to_move;
    pawn_that_was_moving.start_move_animation(path_indices)
    turn_phase = 'PAWN_MOVING';
    print(f"Pionek {current_player_id} (z pola {start_idx}) rozpoczyna ruch o {roll_value} pól.")


def switch_turn():
    global current_player_id, turn_phase
    if current_player_id == "player_1":
        current_player_id = "player_2"
    elif current_player_id == "player_2":
        current_player_id = "player_1"
    print(f"--- Następna tura: Gracz {current_player_id} ---")
    turn_phase = 'WAITING_FOR_ROLL';
    update_active_pawn_indicator()


def process_player_answer(chosen_answer_index):
    global turn_phase, active_question_card, professor_move_pending, points_to_animate
    if not active_question_card: return
    active_question_card.show_result(chosen_answer_index)
    correct_index = active_question_card.question_data["correct_answer_index"]
    if chosen_answer_index == correct_index:
        print("ODPOWIEDŹ POPRAWNA!");
        points_to_animate = settings.POINTS_FOR_EXAM_CORRECT if exam_mode_active else settings.POINTS_FOR_CORRECT_ANSWER
    else:
        print("ODPOWIEDŹ BŁĘDNA!");
        professor_move_pending = 1
        if exam_mode_active: points_to_animate = settings.POINTS_FOR_EXAM_INCORRECT
    turn_phase = 'SHOWING_RESULT_ON_CARD'


def ask_next_exam_question():
    global exam_questions_left, active_question_card, turn_phase
    if exam_questions_left > 0:
        question = question_manager.get_random_question_from_any_subject()
        if question:
            exam_questions_left -= 1;
            subject_name = question.get("original_subject", "EGZAMIN")
            active_question_card = QuestionCard(question, subject_name)
            turn_phase = 'SHOWING_QUESTION';
            print(f"Pytanie egzaminacyjne ({3 - exam_questions_left}/3): {subject_name}")
        else:
            print("Brak więcej pytań w puli! Kończę egzamin."); end_exam_mode()
    else:
        end_exam_mode()


def end_exam_mode():
    global exam_mode_active, turn_phase;
    print("Egzamin zakończony.");
    exam_mode_active = False;
    turn_phase = 'PROCESSING_AFTER_ACTION'


def handle_field_action():
    global turn_phase, active_question_card, exam_mode_active, exam_questions_left, points_to_animate
    active_pawn = next((p for p in all_pawn_objects if p.pawn_id == current_player_id), None)
    if not (active_pawn and gameplay_screen.game_board_instance): turn_phase = 'PROCESSING_AFTER_ACTION'; return
    field_data = gameplay_screen.game_board_instance.get_field_data(active_pawn.board_field_index)
    if field_data:
        subject_name = field_data["label"].upper()
        if subject_name == "STYPENDIUM":
            print("Pole specjalne: STYPENDIUM! +2 ECTS");
            points_to_animate = settings.POINTS_FOR_SCHOLARSHIP;
            turn_phase = 'PROCESSING_AFTER_ACTION'
        elif subject_name == "POPRAWKA":
            print("Pole specjalne: POPRAWKA! -2 ECTS");
            points_to_animate = settings.POINTS_FOR_RETAKE;
            turn_phase = 'PROCESSING_AFTER_ACTION'
        elif subject_name == "EGZAMIN":
            print(
                "Pole specjalne: EGZAMIN! Czas na 3 pytania."); exam_mode_active = True; exam_questions_left = 3; ask_next_exam_question()
        elif subject_name not in SPECIAL_FIELDS:
            question = question_manager.get_random_question_for_subject(subject_name)
            if question:
                active_question_card = QuestionCard(question, subject_name); turn_phase = 'SHOWING_QUESTION'
            else:
                print(f"Brak pytań dla: {subject_name}."); turn_phase = 'PROCESSING_AFTER_ACTION'
        else:
            print(f"Wylądowano na polu: {subject_name}."); turn_phase = 'PROCESSING_AFTER_ACTION'
    else:
        print(f"Brak danych dla pola {active_pawn.board_field_index}"); turn_phase = 'PROCESSING_AFTER_ACTION'


def update_game_logic(dt_seconds, dice_instance):
    global turn_phase, pawn_that_was_moving, active_question_card, professor_move_pending, delay_timer, points_to_animate, exam_mode_active
    all_sprites_group.update(dt_seconds);
    dice_instance.update(dt_seconds)
    if turn_phase == 'DICE_ROLLING' and not dice_instance.is_animating:
        roll_value = dice_instance.get_final_roll_result();
        start_pawn_move(roll_value)
    elif turn_phase == 'PAWN_MOVING' and pawn_that_was_moving and not pawn_that_was_moving.is_moving:
        final_board_index = pawn_that_was_moving.board_field_index;
        total_fields = gameplay_screen.game_board_instance.get_total_fields()
        roll_amount = dice_instance.current_roll;
        old_board_index = (final_board_index - roll_amount + total_fields) % total_fields
        remove_pawn_from_field_map(pawn_that_was_moving, old_board_index);
        add_pawn_to_field_map(pawn_that_was_moving, final_board_index)
        start_pawns_repositioning_on_field(old_board_index);
        start_pawns_repositioning_on_field(final_board_index)
        turn_phase = 'FIELD_ACTION';
        pawn_that_was_moving = None
    elif turn_phase == 'FIELD_ACTION':
        any_pawn_repositioning = next((p for p in all_pawn_objects if p.is_repositioning), None)
        if not any_pawn_repositioning: handle_field_action()
    elif turn_phase == 'SHOWING_RESULT_ON_CARD':
        if active_question_card:
            active_question_card.update(dt_seconds)
            if not active_question_card.is_visible:
                active_question_card = None;
                turn_phase = 'PROCESSING_AFTER_ACTION'
    elif turn_phase == 'PROCESSING_AFTER_ACTION':
        any_pawn_moving = next((p for p in all_pawn_objects if p.is_moving or p.is_repositioning), None)
        if not any_pawn_moving:
            if points_to_animate != 0:
                add_points_to_player(current_player_id, points_to_animate)
                update_player_widgets_points()
                trigger_points_animation(current_player_id, points_to_animate)
                points_to_animate = 0
            if professor_move_pending > 0:
                move_professor(professor_move_pending);
                professor_move_pending = 0
                # Nie zmieniamy tu fazy, bo move_professor sam to zrobi
            elif exam_mode_active:
                delay_timer = 0.0;
                turn_phase = 'INTER_QUESTION_DELAY'
            else:
                switch_turn()
    elif turn_phase == 'INTER_QUESTION_DELAY':
        delay_timer += dt_seconds
        if delay_timer >= settings.INTER_QUESTION_DELAY_SECONDS: ask_next_exam_question()
    elif turn_phase == 'WAITING_FOR_PAWNS':
        any_pawn_moving = next((p for p in all_pawn_objects if p.is_moving or p.is_repositioning), None)
        if not any_pawn_moving:
            if exam_mode_active:
                delay_timer = 0.0;
                turn_phase = 'INTER_QUESTION_DELAY'
            else:
                switch_turn()