import pygame
import sys

# --- Inicjalizacja Pygame ---
pygame.init()

# --- Ustawienia Okna Gry ---
SCREEN_WIDTH = 1436
SCREEN_HEIGHT = 950  
SCREEN_TITLE = "Wyścig po Zaliczenie"

# Ustawienie tytułu okna
pygame.display.set_caption(SCREEN_TITLE)

# Utworzenie okna/powierzchni wyświetlania
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# --- Kolory (RGB) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (240, 190, 100)  # Kolor przycisków z makiety (przybliżony)
BUTTON_HOVER_COLOR = (255, 210, 120)  # Jaśniejszy kolor przy najechaniu
TEXT_COLOR = (80, 50, 20)  # Ciemnobrązowy kolor tekstu

# --- Czcionki ---
try:
    TITLE_FONT = pygame.font.Font("../assets/fonts/PTSerif-Regular.ttf", 90)
    BUTTON_FONT = pygame.font.Font("../assets/fonts/PTSerif-Regular.ttf", 40)
except pygame.error as e:
    print(f"Błąd ładowania czcionki: {e}")
    # Użyj domyślnej czcionki, jeśli plik nie zostanie znaleziony
    TITLE_FONT = pygame.font.SysFont(None, 100)
    BUTTON_FONT = pygame.font.SysFont(None, 50)

# --- Ładowanie Zasobów Graficznych ---
try:
    menu_background_img = pygame.image.load("../assets/images/MENU_GLOWNE.png").convert()
    # Skalowanie tła do rozmiaru ekranu
    menu_background_img = pygame.transform.scale(menu_background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Błąd ładowania obrazka tła: {e}")
    menu_background_img = None  # Użyjemy koloru tła, jeśli obrazek się nie załaduje

# === Ustawianie Ikony Okna ===
try:
    icon_path = "../assets/images/IKONA_GRY.png"
    game_icon = pygame.image.load(icon_path)
    pygame.display.set_icon(game_icon)
    print("Ikona okna została ustawiona.")  # Debug
except pygame.error as e:
    print(f"Błąd ładowania ikony okna: {e}")
except FileNotFoundError:
    print(f"Nie znaleziono pliku ikony: {icon_path}")

# --- Definicje Przycisków (jako prostokąty i tekst) ---
# Pozycje i rozmiary przycisków
button_width = 470
button_height = 105
button_spacing = 23   # Odstęp między przyciskami

# Przycisk "NOWA GRA"
new_game_text_surface = BUTTON_FONT.render("NOWA GRA", True, TEXT_COLOR)
new_game_button_rect = pygame.Rect(
    (SCREEN_WIDTH - button_width) - 140,
    SCREEN_HEIGHT - 260 - button_height - button_spacing,  # Pozycja Y pierwszego przycisku
    button_width,
    button_height
)

# Przycisk "INSTRUKCJA"
instructions_text_surface = BUTTON_FONT.render("INSTRUKCJA", True, TEXT_COLOR)
instructions_button_rect = pygame.Rect(
    new_game_button_rect.left,
    new_game_button_rect.bottom + button_spacing,
    button_width,
    button_height
)

# Przycisk "WYJDŹ"
exit_text_surface = BUTTON_FONT.render("WYJDŹ", True, TEXT_COLOR)
exit_button_rect = pygame.Rect(
    instructions_button_rect.left,
    instructions_button_rect.bottom + button_spacing,
    button_width,
    button_height
)

buttons = [
    {"rect": new_game_button_rect, "text_surface": new_game_text_surface, "action": "GAMEPLAY"},
    {"rect": instructions_button_rect, "text_surface": instructions_text_surface, "action": "INSTRUCTIONS"},
    {"rect": exit_button_rect, "text_surface": exit_text_surface, "action": "QUIT"}
]

# --- Zegar do kontroli FPS ---
clock = pygame.time.Clock()
FPS = 60

# --- Stany Gry ---
game_state = "MENU_GLOWNE"  # Możliwe stany: "MENU_GLOWNE", "GAMEPLAY", "INSTRUCTIONS", "GAME_OVER" itd.


# --- Funkcja do rysowania przycisku ---
def draw_button(surface, button_info, mouse_pos):
    rect = button_info["rect"]
    text_surface = button_info["text_surface"]
    color = BUTTON_COLOR
    if rect.collidepoint(mouse_pos):
        color = BUTTON_HOVER_COLOR  # Zmiana koloru przy najechaniu

    pygame.draw.rect(surface, color, rect, border_radius=15)  # Rysowanie prostokąta przycisku
    # Wyśrodkowanie tekstu na przycisku
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


# --- Główna Pętla Gry ---
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()  # Pobierz pozycję myszy raz na klatkę

    # 1. Obsługa Zdarzeń (Input)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "MENU_GLOWNE":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Lewy przycisk myszy
                    for button in buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            if button["action"] == "GAMEPLAY":
                                game_state = "GAMEPLAY"
                                print("Przełączam stan na GAMEPLAY")  # Debug
                            elif button["action"] == "INSTRUCTIONS":
                                game_state = "INSTRUCTIONS"
                                print("Przełączam stan na INSTRUCTIONS")  # Debug
                            elif button["action"] == "QUIT":
                                running = False

        # TODO: Obsługa zdarzeń dla innych stanów gry (GAMEPLAY, INSTRUCTIONS)

    # 2. Aktualizacja Stanu Gry (Logika)
    if game_state == "MENU_GLOWNE":
        # Logika specyficzna dla menu (jeśli potrzebna)
        pass
    elif game_state == "GAMEPLAY":
        # TODO: Logika rozgrywki
        pass
    elif game_state == "INSTRUCTIONS":
        # TODO: Logika ekranu instrukcji
        pass
    # itd.

    # 3. Rysowanie na Ekranie (Renderowanie)
    screen.fill(BLACK)  # Wypełnienie czarnym tłem na wszelki wypadek

    if game_state == "MENU_GLOWNE":
        # Rysowanie tła menu
        if menu_background_img:
            screen.blit(menu_background_img, (0, 0))
        else:
            screen.fill((200, 180, 160))  # Alternatywny kolor tła, jeśli obrazek się nie załaduje



        # Rysowanie przycisków
        for button in buttons:
            draw_button(screen, button, mouse_pos)

    elif game_state == "GAMEPLAY":
        screen.fill((50, 150, 50))  # Przykładowe tło dla rozgrywki (zielone)
        gameplay_text = BUTTON_FONT.render("Stan: ROZGRYWKA (TODO)", True, WHITE)
        screen.blit(gameplay_text, (50, 50))
        # TODO: Rysowanie planszy, pionków itp.

    elif game_state == "INSTRUCTIONS":
        screen.fill((50, 50, 150))  # Przykładowe tło dla instrukcji (niebieskie)
        instructions_text = BUTTON_FONT.render("Stan: INSTRUKCJA (TODO)", True, WHITE)
        screen.blit(instructions_text, (50, 50))
        # TODO: Rysowanie tekstu instrukcji

    # 4. Aktualizacja Wyświetlania
    pygame.display.flip()

    # 5. Kontrola FPS
    clock.tick(FPS)

# --- Zakończenie Pygame ---
pygame.quit()
sys.exit()