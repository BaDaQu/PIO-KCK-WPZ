# src/pawn.py
import pygame
import os
import settings


class Pawn(pygame.sprite.Sprite):
    def __init__(self, image_path, initial_board_field_index, board_ref):
        super().__init__()
        self.board_field_index = initial_board_field_index
        self.board = board_ref
        self.pawn_id = id(self)

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

    def update_position_on_board_with_sharing(self, field_index, pawns_on_this_field_ids):
        self.board_field_index = field_index
        field_screen_rect = self.board.get_field_screen_rect(self.board_field_index)

        if not field_screen_rect:
            self.rect.topleft = (0, 0)
            return

        num_pawns_on_field = len(pawns_on_this_field_ids)

        current_pawn_index_on_field = -1
        try:
            current_pawn_index_on_field = pawns_on_this_field_ids.index(self.pawn_id)
        except ValueError:
            # To nie powinno się zdarzyć, jeśli logika mapowania jest poprawna
            # Jeśli się zdarzy, pionek zostanie potraktowany jakby był pierwszy (lub jedyny)
            # print(f"OSTRZEŻENIE: Pionek {self.pawn_id} nie znaleziony na liście {pawns_on_this_field_ids} dla pola {field_index}")
            pass

        if num_pawns_on_field <= 0:
            self.rect.center = field_screen_rect.center
        elif num_pawns_on_field == 1:
            self.rect.center = field_screen_rect.center
        elif num_pawns_on_field == 2:
            spacing = self.pawn_render_width // 4
            total_pawns_area_width = self.pawn_render_width * 2 + spacing
            start_x_pawns = field_screen_rect.centerx - total_pawns_area_width // 2

            # Używamy current_pawn_index_on_field (który będzie 0 lub 1)
            if current_pawn_index_on_field == 0 or current_pawn_index_on_field == -1:  # -1 jako fallback
                self.rect.left = start_x_pawns
            else:  # current_pawn_index_on_field == 1
                self.rect.left = start_x_pawns + self.pawn_render_width + spacing
            self.rect.centery = field_screen_rect.centery
        else:  # Dla 3+ pionków
            offset_increment = 5
            # Używamy current_pawn_index_on_field (0, 1, 2...)
            # Jeśli current_pawn_index_on_field to -1, potraktuj jak 0
            effective_index = current_pawn_index_on_field if current_pawn_index_on_field != -1 else 0

            self.rect.centerx = field_screen_rect.centerx + int(
                (effective_index - (num_pawns_on_field - 1) / 2) * offset_increment)
            self.rect.centery = field_screen_rect.centery + int(
                (effective_index - (num_pawns_on_field - 1) / 2) * offset_increment)


class PlayerPawn(Pawn):
    def __init__(self, player_id, image_path, initial_board_field_index, board_ref):
        super().__init__(image_path, initial_board_field_index, board_ref)
        self.player_id_num = player_id
        self.pawn_id = f"player_{player_id}"  # Użyj string ID
        print(f"Utworzono pionek gracza {self.player_id_num} (ID: {self.pawn_id})")


class ProfessorPawn(Pawn):
    def __init__(self, image_path, initial_board_field_index, board_ref):
        super().__init__(image_path, initial_board_field_index, board_ref)
        self.pawn_id = "professor"
        print(f"Utworzono pionek Profesora (ID: {self.pawn_id})")