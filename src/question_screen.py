# src/question_screen.py
import pygame
import settings
import text_utility


# --- Funkcja Pomocnicza do Zaokrąglania Rogów Obrazka ---
def apply_rounded_corners_mask(image, radius):
    """Zwraca nową powierzchnię z obrazkiem, który ma zaokrąglone rogi."""
    if radius <= 0:
        return image.copy()

    rounded_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    rect = image.get_rect()

    # Utwórz maskę - czarny kształt z przezroczystymi, zaokrąglonymi rogami
    mask = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 0))  # Całkowicie przezroczysta na start
    pygame.draw.rect(mask, (255, 255, 255, 255), rect, border_radius=radius)  # Narysuj biały zaokrąglony prostokąt

    # Nałóż oryginalny obrazek na przezroczystą powierzchnię, używając maski
    rounded_image.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MAX)  # Kopiuj piksele
    rounded_image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)  # Zastosuj alfę z maski

    return rounded_image


class QuestionCard:
    def __init__(self, question_data, subject_name):
        self.question_data = question_data
        self.subject_name = subject_name
        self.is_visible = True
        self.answer_buttons = []

        self._load_assets()
        self._setup_layout()

    def _load_assets(self):
        """Ładuje zasoby i stosuje zaokrąglenie do obrazka karty."""
        try:
            # 1. Załaduj oryginalny, prostokątny obrazek
            original_card_bg_image = pygame.image.load(settings.IMAGE_PATH_QUESTION_CARD_BG).convert_alpha()

            # 2. Zastosuj maskę z zaokrąglonymi rogami
            self.card_bg_image = apply_rounded_corners_mask(
                original_card_bg_image,
                settings.QUESTION_CARD_BORDER_RADIUS
            )
        except Exception as e:
            print(f"Błąd ładowania lub przetwarzania tła karty pytania: {e}")
            # Tworzenie zastępczego, już zaokrąglonego prostokąta
            self.card_bg_image = pygame.Surface((settings.QUESTION_CARD_WIDTH, settings.QUESTION_CARD_HEIGHT),
                                                pygame.SRCALPHA)
            pygame.draw.rect(self.card_bg_image, settings.QUESTION_CARD_BG_COLOR, self.card_bg_image.get_rect(),
                             border_radius=settings.QUESTION_CARD_BORDER_RADIUS)

        # Ładowanie czcionek
        try:
            self.question_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR,
                                                  settings.QUESTION_CARD_QUESTION_FONT_SIZE)
            self.answer_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR,
                                                settings.QUESTION_CARD_ANSWER_FONT_SIZE)
            self.answer_label_font = pygame.font.Font(settings.FONT_PATH_PT_SERIF_REGULAR,
                                                      settings.QUESTION_CARD_ANSWER_LABEL_FONT_SIZE)
        except Exception as e:
            print(f"Błąd ładowania czcionek dla karty pytania: {e}")
            self.question_font = pygame.font.SysFont(None, settings.QUESTION_CARD_QUESTION_FONT_SIZE)
            self.answer_font = pygame.font.SysFont(None, settings.QUESTION_CARD_ANSWER_FONT_SIZE)
            self.answer_label_font = pygame.font.SysFont(None, settings.QUESTION_CARD_ANSWER_LABEL_FONT_SIZE)

    def _setup_layout(self):
        """Ustawia pozycje i prostokąty dla tekstu i przycisków na podstawie `settings`."""
        self.card_rect = self.card_bg_image.get_rect(
            center=(settings.GAMEPLAY_SCREEN_WIDTH // 2, settings.GAMEPLAY_SCREEN_HEIGHT // 2)
        )
        self.question_text_screen_rect = settings.QUESTION_TEXT_AREA_RECT.move(self.card_rect.left, self.card_rect.top)

        self.answer_buttons = []
        local_answer_rects = [
            settings.ANSWER_A_CLICK_RECT, settings.ANSWER_B_CLICK_RECT,
            settings.ANSWER_C_CLICK_RECT, settings.ANSWER_D_CLICK_RECT
        ]
        for i, local_rect in enumerate(local_answer_rects):
            screen_rect = local_rect.move(self.card_rect.left, self.card_rect.top)
            self.answer_buttons.append({"rect": screen_rect, "index": i, "hover": False})

    def handle_event(self, event, mouse_pos):
        if not self.is_visible: return None
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.answer_buttons:
                if button["rect"].collidepoint(mouse_pos):
                    self.is_visible = False
                    return button["index"]
        return None

    def update_hover(self, mouse_pos):
        if not self.is_visible: return
        for button in self.answer_buttons:
            button["hover"] = button["rect"].collidepoint(mouse_pos)

    def draw(self, surface):
        if not self.is_visible: return

        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        surface.blit(self.card_bg_image, self.card_rect)

        text_utility.render_text_in_rect(
            surface=surface, text=self.question_data["question_text"],
            font_path=settings.FONT_PATH_NOTO_SERIF_REGULAR, initial_font_size=settings.QUESTION_CARD_QUESTION_FONT_SIZE,
            color=settings.QUESTION_CARD_TEXT_COLOR, rect=self.question_text_screen_rect,
            vertical_align='center'
        )

        answer_labels = ["A", "B", "C", "D"]
        for i, answer_text in enumerate(self.question_data["answers"]):
            button_info = self.answer_buttons[i]

            if button_info["hover"]:
                pygame.draw.rect(surface, settings.ANSWER_BUTTON_HOVER_COLOR, button_info["rect"],
                                 border_radius=settings.ANSWER_HOVER_BORDER_RADIUS)

            label_surf = self.answer_label_font.render(answer_labels[i], True, settings.QUESTION_CARD_TEXT_COLOR)
            label_rect = label_surf.get_rect(
                centerx=button_info["rect"].left + settings.ANSWER_LABEL_CENTER_X,
                centery=button_info["rect"].centery
            )
            surface.blit(label_surf, label_rect)

            answer_text_area = button_info["rect"].inflate(
                -settings.ANSWER_TEXT_AREA_PADDING_X * 2,
                -settings.ANSWER_TEXT_AREA_PADDING_Y * 2
            )
            answer_text_area.left = button_info["rect"].left + settings.ANSWER_TEXT_AREA_PADDING_X

            text_utility.render_text_in_rect(
                surface=surface, text=answer_text,
                font_path=settings.FONT_PATH_NOTO_SERIF_REGULAR,
                initial_font_size=settings.QUESTION_CARD_ANSWER_FONT_SIZE,
                color=settings.QUESTION_CARD_TEXT_COLOR, rect=answer_text_area,
                vertical_align='center'
            )