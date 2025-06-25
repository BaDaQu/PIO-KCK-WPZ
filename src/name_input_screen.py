# src/name_input_screen.py
import pygame
from button import Button
import settings
import menu_screen
import sound_manager

# --- Zmienne Modułu ---
player_names_input = ["", ""]
active_input_box_index = 0  # Które pole jest aktywne (0 lub 1)
input_boxes_rects = []
input_font = None
label_font = None
start_game_button = None
error_message = ""
error_message_timer = 0.0
error_message_position = (0, 0)
error_font = None
background_image = None

# --- NOWE ZMIENNE DLA KURSORA I POZYCJI ---
cursor_positions = [0, 0]  # Pozycja kursora (indeks znaku) dla każdego pola
cursor_visible = True
cursor_blink_timer = 0.0


def setup_name_input_screen(screen_width, screen_height):
    """Przygotowuje UI dla ekranu wprowadzania imion."""
    global input_boxes_rects, input_font, label_font, player_names_input, start_game_button, active_input_box_index
    global error_font, error_message, error_message_timer, background_image
    global cursor_positions, cursor_visible, cursor_blink_timer  # Resetuj też te zmienne

    input_boxes_rects = []
    player_names_input = ["", ""]  # Zawsze czyść przy setupie
    active_input_box_index = 0
    cursor_positions = [0, 0]
    cursor_visible = True
    cursor_blink_timer = 0.0
    error_message = "";
    error_message_timer = 0.0

    try:
        img = pygame.image.load(settings.IMAGE_PATH_NAME_INPUT_BG).convert()
        background_image = pygame.transform.scale(img, (screen_width, screen_height))
    except Exception as e:
        print(f"Błąd ładowania tła dla ekranu imion: {e}"); background_image = None
    try:
        input_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.NAME_INPUT_FONT_SIZE)
        label_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.NAME_INPUT_LABEL_FONT_SIZE)
        error_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.NAME_ERROR_FONT_SIZE)
    except Exception as e:
        input_font = pygame.font.SysFont(None, settings.NAME_INPUT_FONT_SIZE + 5);
        label_font = pygame.font.SysFont(None, settings.NAME_INPUT_LABEL_FONT_SIZE + 5);
        error_font = pygame.font.SysFont(None, settings.NAME_ERROR_FONT_SIZE + 2)

    box_width, box_height = settings.NAME_INPUT_BOX_WIDTH, settings.NAME_INPUT_BOX_HEIGHT
    input_box_1_rect = pygame.Rect((screen_width - box_width) // 2, screen_height // 2 - box_height - 30, box_width,
                                   box_height)
    input_boxes_rects.append(input_box_1_rect)
    input_box_2_rect = pygame.Rect((screen_width - box_width) // 2, screen_height // 2 + 50, box_width, box_height)
    input_boxes_rects.append(input_box_2_rect)

    if menu_screen.BUTTON_FONT_MENU:
        start_game_button = Button(
            x=(screen_width - settings.MENU_BUTTON_WIDTH) // 2, y=input_box_2_rect.bottom + 50,
            width=settings.MENU_BUTTON_WIDTH, height=settings.MENU_BUTTON_HEIGHT,
            text="Rozpocznij Wyścig!", font=menu_screen.BUTTON_FONT_MENU,
            base_color=settings.MENU_BUTTON_BASE_COLOR, hover_color=settings.MENU_BUTTON_HOVER_COLOR,
            text_color=settings.MENU_TEXT_COLOR, action="START_FROM_INPUT", border_radius=15
        )


def handle_name_input_events(event, mouse_pos):
    """Obsługuje zdarzenia dla ekranu wprowadzania imion, w tym nawigację klawiaturą."""
    global active_input_box_index, player_names_input, error_message, error_message_timer, error_message_position
    global cursor_positions, cursor_visible, cursor_blink_timer

    if start_game_button:
        action = start_game_button.handle_event(event, mouse_pos)
        if action == "START_FROM_INPUT": sound_manager.play_sound('button_click'); return "START_GAME"

    if event.type == pygame.MOUSEBUTTONDOWN:
        if input_boxes_rects[0].collidepoint(mouse_pos):
            active_input_box_index = 0;
            cursor_visible = True;
            cursor_blink_timer = 0.0;
            sound_manager.play_sound('button_click')
        elif input_boxes_rects[1].collidepoint(mouse_pos):
            active_input_box_index = 1;
            cursor_visible = True;
            cursor_blink_timer = 0.0;
            sound_manager.play_sound('button_click')

    if event.type == pygame.KEYDOWN:
        if active_input_box_index is not None:  # Jeśli któreś pole jest aktywne
            cursor_visible = True  # Pokaż kursor przy każdym naciśnięciu klawisza
            cursor_blink_timer = 0.0  # Zresetuj timer migania
            current_text = player_names_input[active_input_box_index]
            current_cursor_pos = cursor_positions[active_input_box_index]

            if event.key == pygame.K_BACKSPACE:
                if current_cursor_pos > 0:
                    player_names_input[active_input_box_index] = current_text[:current_cursor_pos - 1] + current_text[
                                                                                                         current_cursor_pos:]
                    cursor_positions[active_input_box_index] -= 1
                sound_manager.play_sound('backspace')
            elif event.key == pygame.K_DELETE:
                if current_cursor_pos < len(current_text):
                    player_names_input[active_input_box_index] = current_text[:current_cursor_pos] + current_text[
                                                                                                     current_cursor_pos + 1:]
                    # Pozycja kursora nie zmienia się
                sound_manager.play_sound('backspace')  # Podobny dźwięk
            elif event.key == pygame.K_LEFT:
                cursor_positions[active_input_box_index] = max(0, current_cursor_pos - 1)
                sound_manager.play_sound('typing')  # Dźwięk ruchu kursora
            elif event.key == pygame.K_RIGHT:
                cursor_positions[active_input_box_index] = min(len(current_text), current_cursor_pos + 1)
                sound_manager.play_sound('typing')
            elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                sound_manager.play_sound('button_click')
                return "START_GAME"
            elif event.key == pygame.K_UP or (event.key == pygame.K_TAB and pygame.key.get_mods() & pygame.KMOD_SHIFT):
                active_input_box_index = (active_input_box_index - 1 + len(input_boxes_rects)) % len(input_boxes_rects)
                cursor_positions[active_input_box_index] = min(cursor_positions[active_input_box_index], len(
                    player_names_input[active_input_box_index]))  # Ustaw kursor na końcu
                sound_manager.play_sound('pawn_move')
            elif event.key == pygame.K_DOWN or event.key == pygame.K_TAB:
                active_input_box_index = (active_input_box_index + 1) % len(input_boxes_rects)
                cursor_positions[active_input_box_index] = min(cursor_positions[active_input_box_index],
                                                               len(player_names_input[active_input_box_index]))
                sound_manager.play_sound('pawn_move')
            elif event.unicode.isprintable():
                if len(current_text) < settings.MAX_PLAYER_NAME_LENGTH:
                    player_names_input[active_input_box_index] = current_text[
                                                                 :current_cursor_pos] + event.unicode + current_text[
                                                                                                        current_cursor_pos:]
                    cursor_positions[active_input_box_index] += 1
                    sound_manager.play_sound('typing')
                else:
                    sound_manager.play_sound('wrong')
                    error_message = f"Maks. {settings.MAX_PLAYER_NAME_LENGTH} znaków."
                    error_message_timer = settings.NAME_ERROR_DURATION_SECONDS
                    active_box_rect = input_boxes_rects[active_input_box_index]
                    error_message_position = (active_box_rect.centerx,
                                              active_box_rect.bottom + settings.NAME_ERROR_Y_OFFSET)
    return None


def draw_name_input_screen(surface, screen_width, screen_height, mouse_pos, dt_seconds):
    global error_message, error_message_timer, cursor_visible, cursor_blink_timer

    if background_image:
        surface.blit(background_image, (0, 0))
    else:
        surface.fill(settings.MENU_BG_FALLBACK_COLOR)

    if menu_screen.TITLE_FONT_MENU:
        prompt_text = menu_screen.TITLE_FONT_MENU.render("Wprowadź Imiona", True, settings.MENU_TEXT_COLOR)
        prompt_rect = prompt_text.get_rect(center=(screen_width // 2, screen_height // 4))
        surface.blit(prompt_text, prompt_rect)

    # Miganie kursora
    cursor_blink_timer += dt_seconds
    if cursor_blink_timer >= settings.NAME_INPUT_CURSOR_BLINK_INTERVAL_SECONDS:
        cursor_visible = not cursor_visible
        cursor_blink_timer -= settings.NAME_INPUT_CURSOR_BLINK_INTERVAL_SECONDS

    for i, box in enumerate(input_boxes_rects):
        pygame.draw.rect(surface, settings.MENU_BUTTON_BASE_COLOR, box, border_radius=5)
        text_surface = input_font.render(player_names_input[i], True, settings.MENU_TEXT_COLOR)
        text_render_pos_y = box.y + (box.height - text_surface.get_height()) // 2
        surface.blit(text_surface, (box.x + 15, text_render_pos_y))

        if i == active_input_box_index:
            pygame.draw.rect(surface, settings.WHITE, box, 4, border_radius=5)  # Aktywne pole
            if cursor_visible:
                # Oblicz pozycję X kursora
                text_before_cursor = player_names_input[i][:cursor_positions[i]]
                cursor_x_offset = input_font.size(text_before_cursor)[0]
                cursor_pos_x = box.x + 15 + cursor_x_offset
                cursor_pos_y1 = text_render_pos_y
                cursor_pos_y2 = text_render_pos_y + text_surface.get_height()
                pygame.draw.line(surface, settings.NAME_INPUT_CURSOR_COLOR,
                                 (cursor_pos_x, cursor_pos_y1),
                                 (cursor_pos_x, cursor_pos_y2), settings.NAME_INPUT_CURSOR_WIDTH)

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