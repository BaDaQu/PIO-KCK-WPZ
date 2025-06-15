# src/player_widget.py
import pygame
import settings


class PlayerInfoWidget:
    def __init__(self, x, y, player_name, font, image_path):
        self.player_name = player_name
        self.is_active_turn = False
        self.font = font

        try:
            self.base_image = pygame.image.load(image_path).convert_alpha()
            self.base_image = pygame.transform.scale(self.base_image,
                                                     (settings.PLAYER_WIDGET_WIDTH, settings.PLAYER_WIDGET_HEIGHT))
        except Exception as e:
            print(f"Błąd ładowania obrazka widgetu gracza ze ścieżki '{image_path}': {e}")
            self.base_image = pygame.Surface((settings.PLAYER_WIDGET_WIDTH, settings.PLAYER_WIDGET_HEIGHT))
            self.base_image.fill((100, 100, 100))

        self.widget_rect = self.base_image.get_rect(topleft=(x, y))

        self.name_text_surface = self.font.render(self.player_name, True, settings.MENU_TEXT_COLOR)

        self.name_text_rect = self.name_text_surface.get_rect(
            centery=self.widget_rect.centery + settings.PLAYER_WIDGET_TEXT_Y_OFFSET,
            left=self.widget_rect.left + settings.PLAYER_WIDGET_TEXT_X_PADDING
        )

    def set_active(self, is_active):
        """Ustawia, czy ten gracz ma teraz turę."""
        self.is_active_turn = is_active

    def draw(self, surface):
        """Rysuje widget na podanej powierzchni."""
        surface.blit(self.base_image, self.widget_rect)

        surface.blit(self.name_text_surface, self.name_text_rect)

        if self.is_active_turn:
            highlight_rect = self.widget_rect.inflate(6, 6)
            pygame.draw.rect(surface, settings.PANEL_BUTTON_HOVER_COLOR, highlight_rect, 4, border_radius=12)