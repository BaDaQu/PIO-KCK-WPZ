# src/instructions_screen.py
import pygame
import settings
import text_utility  # Upewniamy się, że mamy dostęp do nowej funkcji
from button import Button

# Zmienne Modułu
background_image = None
back_button = None

RULES_TEXT = [
    ("Cel Gry", "header"),
    ("Wygrywa gracz, który jako pierwszy zdobędzie 30 punktów ECTS. Przegrywasz, gdy stracisz wszystkie 3 życia.",
     "body"),

    ("Tura i Pola", "header"),
    ("Kliknij 'Rzuć Kostką', aby się poruszyć. Lądując na polu przedmiotu, odpowiadasz na pytanie. Poprawna odpowiedź daje +1 ECTS, błędna przesuwa Profesora o 1 pole. Pola specjalne dają bonusy lub kary: STYPENDIUM (+2 ECTS), POPRAWKA (-2 ECTS).",
     "body"),

    ("Egzamin i Profesor", "header"),
    ("Pole EGZAMIN uruchamia test z 3 losowych pytań (poprawna: +1 ECTS, błędna: -1 ECTS i ruch Profesora). Profesor porusza się o 1 pole co 3 tury graczy oraz po każdej błędnej odpowiedzi. Złapanie przez Profesora kosztuje 1 życie i 1 ECTS.",
     "body"),

    ("Koniec Gry", "header"),
    ("Gra kończy się natychmiast, gdy gracz zdobędzie 30 ECTS, straci wszystkie życia lub podda grę przyciskiem 'Zakończ Grę'.",
     "body")
]


def load_instructions_resources(screen_width, screen_height):
    """Ładuje zasoby potrzebne dla PEŁNOEKRANOWEJ instrukcji."""
    global background_image
    try:
        bg_image_raw = pygame.image.load(settings.IMAGE_PATH_INSTRUCTIONS_BG).convert()
        background_image = pygame.transform.scale(bg_image_raw, (screen_width, screen_height))
    except Exception as e:
        print(f"Błąd ładowania tła instrukcji: {e}")
        background_image = None


def setup_instructions_ui(screen_width, screen_height, back_button_font):
    """Konfiguruje przycisk powrotu dla pełnego ekranu."""
    global back_button
    btn_width = settings.INSTRUCTIONS_BACK_BUTTON_WIDTH
    btn_height = settings.INSTRUCTIONS_BACK_BUTTON_HEIGHT

    back_button = Button(
        x=(screen_width - btn_width) // 2,
        y=screen_height + settings.INSTRUCTIONS_BACK_BUTTON_Y_OFFSET,  # Poprawka, aby przycisk był widoczny
        width=btn_width, height=btn_height,
        text="Powrót do Menu", font=back_button_font,
        base_color=settings.MENU_BUTTON_BASE_COLOR,
        hover_color=settings.MENU_BUTTON_HOVER_COLOR,
        text_color=settings.MENU_TEXT_COLOR,
        action="BACK_TO_MENU",
        border_radius=15
    )


def handle_instructions_input(event, mouse_pos):
    """Obsługuje input dla ekranu instrukcji."""
    if back_button:
        action = back_button.handle_event(event, mouse_pos)
        if action: return action
    if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN):
        return "BACK_TO_MENU"
    return None


def draw_instructions_screen(surface, mouse_pos):
    """Rysuje cały, pełnoekranowy widok instrukcji z tekstem z obrysem."""
    if background_image:
        surface.blit(background_image, (0, 0))
    else:
        surface.fill(settings.INSTRUCTIONS_FALLBACK_BG_COLOR)

    # Rysowanie tytułu z obrysem
    title_area = pygame.Rect(0, settings.INSTRUCTIONS_TITLE_Y - 40, surface.get_width(), 100)
    text_utility.render_text(
        surface=surface, text="Instrukcja Gry",
        font_path=settings.FONT_PATH_PT_SERIF_REGULAR, initial_font_size=settings.INSTRUCTIONS_TITLE_FONT_SIZE,
        color=settings.INSTRUCTIONS_TITLE_COLOR,
        rect=title_area,
        outline_color=settings.INSTRUCTIONS_OUTLINE_COLOR,
        outline_width=settings.INSTRUCTIONS_OUTLINE_WIDTH
    )

    # Rysowanie treści zasad
    current_y = settings.INSTRUCTIONS_CONTENT_START_Y
    text_area_width = surface.get_width() - 2 * settings.INSTRUCTIONS_CONTENT_X_PADDING

    for text, style in RULES_TEXT:
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
            surface.get_height() - current_y  # Ogranicz wysokość, żeby tekst się nie wylewał
        )

        # --- ZMIANA: Wywołujemy nową, uniwersalną funkcję ---
        final_y = text_utility.render_text(
            surface=surface, text=text,
            font_path=settings.FONT_PATH_PT_SERIF_REGULAR,
            initial_font_size=font_size,
            color=color,
            rect=text_area_rect,
            vertical_align='top',
            horizontal_align='left',  # Wyrównanie do lewej dla czytelności
            outline_color=settings.INSTRUCTIONS_OUTLINE_COLOR,
            outline_width=settings.INSTRUCTIONS_OUTLINE_WIDTH,
            return_final_y=True  # Prosimy o zwrócenie pozycji Y ostatniej linii
        )

        # Aktualizuj pozycję Y dla następnego bloku tekstu
        if final_y:
            current_y = final_y

    # Rysowanie przycisku powrotu
    if back_button:
        back_button.update_hover(mouse_pos)
        back_button.draw(surface)