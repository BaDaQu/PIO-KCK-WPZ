# src/gameplay_screen.py
import pygame
from board_screen import Board
from button import Button
from player_widget import PlayerInfoWidget
import settings
import sound_manager  # Dodano na wypadek przyszłych dźwięków specyficznych dla tego ekranu

# Zmienne globalne modułu
game_board_instance = None
left_panel_background_img = None
info_font = None  # Ogólna czcionka dla informacji w panelu
button_font_gameplay = None  # Czcionka dla standardowych przycisków w panelu
player_widgets = []  # Lista obiektów PlayerInfoWidget

# Elementy UI Panelu
dice_button_panel = None  # Przycisk "Rzuć Kostką"
forfeit_button_panel = None  # Przycisk "Zakończ Grę / Powrót do Menu"
settings_button_panel = None  # Przycisk ikonki Ustawień
settings_button_icon = None  # Załadowany obrazek ikonki Ustawień


def load_gameplay_resources(screen_width, screen_height):
    """Ładuje wszystkie zasoby potrzebne dla ekranu rozgrywki."""
    global game_board_instance, left_panel_background_img, info_font, button_font_gameplay, settings_button_icon

    # Inicjalizuj planszę z poprawnymi wymiarami ekranu rozgrywki
    # screen_width tutaj to GAMEPLAY_SCREEN_WIDTH z main.py
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
    except Exception as e:
        print(f"Błąd ładowania czcionek dla panelu gameplay: {e}")
        info_font = pygame.font.SysFont(None, settings.GAMEPLAY_PANEL_INFO_FONT_SIZE + 2)
        button_font_gameplay = pygame.font.SysFont(None, settings.GAMEPLAY_PANEL_BUTTON_FONT_SIZE + 2)

    # Ładowanie ikonki ustawień
    try:
        icon_img_raw = pygame.image.load(settings.IMAGE_PATH_SETTINGS_ICON).convert_alpha()
        settings_button_icon = pygame.transform.scale(icon_img_raw,
                                                      (settings.GAMEPLAY_SETTINGS_ICON_SIZE,
                                                       settings.GAMEPLAY_SETTINGS_ICON_SIZE))
    except Exception as e:
        print(f"Błąd ładowania ikonki ustawień dla gameplay: {e}")
        settings_button_icon = None


def setup_gameplay_ui_elements(screen_height_param, player_names):
    global dice_button_panel, forfeit_button_panel, player_widgets, settings_button_panel

    # --- Konfiguracja Widgetów Graczy (pozostaje bez zmian) ---
    player_widgets = []
    widget_start_x = settings.PLAYER_WIDGET_1_X_OFFSET
    widget_start_y = settings.PLAYER_WIDGET_1_Y_OFFSET
    if len(player_names) > 0:
        p1_widget = PlayerInfoWidget(
            x=widget_start_x, y=widget_start_y,
            player_id="player_1", player_name=player_names[0],
            image_path=settings.IMAGE_PATH_PLAYER_WIDGET_BG,
            ects_icon_path=settings.IMAGE_PATH_ECTS_ICON,
            heart_icon_path=settings.IMAGE_PATH_HEART_ICON,
            empty_heart_icon_path=settings.IMAGE_PATH_EMPTY_HEART_ICON
        )
        player_widgets.append(p1_widget)
    if len(player_names) > 1:
        p2_y_pos = p1_widget.widget_rect.bottom + settings.PLAYER_WIDGET_VERTICAL_SPACING
        p2_widget = PlayerInfoWidget(
            x=widget_start_x, y=p2_y_pos,
            player_id="player_2", player_name=player_names[1],
            image_path=settings.IMAGE_PATH_PLAYER_WIDGET_BG_2,
            ects_icon_path=settings.IMAGE_PATH_ECTS_ICON,
            heart_icon_path=settings.IMAGE_PATH_HEART_ICON,
            empty_heart_icon_path=settings.IMAGE_PATH_EMPTY_HEART_ICON
        )
        player_widgets.append(p2_widget)

    # --- Konfiguracja Przycisków Panelu ---
    btn_width = settings.GAMEPLAY_PANEL_BUTTON_WIDTH
    btn_height = settings.GAMEPLAY_PANEL_BUTTON_HEIGHT
    btn_spacing_panel = settings.GAMEPLAY_PANEL_BUTTON_SPACING

    # Definiujemy przesunięcie tylko dla tych dwóch przycisków
    horizontal_offset_for_dice_and_forfeit = 45

    # Przycisk "Rzuć Kostką"
    dice_button_panel = Button(
        x=(settings.LEFT_PANEL_WIDTH - btn_width) // 2 + horizontal_offset_for_dice_and_forfeit, # <-- DODANO PRZESUNIĘCIE
        y=screen_height_param - (btn_height * 2) - btn_spacing_panel - 50,
        width=btn_width, height=btn_height,
        text="Rzuć Kostką", font=button_font_gameplay,
        base_color=settings.PANEL_BUTTON_BASE_COLOR, hover_color=settings.PANEL_BUTTON_HOVER_COLOR,
        text_color=settings.PANEL_BUTTON_TEXT_COLOR, action="ROLL_DICE_PANEL", border_radius=10
    )

    # Przycisk "Zakończ Grę"
    forfeit_button_panel = Button(
        x=(settings.LEFT_PANEL_WIDTH - btn_width) // 2 + horizontal_offset_for_dice_and_forfeit, # <-- DODANO PRZESUNIĘCIE
        y=dice_button_panel.rect.bottom + btn_spacing_panel,
        width=btn_width, height=btn_height,
        text=settings.FORFEIT_BUTTON_TEXT,
        font=button_font_gameplay,
        base_color=settings.PANEL_BUTTON_BASE_COLOR, hover_color=settings.PANEL_BUTTON_HOVER_COLOR,
        text_color=settings.PANEL_BUTTON_TEXT_COLOR,
        action="FORFEIT_GAME",
        border_radius=10
    )

    # Przycisk Ustawień (zębatka) - jego pozycja X pozostaje bez zmian (sterowana przez settings.py)
    settings_button_panel = Button(
        x=settings.GAMEPLAY_SETTINGS_ICON_X,
        y=settings.GAMEPLAY_SETTINGS_ICON_Y,
        width=settings.GAMEPLAY_SETTINGS_ICON_SIZE,
        height=settings.GAMEPLAY_SETTINGS_ICON_SIZE,
        text="", font=None,
        base_color=(0,0,0,0),
        hover_color=settings.GAMEPLAY_SETTINGS_ICON_HOVER_BG_COLOR,
        text_color=(0,0,0),
        action="OPEN_SETTINGS_OVERLAY",
        border_radius=settings.GAMEPLAY_SETTINGS_ICON_HOVER_BORDER_RADIUS,
        image=settings_button_icon
    )


def handle_gameplay_input(event, mouse_pos):
    """Obsługuje input dla wszystkich przycisków w panelu rozgrywki."""
    # Przycisk ustawień ma priorytet, bo może być kliknięty zawsze
    if settings_button_panel:
        action = settings_button_panel.handle_event(event, mouse_pos)
        if action: return action

    if forfeit_button_panel:
        action = forfeit_button_panel.handle_event(event, mouse_pos)
        if action: return action

    if dice_button_panel:
        action = dice_button_panel.handle_event(event, mouse_pos)
        if action: return action

    return None


def update_gameplay_state(current_player_id, dt_seconds):
    """Aktualizuje stan rozgrywki, w tym podświetlenie i animacje widgetów."""
    for widget in player_widgets:
        widget.set_active(widget.player_id == current_player_id)
        widget.update(dt_seconds)


def draw_gameplay_screen(surface, mouse_pos, dice_instance_to_draw):
    """Rysuje cały ekran rozgrywki: panel boczny, planszę, UI i kostkę."""
    surface.fill(settings.DEFAULT_BG_COLOR)

    # Rysowanie lewego panelu
    if left_panel_background_img:
        surface.blit(left_panel_background_img, (0, 0))
    else:
        pygame.draw.rect(surface, settings.PANEL_BG_COLOR, (0, 0, settings.LEFT_PANEL_WIDTH, surface.get_height()))

    # Rysowanie planszy gry
    if game_board_instance:
        game_board_instance.draw(surface)  # Plansza sama wie, gdzie się narysować

    # Rysowanie widgetów graczy
    for widget in player_widgets:
        widget.draw(surface)

    # Rysowanie przycisków panelu
    if dice_button_panel:
        dice_button_panel.update_hover(mouse_pos)
        dice_button_panel.draw(surface)

    if forfeit_button_panel:
        forfeit_button_panel.update_hover(mouse_pos)
        forfeit_button_panel.draw(surface)

    # Dedykowana logika rysowania dla przycisku ustawień z ikonką
    if settings_button_panel and settings_button_icon:
        settings_button_panel.update_hover(mouse_pos)
        # Rysuj podświetlenie i ramkę tylko, gdy jest hover
        if settings_button_panel.is_hovered:
            hover_surface = pygame.Surface(settings_button_panel.rect.size, pygame.SRCALPHA)
            hover_surface.fill(settings.GAMEPLAY_SETTINGS_ICON_HOVER_BG_COLOR)
            surface.blit(hover_surface, settings_button_panel.rect)

            pygame.draw.rect(surface, settings.GAMEPLAY_SETTINGS_ICON_HOVER_OUTLINE_COLOR, settings_button_panel.rect,
                             settings.GAMEPLAY_SETTINGS_ICON_HOVER_OUTLINE_WIDTH,
                             border_radius=settings.GAMEPLAY_SETTINGS_ICON_HOVER_BORDER_RADIUS)
        # Zawsze rysuj ikonkę na wierzchu
        surface.blit(settings_button_icon, settings_button_panel.rect)

    # Rysowanie samego obrazka kostki (przekazanej z main.py)
    if dice_instance_to_draw and dice_button_panel:
        # Pozycjonuj obrazek kostki nad przyciskiem "Rzuć Kostką"
        dice_instance_to_draw.dice_display_rect.centerx = dice_button_panel.rect.centerx
        dice_instance_to_draw.dice_display_rect.bottom = dice_button_panel.rect.top - 15  # 15px odstępu
        dice_instance_to_draw.draw(surface)