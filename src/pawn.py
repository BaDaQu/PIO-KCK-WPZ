# src/pawn.py
import pygame
import os
import settings
import math


class Pawn(pygame.sprite.Sprite):
    def __init__(self, image_path, initial_board_field_index, board_ref):
        super().__init__()
        self.board_field_index = initial_board_field_index
        self.board = board_ref
        self.pawn_id = id(self)

        self.is_moving = False
        self.is_repositioning = False
        self.path = []
        self.target_screen_center_pos = None
        self.current_screen_pos_float = None
        self.is_active_turn = False

        try:
            self.original_image = pygame.image.load(image_path).convert_alpha()
            original_width, original_height = self.original_image.get_size()
            if original_height == 0:
                aspect_ratio = 1
            else:
                aspect_ratio = original_width / original_height
            self.pawn_render_height = settings.PAWN_TARGET_HEIGHT
            self.pawn_render_width = int(self.pawn_render_height * aspect_ratio)
            self.image = pygame.transform.scale(self.original_image, (self.pawn_render_width, self.pawn_render_height))
            self.rect = self.image.get_rect()

        except Exception as e:
            print(f"Błąd ładowania obrazka pionka '{image_path}': {e}")
            self.image = pygame.Surface([int(settings.PAWN_TARGET_HEIGHT * 0.8), settings.PAWN_TARGET_HEIGHT])
            self.image.fill(settings.PAWN_FALLBACK_COLOR)
            self.rect = self.image.get_rect()

        initial_center_pos = self.board.get_field_screen_center(self.board_field_index)
        if initial_center_pos:
            self.rect.center = initial_center_pos
        else:
            self.rect.topleft = (0, 0)

    def set_active(self, is_active):
        """Ustawia, czy ten pionek ma teraz turę."""
        self.is_active_turn = is_active

    def draw(self, surface):
        """Rysuje pionek na podanej powierzchni."""
        # Rysujemy tylko obrazek pionka, bez żadnej obwoluty.
        surface.blit(self.image, self.rect)

    def start_move_animation(self, path_of_indices):
        if not path_of_indices: return
        self.current_screen_pos_float = list(self.rect.center)
        self.path = path_of_indices
        self.is_moving = True
        self.is_repositioning = False
        self._set_next_target_from_path()

    def _set_next_target_from_path(self):
        if self.path:
            next_field_index = self.path.pop(0)
            self.board_field_index = next_field_index
            self.target_screen_center_pos = self.board.get_field_screen_center(next_field_index)
            if not self.target_screen_center_pos:
                self.is_moving = False;
                self.path = []
        else:
            self.is_moving = False
            self.target_screen_center_pos = None

    def update_visual_position_on_field(self, field_index_param, pawns_on_this_field_ids):
        if self.is_moving: return
        self.board_field_index = field_index_param
        field_screen_rect = self.board.get_field_screen_rect(self.board_field_index)
        if not field_screen_rect: return
        num_pawns_on_field = len(pawns_on_this_field_ids)
        current_pawn_index_on_field = -1
        try:
            current_pawn_index_on_field = pawns_on_this_field_ids.index(self.pawn_id)
        except ValueError:
            pass
        target_pos = list(field_screen_rect.center)
        if num_pawns_on_field == 2:
            is_field_taller_than_wide = field_screen_rect.height > field_screen_rect.width + 10
            if is_field_taller_than_wide:
                spacing = -5;
                total_area_height = self.pawn_render_height * 2 + spacing;
                start_y = field_screen_rect.centery - total_area_height // 2
                if current_pawn_index_on_field <= 0:
                    target_pos[1] = start_y + self.pawn_render_height // 2
                else:
                    target_pos[1] = start_y + self.pawn_render_height + spacing + self.pawn_render_height // 2
            else:
                spacing = self.pawn_render_width // 3;
                total_area_width = self.pawn_render_width * 2 + spacing;
                start_x = field_screen_rect.centerx - total_area_width // 2
                if current_pawn_index_on_field <= 0:
                    target_pos[0] = start_x + self.pawn_render_width // 2
                else:
                    target_pos[0] = start_x + self.pawn_render_width + spacing + self.pawn_render_width // 2
        elif num_pawns_on_field > 2:
            offset = 6;
            effective_index = current_pawn_index_on_field if current_pawn_index_on_field != -1 else 0
            target_pos[0] = field_screen_rect.centerx + int((effective_index - (num_pawns_on_field - 1) / 2) * offset)
            target_pos[1] = field_screen_rect.centery + int(
                (effective_index - (num_pawns_on_field - 1) / 2) * offset / 2)
        if pygame.math.Vector2(self.rect.center).distance_to(target_pos) > 1:
            self.target_screen_center_pos = tuple(target_pos);
            self.current_screen_pos_float = list(self.rect.center);
            self.is_repositioning = True

    def update(self, dt):
        if not self.is_moving and not self.is_repositioning: return
        if self.target_screen_center_pos and self.current_screen_pos_float:
            target_x, target_y = self.target_screen_center_pos;
            current_x, current_y = self.current_screen_pos_float
            dx = target_x - current_x;
            dy = target_y - current_y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            move_step = settings.PAWN_MOVE_SPEED_PIXELS_PER_SECOND * dt
            if distance <= move_step or distance < 1:
                self.current_screen_pos_float = list(self.target_screen_center_pos);
                self.rect.center = tuple(int(c) for c in self.target_screen_center_pos)
                if self.is_moving:
                    self._set_next_target_from_path()
                elif self.is_repositioning:
                    self.is_repositioning = False; self.target_screen_center_pos = None
            else:
                dir_x = dx / distance if distance > 0 else 0;
                dir_y = dy / distance if distance > 0 else 0
                self.current_screen_pos_float[0] += dir_x * move_step;
                self.current_screen_pos_float[1] += dir_y * move_step
                self.rect.center = (int(self.current_screen_pos_float[0]), int(self.current_screen_pos_float[1]))


class PlayerPawn(Pawn):
    def __init__(self, player_id, image_path, initial_board_field_index, board_ref):
        super().__init__(image_path, initial_board_field_index, board_ref)
        self.player_id_num = player_id
        self.pawn_id = f"player_{player_id}"
        print(f"Utworzono pionek gracza {self.player_id_num} (ID: {self.pawn_id})")


class ProfessorPawn(Pawn):
    def __init__(self, image_path, initial_board_field_index, board_ref):
        super().__init__(image_path, initial_board_field_index, board_ref)
        self.pawn_id = "professor"
        print(f"Utworzono pionek Profesora (ID: {self.pawn_id})")   