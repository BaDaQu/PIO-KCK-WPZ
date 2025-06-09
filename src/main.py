# src/main.py
import pygame
import sys
import menu_screen
import gameplay_screen
from pawn import PlayerPawn, ProfessorPawn

pygame.init()

INITIAL_SCREEN_WIDTH = 1436
INITIAL_SCREEN_HEIGHT = 1024
SCREEN_TITLE = "Wyścig po Zaliczenie"
GAMEPLAY_SCREEN_WIDTH = 1436
GAMEPLAY_SCREEN_HEIGHT = 1024

current_screen_width = INITIAL_SCREEN_WIDTH
current_screen_height = INITIAL_SCREEN_HEIGHT

pygame.display.set_caption(SCREEN_TITLE)
screen = pygame.display.set_mode((current_screen_width, current_screen_height))

FONT_PATH = "../assets/fonts/PTSerif-Regular.ttf"
MENU_BG_PATH = "../assets/images/MENU_GLOWNE.png"
ICON_PATH = "../assets/images/IKONA_GRY.png"
LEFT_PANEL_BG_PATH = "../assets/images/GAMEBOARD_LEFT_PANEL.png"

PLAYER_PAWN_IMAGE_PATH = "../assets/images/PIONEK_STUDENT.png"
PLAYER2_PAWN_IMAGE_PATH = "../assets/images/PIONEK_STUDENT.png"
PROFESSOR_PAWN_IMAGE_PATH = "../assets/images/PIONEK_PROFESOR.png"

try:
    game_icon = pygame.image.load(ICON_PATH)
    pygame.display.set_icon(game_icon)
except Exception as e:
    print(f"Błąd ładowania ikony: {e}")

menu_screen.load_menu_resources(current_screen_width, current_screen_height, FONT_PATH, FONT_PATH, MENU_BG_PATH)
menu_screen.setup_menu_ui_elements(current_screen_width, current_screen_height)

player_pawns_group = pygame.sprite.Group()
professor_pawn_group = pygame.sprite.Group()
all_sprites_group = pygame.sprite.Group()

pawns_on_fields_map = {}
all_pawn_objects = []

player1_next_move_amount = 2
player2_next_move_amount = 1
test_move_turn_counter = 0

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
        gameplay_screen.setup_gameplay_ui_elements(current_screen_height)
        initialize_pawns()
    elif game_state == "INSTRUCTIONS":
        menu_screen.load_menu_resources(current_screen_width, current_screen_height, FONT_PATH, FONT_PATH, MENU_BG_PATH)


def initialize_pawns():
    global player_pawns_group, professor_pawn_group, all_sprites_group, pawns_on_fields_map, all_pawn_objects
    global player1_next_move_amount, player2_next_move_amount, test_move_turn_counter  # Resetuj też te zmienne

    player_pawns_group.empty()
    professor_pawn_group.empty()
    all_sprites_group.empty()
    pawns_on_fields_map.clear()
    all_pawn_objects.clear()

    # Reset zmiennych testowego ruchu
    player1_next_move_amount = 2
    player2_next_move_amount = 1
    test_move_turn_counter = 0

    if gameplay_screen.game_board_instance:
        try:
            player1_start_field = 0
            player1 = PlayerPawn(player_id=1,
                                 image_path=PLAYER_PAWN_IMAGE_PATH,
                                 initial_board_field_index=player1_start_field,
                                 board_ref=gameplay_screen.game_board_instance)
            add_pawn_to_field_map(player1, player1_start_field)
            all_pawn_objects.append(player1)
            player_pawns_group.add(player1)
            all_sprites_group.add(player1)

            player2_start_field = 0
            player2 = PlayerPawn(player_id=2,
                                 image_path=PLAYER2_PAWN_IMAGE_PATH,
                                 initial_board_field_index=player2_start_field,
                                 board_ref=gameplay_screen.game_board_instance)
            add_pawn_to_field_map(player2, player2_start_field)
            all_pawn_objects.append(player2)
            player_pawns_group.add(player2)
            all_sprites_group.add(player2)

            professor_start_field = 0
            professor = ProfessorPawn(image_path=PROFESSOR_PAWN_IMAGE_PATH,
                                      initial_board_field_index=professor_start_field,
                                      board_ref=gameplay_screen.game_board_instance)
            add_pawn_to_field_map(professor, professor_start_field)
            all_pawn_objects.append(professor)
            professor_pawn_group.add(professor)
            all_sprites_group.add(professor)

            update_all_pawn_visual_positions()
            print("Pionki zainicjalizowane i pozycje zaktualizowane.")
        except Exception as e:
            print(f"Błąd krytyczny podczas inicjalizacji pionków: {e}")
    else:
        print("BŁĄD: Nie można zainicjalizować pionków - instancja planszy nie istnieje.")


def add_pawn_to_field_map(pawn_obj, field_index):
    if field_index not in pawns_on_fields_map:
        pawns_on_fields_map[field_index] = []
    if pawn_obj.pawn_id not in pawns_on_fields_map[field_index]:
        pawns_on_fields_map[field_index].append(pawn_obj.pawn_id)


def remove_pawn_from_field_map(pawn_obj_id, field_index):
    if field_index in pawns_on_fields_map and pawn_obj_id in pawns_on_fields_map[field_index]:
        pawns_on_fields_map[field_index].remove(pawn_obj_id)
        if not pawns_on_fields_map[field_index]:
            del pawns_on_fields_map[field_index]


def get_pawn_ids_on_field(field_index):
    return pawns_on_fields_map.get(field_index, [])


def update_all_pawn_visual_positions():
    for pawn_obj in all_pawn_objects:
        pawn_ids_on_current_field = get_pawn_ids_on_field(pawn_obj.board_field_index)
        pawn_obj.update_position_on_board_with_sharing(pawn_obj.board_field_index, pawn_ids_on_current_field,
                                                       all_pawn_objects)


def move_pawn_logic(pawn_to_move_id, new_field_index):
    pawn_obj_to_move = next((p for p in all_pawn_objects if p.pawn_id == pawn_to_move_id), None)
    if not pawn_obj_to_move:
        print(f"BŁĄD: Nie znaleziono pionka o ID {pawn_to_move_id}")
        return

    old_field_index = pawn_obj_to_move.board_field_index
    if old_field_index == new_field_index:
        return

    remove_pawn_from_field_map(pawn_obj_to_move.pawn_id, old_field_index)
    add_pawn_to_field_map(pawn_obj_to_move, new_field_index)
    pawn_obj_to_move.board_field_index = new_field_index

    update_all_pawn_visual_positions()


running = True
move_timer = 0
move_interval = 2000

while running:
    dt = clock.tick(FPS)
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
                    else:
                        gameplay_screen.load_gameplay_resources(current_screen_width, current_screen_height, FONT_PATH,
                                                                LEFT_PANEL_BG_PATH)
                        gameplay_screen.setup_gameplay_ui_elements(current_screen_height)
                        initialize_pawns()  # Upewnij się, że pionki są inicjalizowane
                    # Resetuj zmienne testowego ruchu przy starcie/restarcie gameplay
                    player1_next_move_amount = 2
                    player2_next_move_amount = 1
                    test_move_turn_counter = 0
                    move_timer = 0
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

        elif game_state == "INSTRUCTIONS":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game_state = "MENU_GLOWNE"
                    if current_screen_width != INITIAL_SCREEN_WIDTH or current_screen_height != INITIAL_SCREEN_HEIGHT:
                        set_screen_mode(INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT)

    if game_state == "GAMEPLAY":
        all_sprites_group.update()
        gameplay_screen.update_gameplay_state()

        move_timer += dt
        if move_timer >= move_interval:
            move_timer = 0
            test_move_turn_counter += 1

            if gameplay_screen.game_board_instance:
                total_fields = gameplay_screen.game_board_instance.get_total_fields()
                if total_fields > 0:

                    player1 = next((p for p in all_pawn_objects if p.pawn_id == "player_1"), None)
                    if player1:
                        new_idx_p1 = (player1.board_field_index + player1_next_move_amount) % total_fields
                        move_pawn_logic(player1.pawn_id, new_idx_p1)
                        player1_next_move_amount = 1 if player1_next_move_amount == 2 else 2

                    player2 = next((p for p in all_pawn_objects if p.pawn_id == "player_2"), None)
                    if player2:
                        new_idx_p2 = (player2.board_field_index + player2_next_move_amount) % total_fields
                        move_pawn_logic(player2.pawn_id, new_idx_p2)
                        player2_next_move_amount = 2 if player2_next_move_amount == 1 else 1

                    if test_move_turn_counter > 1:
                        professor = next((p for p in all_pawn_objects if p.pawn_id == "professor"), None)
                        if professor:
                            new_idx_prof = (professor.board_field_index + 1) % total_fields
                            move_pawn_logic(professor.pawn_id, new_idx_prof)

                    # print(f"Test: Tura ruchu {test_move_turn_counter}. Pionki przesunięte.")

    default_bg_color = menu_screen.BLACK if hasattr(menu_screen, 'BLACK') and menu_screen.BLACK else (0, 0, 0)
    screen.fill(default_bg_color)

    if game_state == "MENU_GLOWNE":
        menu_screen.draw_menu_screen(screen, current_screen_width, current_screen_height, mouse_pos)
    elif game_state == "GAMEPLAY":
        gameplay_screen.draw_gameplay_screen(screen, mouse_pos)
        all_sprites_group.draw(screen)
    elif game_state == "INSTRUCTIONS":
        instr_white = menu_screen.WHITE if hasattr(menu_screen, 'WHITE') and menu_screen.WHITE else (255, 255, 255)
        if hasattr(menu_screen, 'TITLE_FONT') and menu_screen.TITLE_FONT:
            title_instr = menu_screen.TITLE_FONT.render("Instrukcja", True, instr_white)
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
                line_surface = menu_screen.BUTTON_FONT.render(line, True, instr_white)
                line_rect = line_surface.get_rect(center=(current_screen_width // 2, line_y_offset + i * 45))
                screen.blit(line_surface, line_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()