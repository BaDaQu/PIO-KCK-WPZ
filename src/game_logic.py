# src/game_logic.py
import pygame
import settings
import gameplay_screen
import menu_screen
import instructions_screen
import game_over_screen
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
professor_that_was_moving = None
final_player_names = []
active_question_card = None
player_points = {}
player_lives = {}
exam_mode_active = False
exam_questions_left = 0
exam_correct_answers_count = 0
professor_move_pending = 0
global_turn_counter = 0
points_to_animate = 0
delay_timer = 0.0
winner_data = None


def set_main_screen(main_screen_surface):
    """Pozwala głównemu plikowi przekazać instancję ekranu do tego modułu."""
    global screen
    screen = main_screen_surface


def reset_to_main_menu():
    """
    Resetuje wszystkie kluczowe zmienne logiki gry do stanu początkowego,
    przygotowując do powrotu do menu głównego.
    """
    global game_state, turn_phase, active_question_card, pawn_that_was_moving, professor_that_was_moving
    global final_player_names, player_points, player_lives, exam_mode_active, professor_move_pending
    global global_turn_counter, points_to_animate

    print("Resetowanie stanu gry do menu głównego...")

    # Reset stanów aplikacji i logiki
    game_state = "MENU_GLOWNE"
    turn_phase = 'WAITING_FOR_ROLL'

    # Wyczyszczenie aktywnych obiektów
    active_question_card = None
    pawn_that_was_moving = None
    professor_that_was_moving = None

    # Reset danych graczy i gry
    final_player_names = []
    player_points = {}
    player_lives = {}
    exam_mode_active = False
    professor_move_pending = 0
    global_turn_counter = 0
    points_to_animate = 0

    # Wyczyszczenie grup sprite'ów i list obiektów
    all_sprites_group.empty()
    pawns_on_fields_map.clear()
    all_pawn_objects.clear()

    # Zapewnij, że menu jest poprawnie skonfigurowane
    if current_screen_width != settings.INITIAL_SCREEN_WIDTH or current_screen_height != settings.INITIAL_SCREEN_HEIGHT:
        set_screen_mode(settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT)
    else:
        # Ponowne załadowanie zasobów menu dla pewności
        menu_screen.load_menu_resources(current_screen_width, current_screen_height)
        menu_screen.setup_menu_ui_elements(current_screen_width, current_screen_height)


def change_game_state(new_state, data=None):
    """Centralna funkcja do zmiany stanu gry."""
    global game_state, winner_data
    if game_state == new_state and new_state != "GAME_OVER": return
    print(f"Zmiana stanu gry z '{game_state}' na '{new_state}'")
    game_state = new_state

    if new_state == "GAME_OVER":
        winner_data = data
        game_over_screen.setup_game_over_screen(current_screen_width, current_screen_height, winner_data)
    elif new_state == "GAMEPLAY" and (
            current_screen_width != settings.GAMEPLAY_SCREEN_WIDTH or current_screen_height != settings.GAMEPLAY_SCREEN_HEIGHT):
        set_screen_mode(settings.GAMEPLAY_SCREEN_WIDTH, settings.GAMEPLAY_SCREEN_HEIGHT)
    elif new_state in ["MENU_GLOWNE", "INSTRUCTIONS", "GETTING_PLAYER_NAMES", "GAME_OVER"] and (
            current_screen_width != settings.INITIAL_SCREEN_WIDTH or current_screen_height != settings.INITIAL_SCREEN_HEIGHT):
        set_screen_mode(settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT)
    else:
        if new_state == "GETTING_PLAYER_NAMES":
            import name_input_screen
            name_input_screen.setup_name_input_screen(current_screen_width, current_screen_height)
        elif new_state == "GAMEPLAY":
            initialize_gameplay()


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
        initialize_gameplay()
    elif game_state == "INSTRUCTIONS":
        instructions_screen.load_instructions_resources(current_screen_width, current_screen_height)
        instructions_screen.setup_instructions_ui(current_screen_width, current_screen_height,
                                                  menu_screen.BUTTON_FONT_MENU)
    elif game_state == "GETTING_PLAYER_NAMES":
        import name_input_screen
        name_input_screen.setup_name_input_screen(current_screen_width, current_screen_height)


def initialize_gameplay():
    """Przygotowuje wszystko do rozpoczęcia nowej gry, używając imion."""
    global final_player_names
    print("Rozpoczynam inicjalizację rozgrywki...")
    question_manager.reset_available_questions()
    gameplay_screen.load_gameplay_resources(current_screen_width, current_screen_height)
    gameplay_screen.setup_gameplay_ui_elements(current_screen_height, final_player_names)
    initialize_game_logic_and_pawns()


def start_new_game(player_names_from_input):
    """Przetwarza imiona i uruchamia grę."""
    global final_player_names
    final_player_names = [name.strip() if name.strip() else f"Gracz {i + 1}" for i, name in
                          enumerate(player_names_from_input)]
    print(f"Ostateczne imiona graczy: {final_player_names}")
    change_game_state("GAMEPLAY")


def add_points_to_player(player_id, points_to_change):
    """Aktualizuje logiczną wartość punktów i zwraca faktyczną zmianę."""
    global player_points
    current_points = player_points.get(player_id, 0)
    actual_change = points_to_change
    if current_points + points_to_change < 0:
        actual_change = -current_points
    player_points[player_id] += actual_change
    return actual_change


def trigger_points_animation(player_id, points_value_to_show):
    """Uruchamia animację "pływającego tekstu" w odpowiednim widgecie."""
    if points_value_to_show == 0: return
    try:
        player_index = int(player_id.split('_')[1]) - 1
        if 0 <= player_index < len(gameplay_screen.player_widgets):
            gameplay_screen.player_widgets[player_index].start_points_animation(points_value_to_show)
    except (IndexError, ValueError) as e:
        print(f"Błąd przy uruchamianiu animacji punktów dla ID '{player_id}': {e}")


def update_player_widgets_data():
    """Aktualizuje DANE (punkty i życia) w widgetach."""
    if gameplay_screen.player_widgets:
        for widget in gameplay_screen.player_widgets:
            widget.points = player_points.get(widget.player_id, 0)
            widget.lives = player_lives.get(widget.player_id, 0)


def update_active_pawn_indicator():
    """Ustawia flagę `is_active_turn` dla widgetów i pionków."""
    for widget in gameplay_screen.player_widgets:
        widget.set_active(widget.player_id == current_player_id)
    for pawn in all_pawn_objects:
        pawn.set_active(pawn.pawn_id == current_player_id)


def initialize_game_logic_and_pawns():
    """Resetuje logikę gry i inicjalizuje pionki, punkty i życia."""
    global all_sprites_group, pawns_on_fields_map, all_pawn_objects, current_player_id, turn_phase, pawn_that_was_moving, player_points, player_lives, global_turn_counter, professor_move_pending, points_to_animate
    all_sprites_group.empty();
    pawns_on_fields_map.clear();
    all_pawn_objects.clear()
    current_player_id = "player_1";
    turn_phase = 'WAITING_FOR_ROLL';
    pawn_that_was_moving = None
    professor_move_pending = 0;
    global_turn_counter = 0;
    points_to_animate = 0
    player_points = {"player_1": 0, "player_2": 0};
    player_lives = {"player_1": settings.INITIAL_PLAYER_LIVES, "player_2": settings.INITIAL_PLAYER_LIVES}
    update_player_widgets_data()
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
            print("Logika gry, pionki, punkty i życia zainicjalizowane.")
        except Exception as e:
            print(f"Błąd krytyczny podczas inicjalizacji pionków: {e}")
    else:
        print("BŁĄD KRYTYCZNY: game_board_instance nie istnieje.")


def move_professor(steps=1):
    """TYLKO rozpoczyna animację ruchu profesora."""
    global turn_phase, professor_that_was_moving
    professor = next((p for p in all_pawn_objects if p.pawn_id == "professor"), None)
    if professor and gameplay_screen.game_board_instance:
        total_fields = gameplay_screen.game_board_instance.get_total_fields();
        old_prof_index = professor.board_field_index
        path = [(old_prof_index + i + 1) % total_fields for i in range(steps)]
        if not path:
            turn_phase = 'PROCESSING_AFTER_ACTION';
            return
        professor_that_was_moving = professor;
        professor_that_was_moving.start_move_animation(path.copy())
        new_prof_index = path[-1];
        remove_pawn_from_field_map(professor, old_prof_index);
        add_pawn_to_field_map(professor, new_prof_index)
        turn_phase = 'WAITING_FOR_PROFESSOR_MOVE'
        print(f"Profesor rozpoczyna ruch na pole {new_prof_index}")


def check_professor_capture():
    global player_lives;
    professor = next((p for p in all_pawn_objects if p.pawn_id == "professor"), None)
    if not professor: return
    pawns_on_field = get_pawn_objects_on_field(professor.board_field_index)
    for pawn in pawns_on_field:
        if pawn.pawn_id.startswith("player_"):
            if player_lives.get(pawn.pawn_id, 0) > 0:
                player_lives[pawn.pawn_id] -= 1;
                widget_to_shake = next((w for w in gameplay_screen.player_widgets if w.player_id == pawn.pawn_id), None)
                if widget_to_shake: widget_to_shake.start_lose_life_animation()
                print(
                    f"!!! Profesor złapał gracza {pawn.pawn_id}! Gracz traci życie. Pozostało: {player_lives[pawn.pawn_id]}");
                actual_change = add_points_to_player(pawn.pawn_id, -1);
                trigger_points_animation(pawn.pawn_id, actual_change)
                print(f"!!! Gracz {pawn.pawn_id} traci również 1 punkt ECTS.");
                update_player_widgets_data()
                if player_lives[pawn.pawn_id] <= settings.LIVES_TO_LOSE: print(
                    f"!!! Gracz {pawn.pawn_id} stracił wszystkie życia!")


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
    global turn_phase, pawn_that_was_moving;
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


def check_for_game_over():
    global player_points, player_lives
    for i, name in enumerate(final_player_names):
        player_id = f"player_{i + 1}"
        if player_points.get(player_id, 0) >= settings.POINTS_TO_WIN:
            print(f"ZWYCIĘSTWO! Gracz {name} zdobył {settings.POINTS_TO_WIN} ECTS!")
            change_game_state("GAME_OVER", {"id": player_id, "name": name,
                                            "reason": f"Zdobył(a) {settings.POINTS_TO_WIN} punktów ECTS."})
            return True
    loser_id = None
    for player_id, lives in player_lives.items():
        if lives <= settings.LIVES_TO_LOSE:
            loser_id = player_id
            break
    if loser_id:
        try:
            winner_id = "player_2" if loser_id == "player_1" else "player_1"
            loser_name = final_player_names[int(loser_id.split('_')[1]) - 1]
            winner_name = final_player_names[int(winner_id.split('_')[1]) - 1]
            print(f"PORAŻKA! Gracz {loser_name} stracił wszystkie życia! Zwycięża {winner_name}!")
            change_game_state("GAME_OVER",
                              {"id": winner_id, "name": winner_name, "reason": "Przeciwnik stracił wszystkie życia."})
            return True
        except (IndexError, ValueError) as e:
            print(f"Błąd przy ustalaniu zwycięzcy po porażce: {e}")
            change_game_state("GAME_OVER",
                              {"id": None, "name": "Błąd", "reason": "Jeden z graczy stracił wszystkie życia."})
            return True
    return False


def forfeit_game():
    loser_id = current_player_id
    try:
        winner_id = "player_2" if loser_id == "player_1" else "player_1"
        loser_name = final_player_names[int(loser_id.split('_')[1]) - 1]
        winner_name = final_player_names[int(winner_id.split('_')[1]) - 1]
        print(f"!!! PODDANIE GRY! Gracz {loser_name} poddaje grę! Zwycięża {winner_name}! !!!")
        change_game_state("GAME_OVER", {"id": winner_id, "name": winner_name, "reason": "Przeciwnik poddał grę."})
    except (IndexError, ValueError) as e:
        print(f"Błąd podczas poddawania gry: {e}")
        change_game_state("GAME_OVER", {"id": None, "name": "Błąd", "reason": "Jeden z graczy poddał grę."})


def switch_turn():
    global current_player_id, turn_phase, global_turn_counter, professor_move_pending
    if check_for_game_over(): return
    if current_player_id == "player_1":
        current_player_id = "player_2"
    elif current_player_id == "player_2":
        global_turn_counter += 1
        current_player_id = "player_1"
        if global_turn_counter > 0 and global_turn_counter % settings.PROFESSOR_BASE_MOVE_TURN_INTERVAL == 0:
            print(f"Minęły {settings.PROFESSOR_BASE_MOVE_TURN_INTERVAL} tury, profesor musi się ruszyć.")
            professor_move_pending += 1
    print(f"--- Tura numer {global_turn_counter + 1}. Następny: Gracz {current_player_id} ---")
    turn_phase = 'WAITING_FOR_ROLL'
    update_active_pawn_indicator()


def process_player_answer(chosen_answer_index):
    global turn_phase, active_question_card, professor_move_pending, points_to_animate, exam_correct_answers_count
    if not active_question_card: return
    active_question_card.show_result(chosen_answer_index);
    correct_index = active_question_card.question_data["correct_answer_index"]
    if chosen_answer_index == correct_index:
        print("ODPOWIEDŹ POPRAWNA!")
        points_to_animate = settings.POINTS_FOR_EXAM_CORRECT if exam_mode_active else settings.POINTS_FOR_CORRECT_ANSWER
        if exam_mode_active: exam_correct_answers_count += 1
    else:
        print("ODPOWIEDŹ BŁĘDNA!");
        professor_move_pending += 1
        if exam_mode_active: points_to_animate = settings.POINTS_FOR_EXAM_INCORRECT
    turn_phase = 'SHOWING_RESULT_ON_CARD'


def ask_next_exam_question():
    global exam_questions_left, active_question_card, turn_phase
    if exam_questions_left > 0:
        question = question_manager.get_random_question_from_any_subject()
        if question:
            exam_questions_left -= 1;
            subject_name = question.get("original_subject", "EGZAMIN")
            active_question_card = QuestionCard(question, subject_name);
            turn_phase = 'SHOWING_QUESTION'
            print(f"Pytanie egzaminacyjne ({3 - exam_questions_left}/3): {subject_name}")
        else:
            print("Brak więcej pytań w puli! Kończę egzamin."); end_exam_mode()
    else:
        end_exam_mode()


def end_exam_mode():
    global exam_mode_active, turn_phase, player_lives, exam_correct_answers_count
    print("Egzamin zakończony.")
    if exam_correct_answers_count >= 2:
        widget_to_pulse = next((w for w in gameplay_screen.player_widgets if w.player_id == current_player_id), None)
        if player_lives.get(current_player_id, 0) < settings.INITIAL_PLAYER_LIVES:
            if widget_to_pulse: widget_to_pulse.start_gain_life_animation(player_lives[current_player_id])
            player_lives[current_player_id] += 1;
            update_player_widgets_data()
            print(f"GRATULACJE! Gracz {current_player_id} zdobywa dodatkowe życie za zdany egzamin!")
        else:
            print(f"Gracz {current_player_id} zdał egzamin, ale ma już maksymalną liczbę żyć.")
    exam_mode_active = False;
    exam_correct_answers_count = 0;
    turn_phase = 'PROCESSING_AFTER_ACTION'


def handle_field_action():
    global turn_phase, active_question_card, exam_mode_active, exam_questions_left, points_to_animate, exam_correct_answers_count
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
            print("Pole specjalne: EGZAMIN! Czas na 3 pytania.");
            exam_mode_active = True;
            exam_questions_left = 3;
            exam_correct_answers_count = 0;
            ask_next_exam_question()
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
    global turn_phase, pawn_that_was_moving, active_question_card, professor_move_pending, delay_timer, points_to_animate, exam_mode_active, professor_that_was_moving
    all_sprites_group.update(dt_seconds);
    dice_instance.update(dt_seconds)
    if turn_phase == 'DICE_ROLLING' and not dice_instance.is_animating:
        roll_value = dice_instance.get_final_roll_result();
        start_pawn_move(roll_value)
    elif turn_phase == 'PAWN_MOVING' and pawn_that_was_moving and not pawn_that_was_moving.is_moving:
        final_board_index = pawn_that_was_moving.board_field_index;
        total_fields = gameplay_screen.game_board_instance.get_total_fields();
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
            if not active_question_card.is_visible: active_question_card = None; turn_phase = 'PROCESSING_AFTER_ACTION'
    elif turn_phase == 'PROCESSING_AFTER_ACTION':
        any_pawn_moving = next((p for p in all_pawn_objects if p.is_moving or p.is_repositioning), None)
        if not any_pawn_moving:
            if points_to_animate != 0:
                actual_change = add_points_to_player(current_player_id, points_to_animate);
                update_player_widgets_data();
                trigger_points_animation(current_player_id, actual_change);
                points_to_animate = 0
            if check_for_game_over(): return
            if professor_move_pending > 0:
                move_professor(professor_move_pending);
                professor_move_pending = 0
            elif exam_mode_active:
                delay_timer = 0.0;
                turn_phase = 'INTER_QUESTION_DELAY'
            else:
                switch_turn()
    elif turn_phase == 'WAITING_FOR_PROFESSOR_MOVE':
        if professor_that_was_moving and not professor_that_was_moving.is_moving:
            print("Profesor zakończył swój ruch.");
            check_professor_capture();
            start_pawns_repositioning_on_field(professor_that_was_moving.board_field_index);
            professor_that_was_moving = None
            if check_for_game_over(): return
            turn_phase = 'PROCESSING_AFTER_ACTION'
    elif turn_phase == 'INTER_QUESTION_DELAY':
        delay_timer += dt_seconds
        if delay_timer >= settings.INTER_QUESTION_DELAY_SECONDS: ask_next_exam_question()
    elif turn_phase == 'WAITING_FOR_PAWNS':
        any_pawn_moving = next((p for p in all_pawn_objects if p.is_moving or p.is_repositioning), None)
        if not any_pawn_moving:
            if exam_mode_active:
                delay_timer = 0.0; turn_phase = 'INTER_QUESTION_DELAY'
            else:
                switch_turn()