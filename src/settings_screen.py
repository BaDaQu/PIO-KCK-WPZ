# src/settings_screen.py
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
import settings
import menu_screen  # Potrzebne dla czcionki przycisku "Powrót"
import sound_manager
from button import Button
import text_utility

# Zmienne modułu
background_image = None  # Tło dla samego ekranu ustawień (opcjonalne, jeśli tło z gry/menu jest przyciemniane)
back_button = None
sliders = []
# Flaga is_visible w tym module nie jest już tak kluczowa, bo main.py decyduje, kiedy rysować
# ale zostawiamy ją do kontroli wewnętrznej, czy suwaki zostały pokazane/ukryte
is_active = False
title_font = None
header_font = None


def setup_settings_screen(surface, screen_width, screen_height):
    """Konfiguruje UI dla ekranu ustawień. Wywoływana raz na początku i przy zmianie trybu ekranu."""
    global background_image, back_button, sliders, title_font, header_font, is_active

    sliders = []  # Czyścimy listę, aby uniknąć duplikatów przy np. zmianie rozdzielczości
    is_active = False  # Domyślnie nie jest aktywny

    try:
        title_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.INSTRUCTIONS_TITLE_FONT_SIZE)
        header_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR, settings.INSTRUCTIONS_HEADER_FONT_SIZE)
    except Exception as e:
        print(f"Błąd ładowania czcionek dla ustawień: {e}")
        title_font = pygame.font.SysFont(None, settings.INSTRUCTIONS_TITLE_FONT_SIZE)
        header_font = pygame.font.SysFont(None, settings.INSTRUCTIONS_HEADER_FONT_SIZE)

    # Tło dla ekranu ustawień (może być to samo co instrukcja lub inne)
    try:
        bg_img_raw = pygame.image.load(settings.IMAGE_PATH_INSTRUCTIONS_BG).convert()
        background_image = pygame.transform.scale(bg_img_raw, (screen_width, screen_height))
    except Exception as e:
        print(f"Błąd ładowania tła dla ustawień: {e}")
        background_image = None

    center_x = screen_width // 2
    slider_x = center_x - settings.SLIDER_WIDTH // 2
    y_pos = settings.SLIDER_START_Y

    slider_params = {
        'min': 0, 'max': 100, 'step': 1,
        'handleColour': settings.MENU_BUTTON_HOVER_COLOR,
        'colour': settings.MENU_BUTTON_BASE_COLOR,
        'handleRadius': 15, 'radius': 10, 'curved': False
    }

    sliders.append(Slider(surface, slider_x, y_pos, settings.SLIDER_WIDTH, settings.SLIDER_HEIGHT,
                          initial=sound_manager.master_volume * 100, **slider_params))
    y_pos += settings.SLIDER_Y_SPACING
    sliders.append(Slider(surface, slider_x, y_pos, settings.SLIDER_WIDTH, settings.SLIDER_HEIGHT,
                          initial=sound_manager.music_volume * 100, **slider_params))
    y_pos += settings.SLIDER_Y_SPACING
    sliders.append(Slider(surface, slider_x, y_pos, settings.SLIDER_WIDTH, settings.SLIDER_HEIGHT,
                          initial=sound_manager.sfx_volume * 100, **slider_params))

    if menu_screen.BUTTON_FONT_MENU:  # Upewnij się, że czcionka z menu jest załadowana
        back_button = Button(
            x=(screen_width - settings.INSTRUCTIONS_BACK_BUTTON_WIDTH) // 2,
            y=screen_height + settings.INSTRUCTIONS_BACK_BUTTON_Y_OFFSET,
            # Powinno być np. y_pos + settings.SLIDER_Y_SPACING
            width=settings.INSTRUCTIONS_BACK_BUTTON_WIDTH, height=settings.INSTRUCTIONS_BACK_BUTTON_HEIGHT,
            text="Powrót", font=menu_screen.BUTTON_FONT_MENU,
            base_color=settings.MENU_BUTTON_BASE_COLOR, hover_color=settings.MENU_BUTTON_HOVER_COLOR,
            text_color=settings.MENU_TEXT_COLOR, action="CLOSE_OVERLAY", border_radius=15
        )

    hide_sliders()  # Domyślnie ukryj suwaki i ustaw flagę `is_active`


def handle_settings_input(events_list, mouse_pos):
    """Obsługuje input TYLKO dla przycisku 'Powrót'. Suwaki obsługuje pygame_widgets.update()."""
    for event in events_list:  # Iterujemy po liście zdarzeń
        if back_button and back_button.handle_event(event, mouse_pos):
            return "CLOSE_OVERLAY"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "CLOSE_OVERLAY"
    return None


def update_volumes_from_sliders():
    """ODCZYTUJE wartości z suwaków i ustawia głośność. Wywoływana w pętli głównej."""
    if sliders and len(sliders) == 3 and is_active:  # Sprawdzaj naszą flagę `is_active`
        new_master_val = sliders[0].getValue() / 100.0
        new_music_val = sliders[1].getValue() / 100.0
        new_sfx_val = sliders[2].getValue() / 100.0

        if abs(new_master_val - sound_manager.master_volume) > 0.001:
            sound_manager.set_master_volume(new_master_val * 100)
        if abs(new_music_val - sound_manager.music_volume) > 0.001 or abs(
                new_master_val - sound_manager.master_volume) > 0.001:
            sound_manager.set_music_volume(new_music_val * 100)
        if abs(new_sfx_val - sound_manager.sfx_volume) > 0.001 or abs(
                new_master_val - sound_manager.master_volume) > 0.001:
            sound_manager.set_sfx_volume(new_sfx_val * 100)


def hide_sliders():
    global is_active
    is_active = False
    for slider in sliders: slider.hide()


def show_sliders():
    global is_active
    is_active = True
    for slider in sliders: slider.show()


def draw_settings_screen(surface, mouse_pos):
    """Rysuje elementy ekranu ustawień (tło, etykiety, przycisk). Suwaki są rysowane przez pygame_widgets.update()."""
    # Tło dla ekranu ustawień jest rysowane w main.py (przyciemnienie + ewentualne tło z menu/gry)

    if title_font and header_font:
        title_rect = pygame.Rect(0, settings.INSTRUCTIONS_TITLE_Y - 40, surface.get_width(), 100)
        text_utility.render_text(
            surface=surface, text="Ustawienia Dźwięku",
            font_path=settings.FONT_PATH_PT_SERIF_REGULAR,
            initial_font_size=settings.INSTRUCTIONS_TITLE_FONT_SIZE,
            color=settings.INSTRUCTIONS_TITLE_COLOR,
            rect=title_rect,
            outline_color=settings.INSTRUCTIONS_OUTLINE_COLOR,
            outline_width=settings.INSTRUCTIONS_OUTLINE_WIDTH
        )

        labels = ["Głośność Ogólna", "Głośność Muzyki", "Głośność Efektów"]
        for i, slider in enumerate(sliders):
            # Etykiety rysujemy zawsze, gdy ten ekran jest rysowany
            # Widoczność samych suwaków jest kontrolowana przez slider.show/hide()
            label_rect = pygame.Rect(slider.getX(), slider.getY() - 50, slider.getWidth(), 40)
            text_utility.render_text(
                surface=surface, text=labels[i],
                font_path=settings.FONT_PATH_PT_SERIF_REGULAR,
                initial_font_size=settings.INSTRUCTIONS_HEADER_FONT_SIZE,
                color=settings.INSTRUCTIONS_HEADER_COLOR,
                rect=label_rect,
                outline_color=settings.INSTRUCTIONS_OUTLINE_COLOR,
                outline_width=settings.INSTRUCTIONS_OUTLINE_WIDTH
            )

    if back_button:
        back_button.update_hover(mouse_pos)
        back_button.draw(surface)