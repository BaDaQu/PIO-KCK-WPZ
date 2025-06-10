# dice.py (wersja z animacją)

import pygame
import random

# Ustawienia z poprzednich kroków (dostosowane do Twojego projektu)
BUTTON_COLOR = (242, 182, 68)
BUTTON_TEXT_COLOR = (89, 53, 29)
FONT_SIZE = 30


class Dice:
    def __init__(self, x, y, button_width=180, button_height=60):
        self.current_roll = 1

        # --- NOWE ZMIENNE DO ANIMACJI ---
        self.is_animating = False
        self.animation_timer = 0
        self.animation_duration = 500  # Czas trwania animacji w milisekundach (0.5s)
        self.frame_timer = 0
        self.frame_duration = 50  # Jak szybko zmieniają się ścianki podczas animacji (co 50ms)
        self.animation_display_roll = 1  # Ścianka pokazywana w trakcie animacji

        # Wczytywanie grafik (pamiętaj o poprawnej ścieżce!)
        self.dice_images = {}
        for i in range(1, 7):
            try:
                img = pygame.image.load(f'../assets/images/dice{i}.png').convert_alpha()
                self.dice_images[i] = pygame.transform.scale(img, (100, 100))
            except pygame.error:
                print(f"Błąd: Nie można załadować obrazka 'assets/images/dice/dice{i}.png'.")
                self.dice_images[i] = pygame.Surface((100, 100))
                self.dice_images[i].fill((255, 0, 0))

        self.dice_display_rect = self.dice_images[1].get_rect(center=(x + button_width // 2, y - 70))

        # Konfiguracja przycisku "Rzuć Kostką"
        self.button_rect = pygame.Rect(x, y, button_width, button_height)
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.button_text_surface = self.font.render("Rzuć Kostką", True, BUTTON_TEXT_COLOR)
        self.button_text_rect = self.button_text_surface.get_rect(center=self.button_rect.center)

    def roll(self):
        """
        Losuje ostateczny wynik rzutu.
        """
        self.current_roll = random.randint(1, 6)
        print(f"Wyrzucono ostatecznie: {self.current_roll}")

    def handle_event(self, event):
        """
        Sprawdza kliknięcie i ROZPOCZYNA animację.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Rozpocznij animację tylko, jeśli nie jest już w toku
            if self.button_rect.collidepoint(event.pos) and not self.is_animating:
                self.is_animating = True
                self.animation_timer = 0  # Resetuj główny timer animacji
                return True  # Zwraca informację, że proces rzutu się rozpoczął
        return False

    def update(self, dt):
        """
        --- NOWA METODA: Aktualizuje logikę animacji w każdej klatce. ---
        'dt' to czas, jaki upłynął od ostatniej klatki.
        """
        if self.is_animating:
            self.animation_timer += dt
            self.frame_timer += dt

            # Zmieniaj pokazywaną ściankę co 'frame_duration'
            if self.frame_timer >= self.frame_duration:
                self.frame_timer = 0
                self.animation_display_roll = random.randint(1, 6)

            # Sprawdź, czy animacja dobiegła końca
            if self.animation_timer >= self.animation_duration:
                self.is_animating = False  # Zakończ animację
                self.roll()  # Wylosuj OSTATECZNY wynik

    def draw(self, screen):
        """
        Rysuje przycisk oraz odpowiednią ściankę kostki (animowaną lub końcową).
        """
        # Rysuj przycisk
        pygame.draw.rect(screen, BUTTON_COLOR, self.button_rect, border_radius=10)
        screen.blit(self.button_text_surface, self.button_text_rect)

        # --- ZMIENIONA LOGIKA RYSOWANIA ---
        # Jeśli trwa animacja, pokazuj losowe ścianki. Jeśli nie, pokazuj ostateczny wynik.
        if self.is_animating:
            image_to_draw = self.dice_images[self.animation_display_roll]
        else:
            image_to_draw = self.dice_images[self.current_roll]

        screen.blit(image_to_draw, self.dice_display_rect)