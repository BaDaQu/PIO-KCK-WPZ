# src/gameplay_screen.py
import pygame
from board_screen import Board
from button import Button
from player_widget import PlayerInfoWidget
import settings

# --- Zmienne Globalne Modułu ---
game_board_instance = None
left_panel_background_img = None
info_font = None
button_font_gameplay = None
player_info_font = None

# Elementy UI
dice_button_panel = None
exit_to_menu_button_panel = None
player_widgets = []


def load_gameplay_resources(screen_width, screen_height):
    """Ładuje wszystkie zasoby potrzebne dla ekranu rozgrywki."""
    global game_board_instance, left_panel_background_img, info_font, button_font_gameplay, player_info_font

    game_board_instance = Board(screen_width, screen_height)

    try:
        left_panel_background_img = pygame.image.load(settings.IMAGE_PATH_GAMEPLAY_LEFT_PANEL_BG).convert()
        left_panel_background_img = pygame.transform.scale(left_panel_background_img,
                                                           (settings.LEFT_PANEL_WIDTH, screen_height))
    except Exception as e:
        print(f"Błąd ładowania tła lewego panelu: {e}")
        left_panel_background_img = None

    try:
        info_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.GAMEPLAY_PANEL_INFO_FONT_SIZE)
        button_font_gameplay = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR,
                                                settings.GAMEPLAY_PANEL_BUTTON_FONT_SIZE)
        player_info_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.PLAYER_WIDGET_FONT_SIZE)
    except Exception as e:
        print(f"Błąd ładowania czcionek dla panelu gameplay: {e}")
        info_font = pygame.font.SysFont(None, settings.GAMEPLAY_PANEL_INFO_FONT_SIZE + 2)
        button_font_gameplay = pygame.font.SysFont(None, settings.GAMEPLAY_PANEL_BUTTON_FONT_SIZE + 2)
        player_info_font = pygame.font.SysFont(None, settings.PLAYER_WIDGET_FONT_SIZE + 2)


def setup_gameplay_ui_elements(screen_height_param, player_names):
    """Konfiguruje elementy UI panelu bocznego, w tym widgety graczy i przyciski."""
    global dice_button_panel, exit_to_menu_button_panel, player_widgets

    # --- Konfiguracja Widgetów Graczy ---
    player_widgets = []
    widget_start_x = settings.PLAYER_WIDGET_1_X_OFFSET
    widget_start_y = settings.PLAYER_WIDGET_1_Y_OFFSET

    if len(player_names) > 0:
        p1_widget = PlayerInfoWidget(
            x=widget_start_x, y=widget_start_y,
            player_name=player_names[0],
            font=player_info_font,
            image_path=settings.IMAGE_PATH_PLAYER_WIDGET_BG  # Ścieżka dla gracza 1
        )
        player_widgets.append(p1_widget)

    if len(player_names) > 1:
        p2_y_pos = p1_widget.widget_rect.bottom + settings.PLAYER_WIDGET_VERTICAL_SPACING
        p2_widget = PlayerInfoWidget(
            x=widget_start_x, y=p2_y_pos,
            player_name=player_names[1],
            font=player_info_font,
            image_path=settings.IMAGE_PATH_PLAYER_WIDGET_BG_2  # Ścieżka dla gracza 2
        )
        player_widgets.append(p2_widget)

    # --- Konfiguracja Przycisków ---
    btn_width = settings.GAMEPLAY_PANEL_BUTTON_WIDTH
    btn_height = settings.GAMEPLAY_PANEL_BUTTON_HEIGHT
    btn_spacing_panel = settings.GAMEPLAY_PANEL_BUTTON_SPACING

    dice_button_panel = Button(
        x=(settings.LEFT_PANEL_WIDTH - btn_width) // 2,
        y=screen_height_param - (btn_height * 2) - btn_spacing_panel - 50,
        width=btn_width, height=btn_height,
        text="Rzuć Kostką", font=button_font_gameplay,
        base_color=settings.PANEL_BUTTON_BASE_COLOR, hover_color=settings.PANEL_BUTTON_HOVER_COLOR,
        text_color=settings.PANEL_BUTTON_TEXT_COLOR, action="ROLL_DICE_PANEL", border_radius=10
    )

    exit_to_menu_button_panel = Button(
        x=(settings.LEFT_PANEL_WIDTH - btn_width) // 2,
        y=dice_button_panel.rect.bottom + btn_spacing_panel,
        width=btn_width, height=btn_height,
        text="Powrót do Menu", font=button_font_gameplay,
        base_color=settings.PANEL_BUTTON_BASE_COLOR, hover_color=settings.PANEL_BUTTON_HOVER_COLOR,
        text_color=settings.PANEL_BUTTON_TEXT_COLOR, action="BACK_TO_MENU", border_radius=10
    )


def handle_gameplay_input(event, mouse_pos):
    """Obsługuje input dla przycisków w panelu rozgrywki."""
    if exit_to_menu_button_panel:
        action_exit = exit_to_menu_button_panel.handle_event(event, mouse_pos)
        if action_exit: return action_exit
    if dice_button_panel:
        action_dice = dice_button_panel.handle_event(event, mouse_pos)
        if action_dice: return action_dice
    return None


def update_gameplay_state(current_player_id):
    """Aktualizuje stan rozgrywki, np. podświetlenie aktywnego gracza."""
    for i, widget in enumerate(player_widgets):
        player_id_to_check = f"player_{i + 1}"
        widget.set_active(player_id_to_check == current_player_id)


def draw_gameplay_screen(surface, mouse_pos, dice_instance_to_draw):
    """Rysuje cały ekran rozgrywki: panel boczny, planszę, UI i kostkę."""
    surface.fill(settings.DEFAULT_BG_COLOR)

    if left_panel_background_img:
        surface.blit(left_panel_background_img, (0, 0))
    else:
        pygame.draw.rect(surface, settings.PANEL_BG_COLOR, (0, 0, settings.LEFT_PANEL_WIDTH, surface.get_height()))

    if game_board_instance:
        game_board_instance.draw(surface)

    for widget in player_widgets:
        widget.draw(surface)

    if dice_button_panel:
        dice_button_panel.update_hover(mouse_pos)
        dice_button_panel.draw(surface)

    if exit_to_menu_button_panel:
        exit_to_menu_button_panel.update_hover(mouse_pos)
        exit_to_menu_button_panel.draw(surface)

    if dice_instance_to_draw and dice_button_panel:
        dice_instance_to_draw.dice_display_rect.centerx = dice_button_panel.rect.centerx
        dice_instance_to_draw.dice_display_rect.bottom = dice_button_panel.rect.top - 15
        dice_instance_to_draw.draw(surface)