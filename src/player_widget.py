# src/player_widget.py
import pygame
import settings
from effects import FloatingText


class PlayerInfoWidget:
    def __init__(self, x, y, player_id, player_name, image_path, ects_icon_path):
        super().__init__()
        self.player_id = player_id  # <-- NOWY ATRYBUT
        self.player_name = player_name
        self.points = 0
        self.is_active_turn = False
        self.floating_texts = []

        try:
            self.name_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR,
                                              settings.PLAYER_WIDGET_NAME_FONT_SIZE)
            self.points_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR,
                                                settings.PLAYER_WIDGET_POINTS_FONT_SIZE)
        except Exception as e:
            print(f"Błąd ładowania czcionek dla widgetu gracza: {e}")
            self.name_font = pygame.font.SysFont(None, settings.PLAYER_WIDGET_NAME_FONT_SIZE)
            self.points_font = pygame.font.SysFont(None, settings.PLAYER_WIDGET_POINTS_FONT_SIZE)

        try:
            self.base_image = pygame.image.load(image_path).convert_alpha()
            self.base_image = pygame.transform.scale(self.base_image,
                                                     (settings.PLAYER_WIDGET_WIDTH, settings.PLAYER_WIDGET_HEIGHT))
        except Exception as e:
            print(f"Błąd ładowania obrazka widgetu gracza '{image_path}': {e}")
            self.base_image = pygame.Surface((settings.PLAYER_WIDGET_WIDTH, settings.PLAYER_WIDGET_HEIGHT));
            self.base_image.fill((100, 100, 100))
        try:
            self.ects_icon_image = pygame.image.load(ects_icon_path).convert_alpha()
            self.ects_icon_image = pygame.transform.scale(self.ects_icon_image, (settings.PLAYER_WIDGET_ECTS_ICON_SIZE,
                                                                                 settings.PLAYER_WIDGET_ECTS_ICON_SIZE))
        except Exception as e:
            print(f"Błąd ładowania ikony ECTS '{ects_icon_path}': {e}")
            self.ects_icon_image = pygame.Surface(
                (settings.PLAYER_WIDGET_ECTS_ICON_SIZE, settings.PLAYER_WIDGET_ECTS_ICON_SIZE));
            self.ects_icon_image.fill((255, 255, 0))

        self.widget_rect = self.base_image.get_rect(topleft=(x, y))
        self.name_text_surface = self.name_font.render(self.player_name, True, settings.MENU_TEXT_COLOR)
        self.name_text_rect = self.name_text_surface.get_rect(
            centery=self.widget_rect.centery + settings.PLAYER_WIDGET_TEXT_Y_OFFSET,
            left=self.widget_rect.left + settings.PLAYER_WIDGET_TEXT_X_PADDING
        )
        self.ects_icon_rect = self.ects_icon_image.get_rect(
            left=self.widget_rect.left + settings.PLAYER_WIDGET_ECTS_ICON_X,
            top=self.widget_rect.top + settings.PLAYER_WIDGET_ECTS_ICON_Y
        )

    def set_active(self, is_active):
        self.is_active_turn = is_active

    def start_points_animation(self, points_to_add):
        if points_to_add == 0: return
        sign = "+" if points_to_add > 0 else "";
        text = f"{sign}{points_to_add}"
        color = (34, 139, 34) if points_to_add > 0 else (220, 20, 60)
        points_text_surface = self.points_font.render(str(self.points), True, settings.MENU_TEXT_COLOR)
        points_text_rect = points_text_surface.get_rect(
            midleft=(self.ects_icon_rect.right + settings.PLAYER_WIDGET_ECTS_TEXT_X_OFFSET,
                     self.ects_icon_rect.centery))
        start_x = points_text_rect.centerx + settings.PLAYER_WIDGET_FLOATING_TEXT_X_OFFSET
        start_y = points_text_rect.centery + settings.PLAYER_WIDGET_FLOATING_TEXT_Y_OFFSET
        new_floating_text = FloatingText(start_x, start_y, text, self.points_font, color)
        self.floating_texts.append(new_floating_text)

    def update(self, dt_seconds):
        self.floating_texts = [ft for ft in self.floating_texts if ft.is_alive]
        for ft in self.floating_texts:
            ft.update(dt_seconds)

    def draw(self, surface):
        surface.blit(self.base_image, self.widget_rect)
        surface.blit(self.name_text_surface, self.name_text_rect)
        surface.blit(self.ects_icon_image, self.ects_icon_rect)
        points_text_surface = self.points_font.render(str(self.points), True, settings.MENU_TEXT_COLOR)
        points_text_rect = points_text_surface.get_rect(
            midleft=(self.ects_icon_rect.right + settings.PLAYER_WIDGET_ECTS_TEXT_X_OFFSET,
                     self.ects_icon_rect.centery))
        surface.blit(points_text_surface, points_text_rect)
        if self.is_active_turn:
            highlight_rect = self.widget_rect.inflate(6, 6)
            pygame.draw.rect(surface, settings.PANEL_BUTTON_HOVER_COLOR, highlight_rect, 4, border_radius=12)
        for ft in self.floating_texts:
            ft.draw(surface)