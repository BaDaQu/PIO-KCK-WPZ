# src/menu_screen.py
import pygame
from button import Button
import settings  # Używamy settings dla kolorów i ścieżek

# Zmienne globalne dla tego modułu
menu_background_img = None
TITLE_FONT_MENU = None  # Zmieniona nazwa, aby nie kolidować
BUTTON_FONT_MENU = None  # Zmieniona nazwa
menu_buttons_list = []


def load_menu_resources(screen_width, screen_height):
    global menu_background_img, TITLE_FONT_MENU, BUTTON_FONT_MENU
    try:
        # Używamy rozmiarów czcionek z settings.py
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


def setup_menu_ui_elements(screen_width, screen_height):
    global menu_buttons_list, BUTTON_FONT_MENU  # Używamy czcionki załadowanej dla menu
    menu_buttons_list = []  # Czyścimy listę przed ponownym setupem

    # Używamy stałych z settings.py dla wymiarów i odstępów
    button_width = settings.MENU_BUTTON_WIDTH
    button_height = settings.MENU_BUTTON_HEIGHT
    button_spacing = settings.MENU_BUTTON_SPACING

    # Oryginalne pozycjonowanie przycisków (z Twojego kodu przed moimi zmianami w settings)
    # (screen_width - button_width) - 140  -> to daje x przesunięty w prawo
    # Jeśli chcesz je bardziej na środku lub inaczej, dostosuj start_x
    # start_x = (screen_width - button_width) // 2 # Dla idealnego wyśrodkowania

    start_x = (screen_width - button_width) + settings.MENU_BUTTON_CENTER_X_OFFSET  # Użyj offsetu z settings
    start_y = int(screen_height * settings.MENU_BUTTON_START_Y_OFFSET_PERCENTAGE)
    # start_y = screen_height - 280 - button_height - button_spacing # Alternatywne pozycjonowanie od dołu

    # Tworzenie obiektów Button
    new_game_btn = Button(
        x=start_x, y=start_y,
        width=button_width, height=button_height,
        text="NOWA GRA", font=BUTTON_FONT_MENU,
        base_color=settings.MENU_BUTTON_BASE_COLOR,
        hover_color=settings.MENU_BUTTON_HOVER_COLOR,
        text_color=settings.MENU_TEXT_COLOR,
        action="GAMEPLAY",
        border_radius=15  # Możesz dodać border_radius do settings
    )
    menu_buttons_list.append(new_game_btn)

    instructions_btn = Button(
        x=start_x, y=new_game_btn.rect.bottom + button_spacing,
        width=button_width, height=button_height,
        text="INSTRUKCJA", font=BUTTON_FONT_MENU,
        base_color=settings.MENU_BUTTON_BASE_COLOR,
        hover_color=settings.MENU_BUTTON_HOVER_COLOR,
        text_color=settings.MENU_TEXT_COLOR,
        action="INSTRUCTIONS",
        border_radius=15
    )
    menu_buttons_list.append(instructions_btn)

    exit_btn = Button(
        x=start_x, y=instructions_btn.rect.bottom + button_spacing,
        width=button_width, height=button_height,
        text="WYJDŹ", font=BUTTON_FONT_MENU,
        base_color=settings.MENU_BUTTON_BASE_COLOR,
        hover_color=settings.MENU_BUTTON_HOVER_COLOR,
        text_color=settings.MENU_TEXT_COLOR,
        action="QUIT",
        border_radius=15
    )
    menu_buttons_list.append(exit_btn)


def handle_menu_input(event, mouse_pos):
    for btn in menu_buttons_list:
        # update_hover jest teraz wywoływane w pętli głównej rysowania,
        # ale można też tutaj, jeśli chcemy logikę hover przed logiką kliknięcia
        # btn.update_hover(mouse_pos)
        action = btn.handle_event(event, mouse_pos)
        if action:
            return action
    return None


def draw_menu_screen(surface, screen_width, screen_height, mouse_pos):
    # Rysowanie tła
    if menu_background_img:
        # Upewnij się, że tło jest poprawnie skalowane, jeśli rozmiar okna się zmienia
        # (choć dla menu głównego zwykle rozmiar jest stały)
        if menu_background_img.get_size() != (screen_width, screen_height):
            current_bg = pygame.transform.scale(menu_background_img, (screen_width, screen_height))
            surface.blit(current_bg, (0, 0))
        else:
            surface.blit(menu_background_img, (0, 0))
    else:
        surface.fill(settings.MENU_BG_FALLBACK_COLOR)  # Użyj koloru zastępczego z settings

    # Celowo NIE rysujemy tutaj tytułu "Wyścig po zaliczenie",
    # ponieważ jest on już częścią grafiki tła `MENU_GLOWNE.png`
    # if TITLE_FONT_MENU:
    #     title_surface = TITLE_FONT_MENU.render("Wyścig po zaliczenie", True, settings.MENU_TITLE_COLOR)
    #     title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 4 - 20))
    #     surface.blit(title_surface, title_rect)

    # Rysowanie przycisków
    for btn in menu_buttons_list:
        btn.update_hover(mouse_pos)  # Ważne, aby stan hover był aktualny przed rysowaniem
        btn.draw(surface)