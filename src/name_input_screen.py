# src/name_input_screen.py
import pygame
from button import Button
import settings
import menu_screen

# --- Zmienne Modułu ---
player_names_input = ["", ""]
active_input_box_index = 0
input_boxes_rects = []
input_font = None
label_font = None
start_game_button = None
error_message = ""
error_message_timer = 0.0
error_message_position = (0, 0)
error_font = None

def setup_name_input_screen(screen_width, screen_height):
    global input_boxes_rects, input_font, label_font, player_names_input, start_game_button, active_input_box_index, error_font, error_message, error_message_timer
    input_boxes_rects = []; player_names_input = ["", ""]; active_input_box_index = 0
    error_message = ""; error_message_timer = 0.0
    try:
        input_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.NAME_INPUT_FONT_SIZE)
        label_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.NAME_INPUT_LABEL_FONT_SIZE)
        error_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.NAME_ERROR_FONT_SIZE)
    except Exception as e:
        print(f"Błąd ładowania czcionek dla ekranu imion: {e}")
        input_font = pygame.font.SysFont(None, settings.NAME_INPUT_FONT_SIZE + 5)
        label_font = pygame.font.SysFont(None, settings.NAME_INPUT_LABEL_FONT_SIZE + 5)
        error_font = pygame.font.SysFont(None, settings.NAME_ERROR_FONT_SIZE + 2)

    box_width, box_height = settings.NAME_INPUT_BOX_WIDTH, settings.NAME_INPUT_BOX_HEIGHT
    input_box_1_rect = pygame.Rect((screen_width - box_width) // 2, screen_height // 2 - box_height - 30, box_width, box_height)
    input_boxes_rects.append(input_box_1_rect)
    input_box_2_rect = pygame.Rect((screen_width - box_width) // 2, screen_height // 2 + 50, box_width, box_height)
    input_boxes_rects.append(input_box_2_rect)
    start_game_button = Button(
        x=(screen_width - settings.MENU_BUTTON_WIDTH) // 2, y=input_box_2_rect.bottom + 50,
        width=settings.MENU_BUTTON_WIDTH, height=settings.MENU_BUTTON_HEIGHT,
        text="Rozpocznij Wyścig!", font=menu_screen.BUTTON_FONT_MENU,
        base_color=settings.MENU_BUTTON_BASE_COLOR, hover_color=settings.MENU_BUTTON_HOVER_COLOR,
        text_color=settings.MENU_TEXT_COLOR, action="START_FROM_INPUT", border_radius=15
    )

def handle_name_input_events(event, mouse_pos):
    global active_input_box_index, player_names_input, error_message, error_message_timer, error_message_position
    if start_game_button:
        action = start_game_button.handle_event(event, mouse_pos)
        if action == "START_FROM_INPUT": return "START_GAME"
    if event.type == pygame.MOUSEBUTTONDOWN:
        if input_boxes_rects[0].collidepoint(mouse_pos): active_input_box_index = 0
        elif input_boxes_rects[1].collidepoint(mouse_pos): active_input_box_index = 1
    if event.type == pygame.KEYDOWN:
        if active_input_box_index is not None:
            if event.key == pygame.K_BACKSPACE:
                player_names_input[active_input_box_index] = player_names_input[active_input_box_index][:-1]
            elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                return "START_GAME"
            elif event.key == pygame.K_TAB:
                active_input_box_index = (active_input_box_index + 1) % 2
            else:
                if len(player_names_input[active_input_box_index]) < settings.MAX_PLAYER_NAME_LENGTH:
                    player_names_input[active_input_box_index] += event.unicode
                else:
                    error_message = f"Maksymalna długość imienia to {settings.MAX_PLAYER_NAME_LENGTH} znaków."
                    error_message_timer = settings.NAME_ERROR_DURATION_SECONDS
                    active_box_rect = input_boxes_rects[active_input_box_index]
                    error_message_position = (active_box_rect.centerx, active_box_rect.bottom + settings.NAME_ERROR_Y_OFFSET)
    return None

def draw_name_input_screen(surface, screen_width, screen_height, mouse_pos, dt_seconds):
    global error_message, error_message_timer
    surface.fill(settings.MENU_BG_FALLBACK_COLOR)
    if menu_screen.TITLE_FONT_MENU:
        prompt_text = menu_screen.TITLE_FONT_MENU.render("Wprowadź Imiona", True, settings.MENU_TEXT_COLOR)
        prompt_rect = prompt_text.get_rect(center=(screen_width // 2, screen_height // 4))
        surface.blit(prompt_text, prompt_rect)
    for i, box in enumerate(input_boxes_rects):
        # PRZYWRÓCONY WYGLĄD POLA TEKSTOWEGO
        pygame.draw.rect(surface, settings.MENU_BUTTON_BASE_COLOR, box, border_radius=5)
        if i == active_input_box_index:
            pygame.draw.rect(surface, settings.WHITE, box, 4, border_radius=5)
        # -------------------------------------
        text_surface = input_font.render(player_names_input[i], True, settings.MENU_TEXT_COLOR)
        surface.blit(text_surface, (box.x + 15, box.y + (box.height - text_surface.get_height()) // 2))
        label_text = f"Imię Gracza {i + 1}:"
        label_surface = label_font.render(label_text, True, settings.MENU_TEXT_COLOR)
        label_x_pos = box.x + settings.NAME_INPUT_LABEL_X_OFFSET
        label_y_pos = box.y + settings.NAME_INPUT_LABEL_Y_OFFSET
        surface.blit(label_surface, (label_x_pos, label_y_pos))
    if error_message_timer > 0:
        error_message_timer -= dt_seconds
        if error_message_timer <= 0:
            error_message = ""
        else:
            if error_font:
                error_surface = error_font.render(error_message, True, settings.NAME_ERROR_COLOR)
                error_rect = error_surface.get_rect(center=error_message_position)
                surface.blit(error_surface, error_rect)
    if start_game_button:
        start_game_button.update_hover(mouse_pos)
        start_game_button.draw(surface)