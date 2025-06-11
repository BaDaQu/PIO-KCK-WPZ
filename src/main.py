# src/main.py
import pygame
import sys
import menu_screen
import gameplay_screen
from pawn import PlayerPawn, ProfessorPawn
from dice import Dice
import settings

pygame.init()

# Używamy stałych z settings.py
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

# Zmienne Globalne Gry
player_pawns_group = pygame.sprite.Group()
professor_pawn_group = pygame.sprite.Group()
all_sprites_group = pygame.sprite.Group()
pawns_on_fields_map = {}
all_pawn_objects = []

dice_instance = Dice(
    initial_x_center=settings.LEFT_PANEL_WIDTH // 2, # Początkowe x, gameplay_screen może to dostosować
    initial_y_bottom_of_image=settings.GAMEPLAY_SCREEN_HEIGHT - 200, # Początkowe y
    dice_images_base_path=settings.DICE_IMAGES_BASE_PATH,
    font_path=settings.FONT_PATH_PT_SERIF_REGULAR, # Przekazujemy ścieżkę do czcionki
    font_size=settings.DICE_BUTTON_FONT_SIZE      # Przekazujemy rozmiar czcionki
)

clock = pygame.time.Clock()
game_state = "MENU_GLOWNE"
current_player_id = "player_1"
dice_action_taken_this_turn = False


def set_screen_mode(width, height):
    global screen, current_screen_width, current_screen_height
    current_screen_width = width
    current_screen_height = height
    screen = pygame.display.set_mode((current_screen_width, current_screen_height))
    print(f"Tryb ekranu zmieniony na: {width}x{height}")

    if game_state == "MENU_GLOWNE":
        menu_screen.load_menu_resources(current_screen_width, current_screen_height)
        menu_screen.setup_menu_ui_elements(current_screen_width, current_screen_height)
    elif game_state == "GAMEPLAY":
        gameplay_screen.load_gameplay_resources(current_screen_width, current_screen_height)
        gameplay_screen.setup_gameplay_ui_elements(current_screen_height)
        initialize_pawns()
    elif game_state == "INSTRUCTIONS":
        menu_screen.load_menu_resources(current_screen_width, current_screen_height)


def initialize_pawns():
    global player_pawns_group, professor_pawn_group, all_sprites_group, pawns_on_fields_map, all_pawn_objects, current_player_id, dice_action_taken_this_turn
    player_pawns_group.empty(); professor_pawn_group.empty(); all_sprites_group.empty()
    pawns_on_fields_map.clear(); all_pawn_objects.clear()
    current_player_id = "player_1"
    dice_action_taken_this_turn = False

    if gameplay_screen.game_board_instance:
        try:
            player1 = PlayerPawn(player_id=1, image_path=settings.IMAGE_PATH_PLAYER1_PAWN,
                                 initial_board_field_index=0, board_ref=gameplay_screen.game_board_instance)
            add_pawn_to_field_map(player1, 0)
            player_pawns_group.add(player1); all_sprites_group.add(player1); all_pawn_objects.append(player1)

            player2 = PlayerPawn(player_id=2, image_path=settings.IMAGE_PATH_PLAYER2_PAWN,
                                 initial_board_field_index=0, board_ref=gameplay_screen.game_board_instance)
            add_pawn_to_field_map(player2, 0)
            player_pawns_group.add(player2); all_sprites_group.add(player2); all_pawn_objects.append(player2)

            professor = ProfessorPawn(image_path=settings.IMAGE_PATH_PROFESSOR_PAWN,
                                      initial_board_field_index=0, board_ref=gameplay_screen.game_board_instance)
            add_pawn_to_field_map(professor, 0)
            professor_pawn_group.add(professor); all_sprites_group.add(professor); all_pawn_objects.append(professor)

            update_all_pawn_visual_positions()
            print("Pionki zainicjalizowane.")
        except Exception as e:
            print(f"Błąd krytyczny podczas inicjalizacji pionków: {e}")
    else:
        print("BŁĄD: Nie można zainicjalizować pionków - game_board_instance nie istnieje.")

# Funkcje add_pawn_to_field_map, remove_pawn_from_field_map, get_pawn_objects_on_field,
# update_all_pawn_visual_positions, move_pawn_to_new_index POZOSTAJĄ BEZ ZMIAN W LOGICE
# (tak jak w Twojej ostatniej wersji - ważne, aby działały poprawnie)
def add_pawn_to_field_map(pawn_obj, field_index):
    if field_index not in pawns_on_fields_map: pawns_on_fields_map[field_index] = []
    if pawn_obj not in pawns_on_fields_map[field_index]: pawns_on_fields_map[field_index].append(pawn_obj)

def remove_pawn_from_field_map(pawn_obj_to_remove, field_index):
    if field_index in pawns_on_fields_map:
        pawns_on_fields_map[field_index] = [p for p in pawns_on_fields_map[field_index] if p.pawn_id != pawn_obj_to_remove.pawn_id]
        if not pawns_on_fields_map[field_index]: del pawns_on_fields_map[field_index]

def get_pawn_objects_on_field(field_index): return pawns_on_fields_map.get(field_index, [])

def update_all_pawn_visual_positions():
    occupied_fields = list(pawns_on_fields_map.keys())
    for field_idx in occupied_fields:
        pawn_objects_on_field = get_pawn_objects_on_field(field_idx)
        pawn_ids_on_field = [p.pawn_id for p in pawn_objects_on_field]
        for pawn_obj in pawn_objects_on_field:
            pawn_obj.update_position_on_board_with_sharing(pawn_obj.board_field_index, pawn_ids_on_field)

def move_pawn_to_new_index(pawn_id_to_move, new_board_index):
    pawn_to_move = next((p for p in all_pawn_objects if p.pawn_id == pawn_id_to_move), None)
    if not pawn_to_move: print(f"Błąd: Nie znaleziono pionka {pawn_id_to_move}"); return
    old_board_index = pawn_to_move.board_field_index
    if old_board_index == new_board_index: return
    remove_pawn_from_field_map(pawn_to_move, old_board_index)
    add_pawn_to_field_map(pawn_to_move, new_board_index)
    pawn_to_move.board_field_index = new_board_index
    update_all_pawn_visual_positions()
    print(f"Pionek {pawn_id_to_move} przesunięty z pola {old_board_index} na pole {new_board_index}")


running = True
while running:
    dt = clock.tick(settings.FPS) # Użyj stałej FPS
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "MENU_GLOWNE":
            action = menu_screen.handle_menu_input(event, mouse_pos)
            if action:
                if action == "GAMEPLAY":
                    game_state = "GAMEPLAY"
                    if current_screen_width != settings.GAMEPLAY_SCREEN_WIDTH or current_screen_height != settings.GAMEPLAY_SCREEN_HEIGHT:
                        set_screen_mode(settings.GAMEPLAY_SCREEN_WIDTH, settings.GAMEPLAY_SCREEN_HEIGHT)
                    else:
                        gameplay_screen.load_gameplay_resources(current_screen_width, current_screen_height)
                        gameplay_screen.setup_gameplay_ui_elements(current_screen_height)
                        initialize_pawns()
                elif action == "INSTRUCTIONS":
                    game_state = "INSTRUCTIONS"
                    if current_screen_width != settings.INITIAL_SCREEN_WIDTH or current_screen_height != settings.INITIAL_SCREEN_HEIGHT:
                        set_screen_mode(settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT)
                elif action == "QUIT":
                    running = False

        elif game_state == "GAMEPLAY":
            gameplay_action = gameplay_screen.handle_gameplay_input(event, mouse_pos)
            if gameplay_action == "ROLL_DICE_PANEL":
                if not dice_instance.is_animating and not dice_action_taken_this_turn:
                    dice_instance.start_animation_and_roll()
                    dice_action_taken_this_turn = True
                    print(f"Gracz {current_player_id} KLIKNĄŁ RZUT (panel).")
            elif gameplay_action == "BACK_TO_MENU":
                game_state = "MENU_GLOWNE"
                if current_screen_width != settings.INITIAL_SCREEN_WIDTH or current_screen_height != settings.INITIAL_SCREEN_HEIGHT:
                    set_screen_mode(settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT)

        elif game_state == "INSTRUCTIONS":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game_state = "MENU_GLOWNE"
                if current_screen_width != settings.INITIAL_SCREEN_WIDTH or current_screen_height != settings.INITIAL_SCREEN_HEIGHT:
                    set_screen_mode(settings.INITIAL_SCREEN_WIDTH, settings.INITIAL_SCREEN_HEIGHT)

    # Aktualizacja Logiki
    if game_state == "GAMEPLAY":
        all_sprites_group.update()
        gameplay_screen.update_gameplay_state()
        dice_instance.update(dt)

        if dice_action_taken_this_turn and not dice_instance.is_animating:
            roll_value = dice_instance.get_final_roll_result()
            print(f"Gracz {current_player_id} wyrzucił: {roll_value}")

            pawn_to_move = next((p for p in all_pawn_objects if p.pawn_id == current_player_id), None)
            if pawn_to_move and gameplay_screen.game_board_instance:
                total_fields = gameplay_screen.game_board_instance.get_total_fields()
                if total_fields > 0:
                    new_idx = (pawn_to_move.board_field_index + roll_value) % total_fields
                    move_pawn_to_new_index(pawn_to_move.pawn_id, new_idx)

                    if current_player_id == "player_1": current_player_id = "player_2"
                    elif current_player_id == "player_2": current_player_id = "player_1"
                    print(f"Następna tura: Gracz {current_player_id}")
                    dice_action_taken_this_turn = False
            else:
                dice_action_taken_this_turn = False

    # Rysowanie
    screen.fill(settings.DEFAULT_BG_COLOR)

    if game_state == "MENU_GLOWNE":
        menu_screen.draw_menu_screen(screen, current_screen_width, current_screen_height, mouse_pos)
    elif game_state == "GAMEPLAY":
        gameplay_screen.draw_gameplay_screen(screen, mouse_pos, dice_instance)
        all_sprites_group.draw(screen)
    elif game_state == "INSTRUCTIONS":
        # Rysowanie ekranu instrukcji (uproszczone)
        if menu_screen.TITLE_FONT_MENU and menu_screen.BUTTON_FONT_MENU: # Użyj czcionek z menu
            screen.fill(settings.MENU_BG_FALLBACK_COLOR) # Możesz dać inne tło dla instrukcji
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
        else: # Fallback, jeśli czcionki menu nie są dostępne
            fallback_font = pygame.font.SysFont(None, 30)
            info_text = fallback_font.render("(Kliknij, aby wrócić)", True, settings.WHITE)
            screen.blit(info_text, (50,50))


    pygame.display.flip()

pygame.quit()
sys.exit()