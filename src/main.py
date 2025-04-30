import pygame
import sys

# Inicjalizacja Pygame
pygame.init()

# Ustawienia Okna
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Wyścig po Zaliczenie"
BG_COLOR = (210, 180, 140) # Kolor tła (Tan)

# Utworzenie okna
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

# Zegar FPS
clock = pygame.time.Clock()
FPS = 60

# Główna Pętla Gry
running = True
while running:
    # Obsługa Zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Zamknięcie okna
            running = False
        # TODO: Obsługa innych zdarzeń (mysz, klawiatura)

    # Aktualizacja Logiki Gry
    # TODO: Logika ruchu, stany gry itp.

    # Rysowanie na Ekranie
    screen.fill(BG_COLOR) # Czyść ekran tłem

    # TODO: Rysowanie planszy, pionków, UI itp.

    # Aktualizacja wyświetlania
    pygame.display.flip()

    # Utrzymanie FPS
    clock.tick(FPS)

# Zakończenie Pygame
pygame.quit()
sys.exit() # Bezpieczne wyjście