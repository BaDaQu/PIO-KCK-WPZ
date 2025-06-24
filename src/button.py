# src/button.py
import pygame
import settings


class Button:
    def __init__(self, x, y, width, height, text, font,
                 base_color, hover_color, text_color, action=None, border_radius=15, image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.action = action
        self.border_radius = border_radius
        self.is_hovered = False

        self.image = None
        self.text_surface = None
        self.text_rect = None

        if image:
            # Jeśli przekazano obrazek, skalujemy go do rozmiaru przycisku
            try:
                self.image = pygame.transform.scale(image, (width, height))
            except Exception as e:
                print(f"Błąd skalowania obrazka dla przycisku: {e}")
                self.image = None  # W razie błędu, wracamy do braku obrazka

        # Jeśli nie ma obrazka, ale jest tekst i czcionka, przygotuj tekst
        if not self.image and self.font and self.text:
            self.text_surface = self.font.render(self.text, True, self.text_color)
            self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def handle_event(self, event, mouse_pos):
        """Obsługuje zdarzenia dla przycisku (np. kliknięcie). Zwraca akcję, jeśli została wykonana."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(mouse_pos):
                return self.action
        return None

    def update_hover(self, mouse_pos):
        """Aktualizuje stan najechania myszką."""
        if self.rect.collidepoint(mouse_pos):
            self.is_hovered = True
        else:
            self.is_hovered = False

    def draw(self, surface):
        """Rysuje przycisk na podanej powierzchni."""
        current_color = self.hover_color if self.is_hovered else self.base_color
        # Rysuj tło tylko, jeśli ma jakąś przezroczystość (nie jest w pełni transparentne)
        # To ważne dla przycisków-ikonek, które mają przezroczyste tło bazowe
        if len(current_color) == 4 and current_color[3] > 0:
            pygame.draw.rect(surface, current_color, self.rect, border_radius=self.border_radius)
        elif len(current_color) == 3:  # Kolory bez alfy zawsze rysujemy
            pygame.draw.rect(surface, current_color, self.rect, border_radius=self.border_radius)

        # Rysuj obrazek LUB tekst, w zależności od tego, co jest dostępne
        if self.image:
            surface.blit(self.image, self.rect.topleft)
        elif self.text_surface and self.text_rect:
            surface.blit(self.text_surface, self.text_rect)