# src/name_input_screen.py
import pygame
from button import Button
import settings
import menu_screen  # Potrzebne do czcionki przycisku "Graj!"

# --- Zmienne Modułu ---
player_names_input = ["", ""]
active_input_box_index = 0
input_boxes_rects = []
input_font = None
label_font = None
start_game_button = None


def setup_name_input_screen(screen_width, screen_height):
    """Przygotowuje UI dla ekranu wprowadzania imion."""
    global input_boxes_rects, input_font, label_font, player_names_input, start_game_button, active_input_box_index
    input_boxes_rects = []
    player_names_input = ["", ""]
    active_input_box_index = 0
    try:
        input_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.NAME_INPUT_FONT_SIZE)
        label_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.NAME_INPUT_LABEL_FONT_SIZE)
    except Exception as e:
        input_font = pygame.font.SysFont(None, settings.NAME_INPUT_FONT_SIZE + 5)
        label_font = pygame.font.SysFont(None, settings.NAME_INPUT_LABEL_FONT_SIZE + 5)

    box_width, box_height = settings.NAME_INPUT_BOX_WIDTH, settings.NAME_INPUT_BOX_HEIGHT

    input_box_1_rect = pygame.Rect((screen_width - box_width) // 2, screen_height // 2 - box_height - 30, box_width,
                                   box_height)
    input_boxes_rects.append(input_box_1_rect)

    input_box_2_rect = pygame.Rect((screen_width - box_width) // 2, screen_height // 2 + 50, box_width, box_height)
    input_boxes_rects.append(input_box_2_rect)

    start_game_button = Button(
        x=(screen_width - settings.MENU_BUTTON_WIDTH) // 2,
        y=input_box_2_rect.bottom + 50,
        width=settings.MENU_BUTTON_WIDTH, height=settings.MENU_BUTTON_HEIGHT,
        text="Rozpocznij Wyścig!", font=menu_screen.BUTTON_FONT_MENU,
        base_color=settings.MENU_BUTTON_BASE_COLOR, hover_color=settings.MENU_BUTTON_HOVER_COLOR,
        text_color=settings.MENU_TEXT_COLOR, action="START_FROM_INPUT", border_radius=15
    )


def handle_name_input_events(event, mouse_pos):
    """Obsługuje zdarzenia dla ekranu wprowadzania imion."""
    global active_input_box_index, player_names_input, start_game_button

    if start_game_button:
        action = start_game_button.handle_event(event, mouse_pos)
        if action == "START_FROM_INPUT":
            return "START_GAME"

    if event.type == pygame.MOUSEBUTTONDOWN:
        if input_boxes_rects[0].collidepoint(mouse_pos):
            active_input_box_index = 0
        elif input_boxes_rects[1].collidepoint(mouse_pos):
            active_input_box_index = 1

    if event.type == pygame.KEYDOWN:
        if active_input_box_index is not None:
            if event.key == pygame.K_BACKSPACE:
                player_names_input[active_input_box_index] = player_names_input[active_input_box_index][:-1]
            elif event.key == pygame.K_RETURN:
                return "START_GAME"
            elif event.key == pygame.K_TAB:
                active_input_box_index = (active_input_box_index + 1) % 2
            else:
                player_names_input[active_input_box_index] += event.unicode
    return None


def draw_name_input_screen(surface, screen_width, screen_height, mouse_pos):
    """Rysuje ekran wprowadzania imion."""
    surface.fill(settings.MENU_BG_FALLBACK_COLOR)

    if menu_screen.TITLE_FONT_MENU:
        prompt_text = menu_screen.TITLE_FONT_MENU.render("Wprowadź Imiona", True, settings.MENU_TEXT_COLOR)
        prompt_rect = prompt_text.get_rect(center=(screen_width // 2, screen_height // 4))
        surface.blit(prompt_text, prompt_rect)

    for i, box in enumerate(input_boxes_rects):
        pygame.draw.rect(surface, settings.MENU_BUTTON_BASE_COLOR, box, border_radius=5)

        if i == active_input_box_index:
            pygame.draw.rect(surface, settings.WHITE, box, 4, border_radius=5)

        text_surface = input_font.render(player_names_input[i], True, settings.MENU_TEXT_COLOR)
        surface.blit(text_surface, (box.x + 15, box.y + (box.height - text_surface.get_height()) // 2))

        # === ZMODYFIKOWANY FRAGMENT Z UŻYCIEM NOWYCH STAŁYCH ===
        label_text = f"Imię Gracza {i + 1}:"
        label_surface = label_font.render(label_text, True, settings.MENU_TEXT_COLOR)

        # Pozycjonujemy etykietę z uwzględnieniem offsetu X i Y z pliku settings
        label_x_pos = box.x + settings.NAME_INPUT_LABEL_X_OFFSET
        label_y_pos = box.y + settings.NAME_INPUT_LABEL_Y_OFFSET
        surface.blit(label_surface, (label_x_pos, label_y_pos))
        # =======================================================

    if start_game_button:
        start_game_button.update_hover(mouse_pos)
        start_game_button.draw(surface)