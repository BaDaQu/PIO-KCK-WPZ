# src/button.py
import pygame

class Button:
    def __init__(self, x, y, width, height, text, font,
                 base_color, hover_color, text_color, action=None, border_radius=15):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.action = action
        self.border_radius = border_radius
        self.is_hovered = False
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(mouse_pos):
                return self.action
        return None

    def update_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos): self.is_hovered = True
        else: self.is_hovered = False

    def draw(self, surface):
        current_color = self.hover_color if self.is_hovered else self.base_color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=self.border_radius)
        surface.blit(self.text_surface, self.text_rect)