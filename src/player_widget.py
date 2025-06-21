# src/player_widget.py
import pygame
import settings
from effects import FloatingText
import random
import math


class PlayerInfoWidget:
    def __init__(self, x, y, player_id, player_name, image_path, ects_icon_path, heart_icon_path,
                 empty_heart_icon_path):
        self.player_id = player_id
        self.player_name = player_name
        self.points = 0
        self.lives = settings.INITIAL_PLAYER_LIVES
        self.is_active_turn = False
        self.floating_texts = []

        # Atrybuty do animacji
        self.is_shaking = False
        self.shake_timer = 0.0
        self.shake_offset = (0, 0)
        self.next_shake_time = 0.0
        self.is_pulsing = False
        self.pulse_timer = 0.0
        self.life_to_pulse_index = -1

        # Ładowanie czcionek
        try:
            self.name_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR,
                                              settings.PLAYER_WIDGET_NAME_FONT_SIZE)
            self.points_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR,
                                                settings.PLAYER_WIDGET_POINTS_FONT_SIZE)
        except Exception as e:
            self.name_font = pygame.font.SysFont(None, settings.PLAYER_WIDGET_NAME_FONT_SIZE);
            self.points_font = pygame.font.SysFont(None, settings.PLAYER_WIDGET_POINTS_FONT_SIZE)

        # Ładowanie obrazków
        try:
            self.base_image = pygame.image.load(image_path).convert_alpha()
            self.base_image = pygame.transform.scale(self.base_image,
                                                     (settings.PLAYER_WIDGET_WIDTH, settings.PLAYER_WIDGET_HEIGHT))
        except Exception as e:
            self.base_image = pygame.Surface((settings.PLAYER_WIDGET_WIDTH, settings.PLAYER_WIDGET_HEIGHT));
            self.base_image.fill((100, 100, 100))
        try:
            self.ects_icon_image = pygame.image.load(ects_icon_path).convert_alpha()
            self.ects_icon_image = pygame.transform.scale(self.ects_icon_image, (settings.PLAYER_WIDGET_ECTS_ICON_SIZE,
                                                                                 settings.PLAYER_WIDGET_ECTS_ICON_SIZE))
        except Exception as e:
            self.ects_icon_image = pygame.Surface(
                (settings.PLAYER_WIDGET_ECTS_ICON_SIZE, settings.PLAYER_WIDGET_ECTS_ICON_SIZE));
            self.ects_icon_image.fill((255, 255, 0))
        try:
            self.heart_full_image = pygame.image.load(heart_icon_path).convert_alpha()
            self.heart_full_image = pygame.transform.scale(self.heart_full_image,
                                                           (settings.PLAYER_WIDGET_HEART_ICON_SIZE,
                                                            settings.PLAYER_WIDGET_HEART_ICON_SIZE))
        except Exception as e:
            self.heart_full_image = pygame.Surface(
                (settings.PLAYER_WIDGET_HEART_ICON_SIZE, settings.PLAYER_WIDGET_HEART_ICON_SIZE));
            self.heart_full_image.fill((255, 20, 147))
        try:
            self.heart_empty_image = pygame.image.load(empty_heart_icon_path).convert_alpha()
            self.heart_empty_image = pygame.transform.scale(self.heart_empty_image,
                                                            (settings.PLAYER_WIDGET_HEART_ICON_SIZE,
                                                             settings.PLAYER_WIDGET_HEART_ICON_SIZE))
        except Exception as e:
            self.heart_empty_image = pygame.Surface(
                (settings.PLAYER_WIDGET_HEART_ICON_SIZE, settings.PLAYER_WIDGET_HEART_ICON_SIZE));
            self.heart_empty_image.fill((50, 50, 50))

        # Pozycjonowanie
        self.widget_rect = self.base_image.get_rect(topleft=(x, y))
        self.name_text_surface = self.name_font.render(self.player_name, True, settings.MENU_TEXT_COLOR)
        self.name_text_rect = self.name_text_surface.get_rect(
            centery=self.widget_rect.centery + settings.PLAYER_WIDGET_TEXT_Y_OFFSET,
            left=self.widget_rect.left + settings.PLAYER_WIDGET_TEXT_X_PADDING)
        self.ects_icon_rect = self.ects_icon_image.get_rect(
            left=self.widget_rect.left + settings.PLAYER_WIDGET_ECTS_ICON_X,
            top=self.widget_rect.top + settings.PLAYER_WIDGET_ECTS_ICON_Y)

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

    def start_lose_life_animation(self):
        if not self.is_shaking:
            self.is_shaking = True
            self.shake_timer = 0.0

    def start_gain_life_animation(self, life_index):
        if not self.is_pulsing:
            self.is_pulsing = True
            self.pulse_timer = 0.0
            self.life_to_pulse_index = life_index

    def update(self, dt_seconds):
        self.floating_texts = [ft for ft in self.floating_texts if ft.is_alive]
        for ft in self.floating_texts:
            ft.update(dt_seconds)

        if self.is_shaking:
            self.shake_timer += dt_seconds
            self.next_shake_time -= dt_seconds
            if self.next_shake_time <= 0:
                self.next_shake_time = settings.WIDGET_SHAKE_FREQUENCY
                intensity = settings.WIDGET_SHAKE_INTENSITY
                self.shake_offset = (random.randint(-intensity, intensity), random.randint(-intensity, intensity))
            if self.shake_timer >= settings.WIDGET_SHAKE_DURATION_SECONDS:
                self.is_shaking = False
                self.shake_offset = (0, 0)

        if self.is_pulsing:
            self.pulse_timer += dt_seconds
            if self.pulse_timer >= settings.WIDGET_PULSE_DURATION_SECONDS:
                self.is_pulsing = False
                self.life_to_pulse_index = -1

    def draw(self, surface):
        draw_rect = self.widget_rect.move(self.shake_offset)

        surface.blit(self.base_image, draw_rect)
        surface.blit(self.name_text_surface, self.name_text_rect.move(self.shake_offset))
        surface.blit(self.ects_icon_image, self.ects_icon_rect.move(self.shake_offset))

        points_text_surface = self.points_font.render(str(self.points), True, settings.MENU_TEXT_COLOR)
        points_text_rect = points_text_surface.get_rect(
            midleft=(self.ects_icon_rect.right + settings.PLAYER_WIDGET_ECTS_TEXT_X_OFFSET,
                     self.ects_icon_rect.centery))
        surface.blit(points_text_surface, points_text_rect.move(self.shake_offset))

        for i in range(settings.INITIAL_PLAYER_LIVES):
            heart_x = self.widget_rect.left + settings.PLAYER_WIDGET_HEARTS_START_X + i * (
                        settings.PLAYER_WIDGET_HEART_ICON_SIZE + settings.PLAYER_WIDGET_HEARTS_SPACING)
            heart_y = self.widget_rect.top + settings.PLAYER_WIDGET_HEARTS_Y
            image_to_draw = self.heart_full_image if i < self.lives else self.heart_empty_image

            if self.is_pulsing and i == self.life_to_pulse_index:
                scale_factor = 1.0 + (settings.WIDGET_PULSE_SCALE_MAX - 1.0) * abs(
                    math.sin(self.pulse_timer * settings.WIDGET_PULSE_SPEED))
                pulsed_size = (int(settings.PLAYER_WIDGET_HEART_ICON_SIZE * scale_factor),
                               int(settings.PLAYER_WIDGET_HEART_ICON_SIZE * scale_factor))
                pulsed_image = pygame.transform.scale(image_to_draw, pulsed_size)
                pulsed_rect = pulsed_image.get_rect(center=(heart_x + settings.PLAYER_WIDGET_HEART_ICON_SIZE // 2,
                                                            heart_y + settings.PLAYER_WIDGET_HEART_ICON_SIZE // 2))
                surface.blit(pulsed_image, pulsed_rect.move(self.shake_offset))
            else:
                surface.blit(image_to_draw, (heart_x + self.shake_offset[0], heart_y + self.shake_offset[1]))

        if self.is_active_turn and not self.is_shaking:
            highlight_rect = self.widget_rect.inflate(6, 6)
            pygame.draw.rect(surface, settings.PANEL_BUTTON_HOVER_COLOR, highlight_rect, 4, border_radius=12)

        for ft in self.floating_texts:
            ft.draw(surface)