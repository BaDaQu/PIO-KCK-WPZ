import pygame
import os


class Pawn(pygame.sprite.Sprite):
    """Bazowa klasa dla wszystkich pionków na planszy."""

    PAWN_TARGET_HEIGHT = 50  # Stała wysokość pionka

    def __init__(self, image_path, initial_board_field_index, board_ref):
        super().__init__()
        self.board_field_index = initial_board_field_index
        self.board = board_ref
        self.pawn_id = id(self)  # Unikalne ID dla każdego pionka, może być przydatne

        try:
            self.original_image = pygame.image.load(image_path).convert_alpha()

            original_width, original_height = self.original_image.get_size()
            if original_height == 0:  # Zabezpieczenie przed dzieleniem przez zero
                print(f"OSTRZEŻENIE: Wysokość obrazka pionka '{image_path}' wynosi 0. Ustawiam domyślny rozmiar.")
                aspect_ratio = 1
            else:
                aspect_ratio = original_width / original_height

            self.pawn_render_height = Pawn.PAWN_TARGET_HEIGHT
            self.pawn_render_width = int(self.pawn_render_height * aspect_ratio)

            self.image = pygame.transform.scale(self.original_image, (self.pawn_render_width, self.pawn_render_height))
            self.rect = self.image.get_rect()
            # Pozycja zostanie ustawiona przez update_position_on_board_with_sharing
            print(f"Pionek załadowany z: {image_path}, rozmiar: {self.pawn_render_width}x{self.pawn_render_height}")
        except pygame.error as e:
            print(f"Błąd ładowania obrazka pionka '{image_path}': {e}")
            self.image = pygame.Surface([40, Pawn.PAWN_TARGET_HEIGHT])
            self.image.fill((255, 0, 0))  # Czerwony kwadrat
            self.rect = self.image.get_rect()
        except FileNotFoundError:
            print(f"BŁĄD: Nie znaleziono pliku obrazka pionka: {image_path}")
            self.image = pygame.Surface([40, Pawn.PAWN_TARGET_HEIGHT])
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect()

    def update_position_on_board_with_sharing(self, field_index, pawns_on_this_field_ids, all_pawns_objects_list):
        """
        Aktualizuje pozycję graficzną pionka na podstawie jego logicznego indeksu pola,
        uwzględniając inne pionki na tym samym polu.
        :param field_index: Indeks pola, na którym ma być pionek.
        :param pawns_on_this_field_ids: Lista ID pionków, które są na tym samym polu (łącznie z tym).
        :param all_pawns_objects_list: Lista wszystkich obiektów pionków w grze.
        """
        self.board_field_index = field_index  # Aktualizuj logiczny indeks na wszelki wypadek
        field_rect = self.board.get_field_screen_rect(self.board_field_index)

        if not field_rect:
            print(
                f"OSTRZEŻENIE: Nie można pobrać prostokąta pola dla indeksu {self.board_field_index} dla pionka ID: {self.pawn_id}.")
            self.rect.topleft = (0, 0)  # Awaryjne ustawienie
            return

        num_pawns_on_field = len(pawns_on_this_field_ids)

        try:
            this_pawn_order_on_field = pawns_on_this_field_ids.index(self.pawn_id)
        except ValueError:
            # print(f"OSTRZEŻENIE: Pionek {self.pawn_id} nie znaleziony na liście pionków ({pawns_on_this_field_ids}) dla pola {field_index}. Ustawiam jako pierwszy.")
            # Jeśli jakimś cudem pionka nie ma na liście, a powinien być, umieść go jako pierwszego
            # To nie powinno się zdarzyć, jeśli logika mapowania jest poprawna
            this_pawn_order_on_field = 0
            if num_pawns_on_field == 0:  # Jeśli lista była pusta, a my tam jesteśmy
                num_pawns_on_field = 1

        if num_pawns_on_field <= 0:  # Dodatkowe zabezpieczenie
            self.rect.center = field_rect.center
        elif num_pawns_on_field == 1:
            self.rect.center = field_rect.center
        elif num_pawns_on_field == 2:
            spacing = 3  # Mały odstęp między pionkami
            if field_rect.width > field_rect.height + 10:  # Pole jest wyraźnie poziome
                # Rozmieść wszerz
                total_pawns_width = self.pawn_render_width * 2 + spacing
                start_x = field_rect.centerx - total_pawns_width // 2
                if this_pawn_order_on_field == 0:
                    self.rect.left = start_x
                else:
                    self.rect.left = start_x + self.pawn_render_width + spacing
                self.rect.centery = field_rect.centery
            else:  # Pole jest pionowe lub kwadratowe
                # Rozmieść wzdłuż (w pionie)
                total_pawns_height = self.pawn_render_height * 2 + spacing
                start_y = field_rect.centery - total_pawns_height // 2
                if this_pawn_order_on_field == 0:
                    self.rect.top = start_y
                else:
                    self.rect.top = start_y + self.pawn_render_height + spacing
                self.rect.centerx = field_rect.centerx
        else:
            # Dla więcej niż 2 pionków, na razie umieszczamy je na sobie lub lekko przesunięte
            # Można tu zaimplementować bardziej zaawansowane rozmieszczanie (np. w kółku, siatce)
            # print(f"OSTRZEŻENIE: {num_pawns_on_field} pionków na polu {field_index}. Rozmieszczam z małym offsetem.")
            offset_x = (this_pawn_order_on_field - (num_pawns_on_field - 1) / 2) * (self.pawn_render_width / 3)
            offset_y = (this_pawn_order_on_field - (num_pawns_on_field - 1) / 2) * (self.pawn_render_height / 3)
            self.rect.centerx = field_rect.centerx + int(offset_x)
            self.rect.centery = field_rect.centery + int(offset_y)

    # Metoda move_to_field nie jest już potrzebna w tej klasie,
    # ponieważ logika przesuwania i aktualizacji mapy jest teraz w main.py (move_pawn_logic)
    # Pionek po prostu ma metodę do aktualizacji swojej wizualnej pozycji na podstawie danych.


class PlayerPawn(Pawn):
    def __init__(self, player_id, image_path, initial_board_field_index, board_ref):
        super().__init__(image_path, initial_board_field_index, board_ref)
        self.player_id_num = player_id  # Numeryczny ID gracza
        self.pawn_id = f"player_{player_id}"  # Unikalne tekstowe ID pionka
        print(f"Utworzono pionek gracza {self.player_id_num} (ID: {self.pawn_id})")


class ProfessorPawn(Pawn):
    def __init__(self, image_path, initial_board_field_index, board_ref):
        super().__init__(image_path, initial_board_field_index, board_ref)
        self.pawn_id = "professor"  # Stałe ID dla profesora
        print(f"Utworzono pionek Profesora (ID: {self.pawn_id})")