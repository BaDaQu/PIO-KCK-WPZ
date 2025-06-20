# src/effects.py
import pygame
import settings


class FloatingText:
    def __init__(self, x, y, text, font, color, duration_seconds=1.0, speed_y=-30):
        self.x = x
        self.y = y
        self.initial_y = y
        self.text = text
        self.font = font
        self.color = color
        self.duration = duration_seconds
        self.speed_y = speed_y  # Prędkość w pikselach na sekundę
        self.alpha = 255  # Początkowa przezroczystość
        self.timer = 0.0
        self.is_alive = True

        self.text_surface = self.font.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect(center=(self.x, self.y))

    def update(self, dt_seconds):
        if not self.is_alive:
            return

        self.timer += dt_seconds
        if self.timer >= self.duration:
            self.is_alive = False
            return

        # Przesuń tekst w górę
        self.y += self.speed_y * dt_seconds
        self.rect.centery = int(self.y)

        # Znikaj pod koniec animacji
        # Zacznij znikać w drugiej połowie czasu trwania
        if self.timer > self.duration / 2:
            time_passed_fade = self.timer - self.duration / 2
            fade_duration = self.duration / 2
            self.alpha = 255 * (1 - (time_passed_fade / fade_duration))
            self.alpha = max(0, int(self.alpha))

        # Aktualizuj powierzchnię tekstu z nową alfą
        self.text_surface.set_alpha(self.alpha)

    def draw(self, surface):
        if self.is_alive:
            surface.blit(self.text_surface, self.rect)