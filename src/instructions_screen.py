# src/instructions_screen.py
import pygame
import settings
import text_utility
from button import Button

# Zmienne Modułu
background_image = None
title_font = None
header_font = None
body_font = None
back_button = None

# Treść zasad
RULES_TEXT = [
    ("Cel Gry", "header"),
    ("Dotrzyj do mety przed przeciwnikiem i goniącym Cię Profesorem, zachowując przy tym jak najwięcej żyć i punktów ECTS.",
     "body"),
    ("Przebieg Tury", "header"),
    ("1. Rzut Kostką: Kliknij przycisk, aby przesunąć swój pionek o wylosowaną liczbę oczek.", "body"),
    ("2. Akcja Pola: Po zatrzymaniu się na polu, wykonaj odpowiednią akcję.", "body"),
    ("Pola Specjalne", "header"),
    ("STYPENDIUM: Otrzymujesz +2 punkty ECTS.", "body_bullet"),
    ("POPRAWKA: Tracisz -2 punkty ECTS.", "body_bullet"),
    ("EGZAMIN: Odpowiedz na 3 losowe pytania. Za 2+ poprawne odpowiedzi odzyskujesz 1 życie!", "body_bullet"),
    ("Pionek Profesora", "header"),
    ("Profesor goni graczy! Przesuwa się co 3 tury oraz za każdą błędną odpowiedź. Złapanie przez Profesora kosztuje 1 życie i 1 ECTS.",
     "body"),
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
        title_font = pygame.font.SysFont(None, settings.INSTRUCTIONS_TITLE_FONT_SIZE)
        header_font = pygame.font.SysFont(None, settings.INSTRUCTIONS_HEADER_FONT_SIZE)
        body_font = pygame.font.SysFont(None, settings.INSTRUCTIONS_BODY_FONT_SIZE)


def setup_instructions_ui(screen_width, screen_height, back_button_font):
    """Konfiguruje przycisk powrotu dla pełnego ekranu."""
    global back_button
    btn_width = settings.INSTRUCTIONS_BACK_BUTTON_WIDTH
    btn_height = settings.INSTRUCTIONS_BACK_BUTTON_HEIGHT

    back_button = Button(
        x=(screen_width - btn_width) // 2,
        y=screen_height + settings.INSTRUCTIONS_BACK_BUTTON_Y_OFFSET - btn_height,
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
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return "BACK_TO_MENU"
    return None


def draw_instructions_screen(surface, mouse_pos):
    """Rysuje cały, pełnoekranowy widok instrukcji z tekstem z obrysem."""
    if background_image:
        surface.blit(background_image, (0, 0))
    else:
        surface.fill(settings.INSTRUCTIONS_FALLBACK_BG_COLOR)

    # Rysowanie tytułu z obrysem
    title_surf = text_utility.render_text_with_outline(
        font=title_font,
        text="Instrukcja Gry",
        base_color=settings.INSTRUCTIONS_TITLE_COLOR,
        outline_color=settings.INSTRUCTIONS_OUTLINE_COLOR,
        outline_width=settings.INSTRUCTIONS_OUTLINE_WIDTH
    )
    title_rect = title_surf.get_rect(centerx=surface.get_rect().centerx, top=settings.INSTRUCTIONS_TITLE_Y)
    surface.blit(title_surf, title_rect)

    # Rysowanie treści zasad z obrysem
    current_y = settings.INSTRUCTIONS_CONTENT_START_Y
    text_area_width = surface.get_width() - 2 * settings.INSTRUCTIONS_CONTENT_X_PADDING

    for text, style in RULES_TEXT:
        if style == "header":
            font = header_font
            color = settings.INSTRUCTIONS_HEADER_COLOR
            y_spacing = settings.INSTRUCTIONS_SECTION_SPACING
            indent = 0
        elif style == "body_bullet":
            font = body_font
            color = settings.INSTRUCTIONS_BODY_COLOR
            text = "• " + text
            y_spacing = 5
            indent = settings.INSTRUCTIONS_BULLET_INDENT
        else:  # "body"
            font = body_font
            color = settings.INSTRUCTIONS_BODY_COLOR
            y_spacing = 15
            indent = 0

        current_y += y_spacing

        # Łamanie tekstu na linie
        words = text.split(' ')
        lines = []
        current_line = ""
        max_width = text_area_width - indent
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line.strip())[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())

        # Rysowanie każdej linii z obrysem
        for line_text in lines:
            if not line_text: continue
            line_surface = text_utility.render_text_with_outline(
                font, line_text, color,
                settings.INSTRUCTIONS_OUTLINE_COLOR,
                settings.INSTRUCTIONS_OUTLINE_WIDTH
            )
            line_rect = line_surface.get_rect(left=settings.INSTRUCTIONS_CONTENT_X_PADDING + indent, top=current_y)
            surface.blit(line_surface, line_rect)
            current_y += int(font.get_linesize() * settings.INSTRUCTIONS_LINE_SPACING)

    # Rysowanie przycisku powrotu
    if back_button:
        back_button.update_hover(mouse_pos)
        back_button.draw(surface)