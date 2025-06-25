# src/instructions_screen.py
import pygame
import settings
import text_utility
from button import Button
import sound_manager  # Dodajemy import dla dźwięków

# Zmienne Modułu
background_image = None
title_font = None  # Zostanie załadowane w load_instructions_resources
header_font = None
body_font = None
back_button = None

RULES_TEXT = [
    ("Cel Gry", "header"),
    ("Wygrywa gracz, który jako pierwszy zdobędzie 20 punktów ECTS. Przegrywasz, gdy stracisz wszystkie 3 życia.",
     "body"),

    ("Tura i Pola", "header"),
    ("Aktywny gracz jest podświetlony. Kliknij 'Rzuć Kostką', aby się poruszyć. Lądując na polu przedmiotu, odpowiadasz na pytanie. Poprawna odpowiedź daje +1 ECTS, błędna przesuwa Profesora o 1 pole. Pola specjalne dają bonusy lub kary: STYPENDIUM (+2 ECTS), POPRAWKA (-2 ECTS).",
     "body"),

    ("Egzamin i Profesor", "header"),
    ("Pole EGZAMIN uruchamia test z 3 losowych pytań (poprawna: +1 ECTS, błędna: -1 ECTS i ruch Profesora). Profesor porusza się o 1 pole co 3 tury graczy oraz po każdej błędnej odpowiedzi. Złapanie przez Profesora kosztuje 1 życie i 1 punkt ECTS.",
     "body"),

    ("Koniec Gry", "header"),
    ("Gra kończy się natychmiast, gdy gracz zdobędzie 30 ECTS, straci wszystkie życia lub podda grę przyciskiem 'Zakończ Grę'.",
     "body"),

    # === NOWA SEKCJA ===
    ("Sterowanie", "header"),
    ("Menu Główne: [N] - Nowa Gra, [I] - Instrukcja, [S] - Ustawienia, [M] - Wyciszenie, [Esc] - Wyjście.", "body_bullet"),
    ("Ekran Imion: [Góra]/[Dół]/[Tab] - Zmiana pola, [Enter] - Start Gry.", "body_bullet"),
    ("Karta Pytania: [A]/[1], [B]/[2], [C]/[3], [D]/[4] - Wybór odpowiedzi.", "body_bullet"),
    ("Rozgrywka: [Enter]/[Spacja] - Rzut kostką, [S] - Ustawienia.", "body_bullet"),
    ("Instrukcja/Koniec Gry: [Enter]/[Esc]/[I] - Powrót do Menu.", "body_bullet"),
    ("Ustawienia (Nakładka): [Esc]/[S] - Zamknij Ustawienia.", "body_bullet")
    # ===================
]


def load_instructions_resources(screen_width, screen_height):
    """Ładuje zasoby potrzebne dla PEŁNOEKRANOWEJ instrukcji."""
    global background_image, title_font, header_font, body_font
    try:
        bg_image_raw = pygame.image.load(settings.IMAGE_PATH_INSTRUCTIONS_BG).convert()
        background_image = pygame.transform.scale(bg_image_raw, (screen_width, screen_height))
    except Exception as e:
        print(f"Błąd ładowania tła instrukcji: {e}")
        background_image = None

    try:
        title_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.INSTRUCTIONS_TITLE_FONT_SIZE)
        header_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.INSTRUCTIONS_HEADER_FONT_SIZE)
        body_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.INSTRUCTIONS_BODY_FONT_SIZE)
    except Exception as e:
        print(f"Błąd ładowania czcionek dla instrukcji: {e}")
        title_font = pygame.font.SysFont(None, settings.INSTRUCTIONS_TITLE_FONT_SIZE)
        header_font = pygame.font.SysFont(None, settings.INSTRUCTIONS_HEADER_FONT_SIZE)
        body_font = pygame.font.SysFont(None, settings.INSTRUCTIONS_BODY_FONT_SIZE)


def setup_instructions_ui(screen_width, screen_height, back_button_font_from_menu):
    """Konfiguruje przycisk powrotu dla pełnego ekranu."""
    global back_button
    btn_width = settings.INSTRUCTIONS_BACK_BUTTON_WIDTH
    btn_height = settings.INSTRUCTIONS_BACK_BUTTON_HEIGHT

    back_button = Button(
        x=(screen_width - btn_width) // 2,
        y=screen_height + settings.INSTRUCTIONS_BACK_BUTTON_Y_OFFSET,  # Poprawka, aby przycisk był widoczny
        width=btn_width, height=btn_height,
        text="Powrót do Menu", font=back_button_font_from_menu,  # Użyj czcionki z menu
        base_color=settings.MENU_BUTTON_BASE_COLOR,
        hover_color=settings.MENU_BUTTON_HOVER_COLOR,
        text_color=settings.MENU_TEXT_COLOR,
        action="BACK_TO_MENU",
        border_radius=15
    )


def handle_instructions_input(event, mouse_pos):
    """Obsługuje input dla ekranu instrukcji, w tym klawisz 'I'."""
    if back_button:
        action = back_button.handle_event(event, mouse_pos)
        if action:
            sound_manager.play_sound('button_click')
            return action

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_i:  # <-- DODANO event.key == pygame.K_i
            sound_manager.play_sound('button_click')
            return "BACK_TO_MENU"
    return None


def draw_instructions_screen(surface, mouse_pos):
    """Rysuje cały, pełnoekranowy widok instrukcji z tekstem z obrysem."""
    if background_image:
        surface.blit(background_image, (0, 0))
    else:
        surface.fill(settings.INSTRUCTIONS_FALLBACK_BG_COLOR)

    # Rysowanie tytułu z obrysem
    title_area = pygame.Rect(0, settings.INSTRUCTIONS_TITLE_Y - 40, surface.get_width(),
                             100)  # Definiujemy obszar dla tytułu
    text_utility.render_text(
        surface=surface, text="Instrukcja Gry",
        font_path=settings.FONT_PATH_PT_SERIF_REGULAR, initial_font_size=settings.INSTRUCTIONS_TITLE_FONT_SIZE,
        color=settings.INSTRUCTIONS_TITLE_COLOR,
        rect=title_area,  # Przekazujemy zdefiniowany prostokąt
        outline_color=settings.INSTRUCTIONS_OUTLINE_COLOR,
        outline_width=settings.INSTRUCTIONS_OUTLINE_WIDTH
    )

    current_y = settings.INSTRUCTIONS_CONTENT_START_Y
    text_area_width = surface.get_width() - 2 * settings.INSTRUCTIONS_CONTENT_X_PADDING

    for text, style in RULES_TEXT:
        font_to_use = None
        if style == "header":
            font_size = settings.INSTRUCTIONS_HEADER_FONT_SIZE
            color = settings.INSTRUCTIONS_HEADER_COLOR
            y_spacing = settings.INSTRUCTIONS_SECTION_SPACING
            indent = 0
        elif style == "body_bullet":
            font_size = settings.INSTRUCTIONS_BODY_FONT_SIZE
            color = settings.INSTRUCTIONS_BODY_COLOR
            text = "• " + text
            y_spacing = 5
            indent = settings.INSTRUCTIONS_BULLET_INDENT
        else:  # "body"
            font_size = settings.INSTRUCTIONS_BODY_FONT_SIZE
            color = settings.INSTRUCTIONS_BODY_COLOR
            y_spacing = 15
            indent = 0

        current_y += y_spacing

        text_area_rect = pygame.Rect(
            settings.INSTRUCTIONS_CONTENT_X_PADDING + indent,
            current_y,
            text_area_width - indent,
            surface.get_height() - current_y  # Ogranicz wysokość
        )

        final_y = text_utility.render_text(
            surface=surface, text=text,
            font_path=settings.FONT_PATH_PT_SERIF_REGULAR,
            initial_font_size=font_size,
            color=color,
            rect=text_area_rect,
            vertical_align='top',
            horizontal_align='left',
            outline_color=settings.INSTRUCTIONS_OUTLINE_COLOR,
            outline_width=settings.INSTRUCTIONS_OUTLINE_WIDTH,
            return_final_y=True
        )

        if final_y:
            current_y = final_y  # Aktualizuj pozycję Y dla następnego bloku tekstu

    if back_button:
        back_button.update_hover(mouse_pos)
        back_button.draw(surface)