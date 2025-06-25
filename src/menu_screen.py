# src/menu_screen.py
import pygame
from button import Button
import settings
import sound_manager  # Dodajemy import dla sprawdzania stanu wyciszenia

# Zmienne globalne modułu
menu_background_img = None
TITLE_FONT_MENU = None
BUTTON_FONT_MENU = None
menu_buttons_list = []
settings_button = None
settings_button_icon = None
mute_icon_overlay_img = None  # Dla obrazka 'X' na ikonce mute


def load_menu_resources(screen_width, screen_height):
    """Ładuje wszystkie zasoby potrzebne dla ekranu menu."""
    global menu_background_img, TITLE_FONT_MENU, BUTTON_FONT_MENU, settings_button_icon, mute_icon_overlay_img

    try:
        TITLE_FONT_MENU = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.MENU_TITLE_FONT_SIZE)
        BUTTON_FONT_MENU = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.MENU_BUTTON_FONT_SIZE)
    except pygame.error as e:
        print(f"Błąd ładowania czcionki dla menu: {e}")
        TITLE_FONT_MENU = pygame.font.SysFont(None, settings.MENU_TITLE_FONT_SIZE + 10)
        BUTTON_FONT_MENU = pygame.font.SysFont(None, settings.MENU_BUTTON_FONT_SIZE + 10)

    try:
        menu_background_img = pygame.image.load(settings.IMAGE_PATH_MENU_BG).convert()
        menu_background_img = pygame.transform.scale(menu_background_img, (screen_width, screen_height))
    except pygame.error as e:
        print(f"Błąd ładowania obrazka tła menu: {e}")
        menu_background_img = None

    try:
        icon_img_raw = pygame.image.load(settings.IMAGE_PATH_SETTINGS_ICON).convert_alpha()
        settings_button_icon = pygame.transform.scale(icon_img_raw,
                                                      (settings.SETTINGS_ICON_SIZE, settings.SETTINGS_ICON_SIZE))
    except Exception as e:
        print(f"Błąd ładowania ikonki ustawień: {e}")
        settings_button_icon = None

    # Ładowanie ikonki "X" dla wyciszenia
    try:
        mute_raw = pygame.image.load(settings.IMAGE_PATH_MUTE_ICON_OVERLAY).convert_alpha()
        mute_icon_overlay_img = pygame.transform.smoothscale(mute_raw,
                                                             (int(
                                                                 settings.SETTINGS_ICON_SIZE * settings.MUTE_ICON_OVERLAY_SCALE_FACTOR),
                                                              int(settings.SETTINGS_ICON_SIZE * settings.MUTE_ICON_OVERLAY_SCALE_FACTOR)))
    except Exception as e:
        print(f"Błąd ładowania ikonki wyciszenia dla menu: {e}")
        mute_icon_overlay_img = None


def setup_menu_ui_elements(screen_width, screen_height):
    """Konfiguruje wszystkie elementy UI na ekranie menu."""
    global menu_buttons_list, settings_button
    menu_buttons_list = []

    button_width = settings.MENU_BUTTON_WIDTH
    button_height = settings.MENU_BUTTON_HEIGHT
    button_spacing = settings.MENU_BUTTON_SPACING
    start_x = (screen_width - button_width) + settings.MENU_BUTTON_CENTER_X_OFFSET
    start_y = int(screen_height * settings.MENU_BUTTON_START_Y_OFFSET_PERCENTAGE)

    new_game_btn = Button(
        x=start_x, y=start_y,
        width=button_width, height=button_height,
        text="NOWA GRA", font=BUTTON_FONT_MENU,
        base_color=settings.MENU_BUTTON_BASE_COLOR, hover_color=settings.MENU_BUTTON_HOVER_COLOR,
        text_color=settings.MENU_TEXT_COLOR, action="GAMEPLAY", border_radius=15
    )
    menu_buttons_list.append(new_game_btn)

    instructions_btn = Button(
        x=start_x, y=new_game_btn.rect.bottom + button_spacing,
        width=button_width, height=button_height,
        text="INSTRUKCJA", font=BUTTON_FONT_MENU,
        base_color=settings.MENU_BUTTON_BASE_COLOR, hover_color=settings.MENU_BUTTON_HOVER_COLOR,
        text_color=settings.MENU_TEXT_COLOR, action="INSTRUCTIONS", border_radius=15
    )
    menu_buttons_list.append(instructions_btn)

    exit_btn = Button(
        x=start_x, y=instructions_btn.rect.bottom + button_spacing,
        width=button_width, height=button_height,
        text="WYJDŹ", font=BUTTON_FONT_MENU,
        base_color=settings.MENU_BUTTON_BASE_COLOR, hover_color=settings.MENU_BUTTON_HOVER_COLOR,
        text_color=settings.MENU_TEXT_COLOR, action="QUIT", border_radius=15
    )
    menu_buttons_list.append(exit_btn)

    settings_button = Button(
        x=settings.SETTINGS_ICON_X_OFFSET,
        y=settings.SETTINGS_ICON_Y_OFFSET,
        width=settings.SETTINGS_ICON_SIZE,
        height=settings.SETTINGS_ICON_SIZE,
        text="", font=BUTTON_FONT_MENU,
        base_color=(0, 0, 0, 0),
        hover_color=settings.SETTINGS_ICON_HOVER_BG_COLOR,
        text_color=(0, 0, 0), action="SETTINGS",
        border_radius=settings.SETTINGS_ICON_HOVER_BORDER_RADIUS
        # Obrazek ikonki jest przypisywany w logice rysowania, jeśli jest dostępny
    )


def handle_menu_input(event, mouse_pos):
    """Obsługuje zdarzenia dla wszystkich przycisków w menu."""
    if settings_button:  # Przycisk ustawień ma priorytet
        action = settings_button.handle_event(event, mouse_pos)
        if action: return action

    for btn in menu_buttons_list:
        action = btn.handle_event(event, mouse_pos)
        if action: return action

    return None


def draw_menu_screen(surface, screen_width, screen_height, mouse_pos):
    """Rysuje cały ekran menu."""
    global settings_button  # Potrzebujemy dostępu do obiektu przycisku

    if menu_background_img:
        if menu_background_img.get_size() != (screen_width, screen_height):
            current_bg = pygame.transform.scale(menu_background_img, (screen_width, screen_height))
            surface.blit(current_bg, (0, 0))
        else:
            surface.blit(menu_background_img, (0, 0))
    else:
        surface.fill(settings.MENU_BG_FALLBACK_COLOR)

    # Tytuł jest częścią tła, więc nie jest rysowany jako tekst

    # Rysowanie głównych przycisków
    for btn in menu_buttons_list:
        btn.update_hover(mouse_pos)
        btn.draw(surface)

    # Dedykowana logika rysowania dla przycisku ustawień z ikonką
    if settings_button and settings_button_icon:
        settings_button.update_hover(mouse_pos)

        # Rysuj podświetlenie i ramkę tylko, gdy jest hover
        if settings_button.is_hovered:
            hover_surface = pygame.Surface(settings_button.rect.size, pygame.SRCALPHA)
            hover_surface.fill(settings_button.hover_color)  # Użyj koloru hover zdefiniowanego dla przycisku
            surface.blit(hover_surface, settings_button.rect)

            pygame.draw.rect(surface, settings.SETTINGS_ICON_HOVER_OUTLINE_COLOR, settings_button.rect,
                             settings.SETTINGS_ICON_HOVER_OUTLINE_WIDTH,
                             border_radius=settings.SETTINGS_ICON_HOVER_BORDER_RADIUS)

        # Zawsze rysuj ikonkę ustawień na wierzchu
        surface.blit(settings_button_icon, settings_button.rect)

        # --- NOWA LOGIKA: Rysowanie ikonki MUTE na przycisku ustawień ---
        if sound_manager.is_effectively_muted() and mute_icon_overlay_img:
            # Wyśrodkuj ikonkę 'X' na ikonce ustawień
            mute_rect = mute_icon_overlay_img.get_rect(center=settings_button.rect.center)
            surface.blit(mute_icon_overlay_img, mute_rect)
        # -----------------------------------------------------------