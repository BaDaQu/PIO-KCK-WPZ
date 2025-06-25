# src/player_widget.py
import pygame
import settings
from effects import FloatingText
import random
import math


class PlayerInfoWidget:
    def __init__(self, x, y, player_id, player_name, image_path, ects_icon_path, heart_icon_path,
                 empty_heart_icon_path):
        super().__init__()
        self.player_id = player_id
        self.player_name = player_name
        self.points = 0
        self.lives = settings.INITIAL_PLAYER_LIVES
        self.is_active_turn = False
        self.floating_texts = []

        self.is_shaking = False
        self.shake_timer = 0.0
        self.shake_offset = (0, 0)
        self.next_shake_time = 0.0
        self.is_pulsing_life_gain = False
        self.pulse_life_gain_timer = 0.0
        self.life_to_pulse_index = -1
        self.active_turn_pulse_timer = 0.0

        try:
            self.name_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR,
                                              settings.PLAYER_WIDGET_NAME_FONT_SIZE)
            self.points_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR,
                                                settings.PLAYER_WIDGET_POINTS_FONT_SIZE)
        except Exception as e:
            self.name_font = pygame.font.SysFont(None, settings.PLAYER_WIDGET_NAME_FONT_SIZE);
            self.points_font = pygame.font.SysFont(None, settings.PLAYER_WIDGET_POINTS_FONT_SIZE)

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
        if not is_active:
            self.active_turn_pulse_timer = 0.0

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
            self.is_shaking = True;
            self.shake_timer = 0.0;
            self.next_shake_time = 0.0

    def start_gain_life_animation(self, life_index):
        if not self.is_pulsing_life_gain:
            self.is_pulsing_life_gain = True;
            self.pulse_life_gain_timer = 0.0;
            self.life_to_pulse_index = life_index

    def update(self, dt_seconds):
        self.floating_texts = [ft for ft in self.floating_texts if ft.is_alive]
        for ft in self.floating_texts: ft.update(dt_seconds)

        if self.is_shaking:
            self.shake_timer += dt_seconds;
            self.next_shake_time -= dt_seconds
            if self.next_shake_time <= 0:
                self.next_shake_time = settings.WIDGET_SHAKE_FREQUENCY
                intensity = settings.WIDGET_SHAKE_INTENSITY
                self.shake_offset = (random.randint(-intensity, intensity), random.randint(-intensity, intensity))
            if self.shake_timer >= settings.WIDGET_SHAKE_DURATION_SECONDS:
                self.is_shaking = False;
                self.shake_offset = (0, 0)

        if self.is_pulsing_life_gain:
            self.pulse_life_gain_timer += dt_seconds
            if self.pulse_life_gain_timer >= settings.WIDGET_PULSE_DURATION_SECONDS:
                self.is_pulsing_life_gain = False;
                self.life_to_pulse_index = -1

        if self.is_active_turn:
            self.active_turn_pulse_timer = (
                                                       self.active_turn_pulse_timer + dt_seconds) % settings.ACTIVE_TURN_PULSE_DURATION_SECONDS

    def draw(self, surface):
        current_widget_rect_pos = (self.widget_rect.left + self.shake_offset[0],
                                   self.widget_rect.top + self.shake_offset[1])

        surface.blit(self.base_image, current_widget_rect_pos)
        # Elementy tekstowe i ikony rysujemy względem przesuniętego widget_rect
        name_text_draw_rect = self.name_text_rect.move(self.shake_offset)
        surface.blit(self.name_text_surface, name_text_draw_rect)

        ects_icon_draw_rect = self.ects_icon_rect.move(self.shake_offset)
        surface.blit(self.ects_icon_image, ects_icon_draw_rect)

        points_text_surface = self.points_font.render(str(self.points), True, settings.MENU_TEXT_COLOR)
        points_text_rect = points_text_surface.get_rect(
            midleft=(ects_icon_draw_rect.right + settings.PLAYER_WIDGET_ECTS_TEXT_X_OFFSET,
                     ects_icon_draw_rect.centery))
        surface.blit(points_text_surface, points_text_rect)

        for i in range(settings.INITIAL_PLAYER_LIVES):
            heart_x_base = self.widget_rect.left + settings.PLAYER_WIDGET_HEARTS_START_X
            heart_y_base = self.widget_rect.top + settings.PLAYER_WIDGET_HEARTS_Y
            heart_x = heart_x_base + i * (
                        settings.PLAYER_WIDGET_HEART_ICON_SIZE + settings.PLAYER_WIDGET_HEARTS_SPACING)
            heart_y = heart_y_base

            image_to_draw = self.heart_full_image if i < self.lives else self.heart_empty_image
            heart_draw_pos = (heart_x + self.shake_offset[0], heart_y + self.shake_offset[1])

            if self.is_pulsing_life_gain and i == self.life_to_pulse_index:
                scale_factor = 1.0 + (settings.WIDGET_PULSE_SCALE_MAX - 1.0) * abs(
                    math.sin(self.pulse_life_gain_timer * settings.WIDGET_PULSE_SPEED))
                pulsed_size = (int(settings.PLAYER_WIDGET_HEART_ICON_SIZE * scale_factor),
                               int(settings.PLAYER_WIDGET_HEART_ICON_SIZE * scale_factor))
                pulsed_image = pygame.transform.smoothscale(image_to_draw, pulsed_size)
                pulsed_rect = pulsed_image.get_rect(
                    center=(heart_draw_pos[0] + settings.PLAYER_WIDGET_HEART_ICON_SIZE // 2,
                            heart_draw_pos[1] + settings.PLAYER_WIDGET_HEART_ICON_SIZE // 2))
                surface.blit(pulsed_image, pulsed_rect)
            else:
                surface.blit(image_to_draw, heart_draw_pos)

        # --- ZMIENIONA LOGIKA PODŚWIETLENIA AKTYWNEJ TURY ---
        if self.is_active_turn and not self.is_shaking:
            progress = (self.active_turn_pulse_timer / settings.ACTIVE_TURN_PULSE_DURATION_SECONDS)
            # Sinusoida dla płynnego pulsowania (od 0 do 1 i z powrotem do 0)
            # Mnożymy przez pi, aby uzyskać pełny cykl sinusa (0 -> 1 -> 0)
            pulse_value = math.sin(progress * math.pi)

            # Pulsowanie przezroczystością
            alpha = settings.ACTIVE_TURN_PULSE_MIN_ALPHA + pulse_value * (
                        settings.ACTIVE_TURN_PULSE_MAX_ALPHA - settings.ACTIVE_TURN_PULSE_MIN_ALPHA)
            alpha = int(max(0, min(255, alpha)))

            # Pulsowanie rozmiarem ramki (subtelne)
            # Możemy użyć tego samego pulse_value, aby ramka była grubsza w "szczycie" alfy
            # lub odwrotnie. Tutaj zrobimy, że ramka jest najgrubsza, gdy alfa jest najwyższa.
            border_width_variation = int(pulse_value * (
                        settings.ACTIVE_TURN_PULSE_BORDER_WIDTH_MAX - settings.ACTIVE_TURN_PULSE_BORDER_WIDTH_MIN))
            current_border_width = settings.ACTIVE_TURN_PULSE_BORDER_WIDTH_MIN + border_width_variation
            current_border_width = max(1, current_border_width)  # Ramka musi mieć co najmniej 1px

            color_tuple = settings.ACTIVE_TURN_PULSE_COLOR
            if len(color_tuple) == 3:
                color_with_alpha = (*color_tuple, alpha)
            else:
                color_with_alpha = (*color_tuple[:3], alpha)

            # Prostokąt ramki, nieco większy niż widget
            highlight_rect = self.widget_rect.inflate(6, 6)
            # Rysujemy ramkę bezpośrednio na głównej powierzchni, ale z uwzględnieniem shake_offset
            pygame.draw.rect(surface, color_with_alpha, highlight_rect.move(self.shake_offset),
                             current_border_width,
                             border_radius=settings.ACTIVE_TURN_PULSE_BORDER_RADIUS)
        # ------------------------------------------------------------------

        for ft in self.floating_texts:
            original_ft_rect_center = ft.rect.center
            ft.rect.center = (original_ft_rect_center[0] + self.shake_offset[0],
                              original_ft_rect_center[1] + self.shake_offset[1])
            ft.draw(surface)
            ft.rect.center = original_ft_rect_center