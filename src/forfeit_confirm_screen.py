# src/forfeit_confirm_screen.py
import pygame
import settings
from button import Button
import text_utility  # Potrzebne dla tekstu z obrysem
import sound_manager

# Zmienne modułu
background_surface = None  # Dla przyciemnienia
# box_rect nie jest już potrzebne
confirm_font = None
button_font = None
yes_button = None
no_button = None


def setup_forfeit_confirm_screen(screen_width, screen_height):
    """Konfiguruje UI dla nakładki potwierdzenia poddania gry."""
    global background_surface, confirm_font, button_font, yes_button, no_button

    background_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    background_surface.fill(settings.CONFIRM_OVERLAY_BG_COLOR)

    # box_rect nie jest już potrzebny, elementy będą pozycjonowane względem środka ekranu

    try:
        confirm_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.CONFIRM_FONT_SIZE)
        button_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.CONFIRM_BUTTON_FONT_SIZE)
    except Exception as e:
        print(f"Błąd ładowania czcionek dla ekranu potwierdzenia: {e}")
        confirm_font = pygame.font.SysFont(None, settings.CONFIRM_FONT_SIZE)
        button_font = pygame.font.SysFont(None, settings.CONFIRM_BUTTON_FONT_SIZE)

    btn_w = settings.CONFIRM_BUTTON_WIDTH
    btn_h = settings.CONFIRM_BUTTON_HEIGHT
    spacing = settings.CONFIRM_BUTTON_SPACING

    # Pozycjonowanie przycisków względem środka ekranu
    screen_center_x = screen_width // 2
    screen_center_y = screen_height // 2

    buttons_total_width = btn_w * 2 + spacing
    start_x_buttons = screen_center_x - buttons_total_width // 2
    buttons_y_pos = screen_center_y + settings.CONFIRM_BUTTONS_Y_OFFSET

    yes_button = Button(
        x=start_x_buttons, y=buttons_y_pos,
        width=btn_w, height=btn_h, text="Tak", font=button_font,
        base_color=settings.MENU_BUTTON_BASE_COLOR, hover_color=settings.MENU_BUTTON_HOVER_COLOR,
        text_color=settings.MENU_TEXT_COLOR, action="CONFIRM_YES", border_radius=10
    )
    no_button = Button(
        x=start_x_buttons + btn_w + spacing, y=buttons_y_pos,
        width=btn_w, height=btn_h, text="Nie", font=button_font,
        base_color=settings.MENU_BUTTON_BASE_COLOR, hover_color=settings.MENU_BUTTON_HOVER_COLOR,
        text_color=settings.MENU_TEXT_COLOR, action="CONFIRM_NO", border_radius=10
    )


def handle_forfeit_confirm_input(event, mouse_pos):
    # Ta funkcja pozostaje bez zmian
    if yes_button and yes_button.handle_event(event, mouse_pos):
        sound_manager.play_sound('button_click');
        return "CONFIRM_YES"
    if no_button and no_button.handle_event(event, mouse_pos):
        sound_manager.play_sound('button_click');
        return "CONFIRM_NO"
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            sound_manager.play_sound('button_click');
            return "CONFIRM_YES"
        elif event.key == pygame.K_ESCAPE:
            sound_manager.play_sound('button_click');
            return "CONFIRM_NO"
    return None


def draw_forfeit_confirm_screen(surface, mouse_pos):
    """Rysuje nakładkę potwierdzenia bez dodatkowego boxa."""
    if not background_surface: return

    # Rysuj przyciemnione tło
    surface.blit(background_surface, (0, 0))

    # Rysuj tekst pytania z obrysem dla lepszej czytelności
    if confirm_font:
        text_to_render = "Czy na pewno chcesz zakończyć grę?"
        # Definiujemy obszar dla tekstu (może być szeroki, funkcja go wyśrodkuje)
        text_area_rect = pygame.Rect(0, 0, surface.get_width() - 100, 100)  # 50px marginesu z każdej strony
        text_area_rect.centerx = surface.get_rect().centerx
        text_area_rect.centery = surface.get_rect().centery + settings.CONFIRM_TEXT_Y_OFFSET

        text_utility.render_text(  # Używamy uniwersalnej funkcji
            surface=surface,
            text=text_to_render,
            font_path=settings.FONT_PATH_PT_SERIF_REGULAR,  # lub inna czcionka jeśli chcesz
            initial_font_size=settings.CONFIRM_FONT_SIZE,
            color=settings.CONFIRM_TEXT_COLOR,  # Zmieniono na biały dla kontrastu
            rect=text_area_rect,
            outline_color=settings.BLACK,  # Dodajemy czarny obrys
            outline_width=2,
            vertical_align='center'
        )

    # Rysuj przyciski
    if yes_button:
        yes_button.update_hover(mouse_pos)
        yes_button.draw(surface)
    if no_button:
        no_button.update_hover(mouse_pos)
        no_button.draw(surface)