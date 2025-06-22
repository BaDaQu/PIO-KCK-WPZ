# src/dice.py
import pygame
import random
import os
import settings

class Dice:
    def __init__(self, initial_x_center, initial_y_bottom_of_image,
                 dice_images_base_path=settings.DICE_IMAGES_BASE_PATH,
                 # Usunięto font_path i font_size, bo przycisk jest teraz w gameplay_screen
                 ):
        self.current_roll = 1
        self.is_animating = False
        self.animation_timer = 0.0 # Używamy float dla sekund
        self.animation_duration = settings.DICE_ANIMATION_DURATION_SECONDS # W sekundach
        self.frame_timer = 0.0 # Używamy float dla sekund
        self.frame_duration = settings.DICE_ANIMATION_FRAME_DURATION_SECONDS   # W sekundach
        self.animation_display_roll = 1

        self.dice_images = {}
        self.dice_image_width = settings.DICE_IMAGE_WIDTH
        self.dice_image_height = settings.DICE_IMAGE_HEIGHT

        for i in range(1, 7):
            try:
                img_path = os.path.join(dice_images_base_path, f'dice{i}.png')
                img = pygame.image.load(img_path).convert_alpha()
                self.dice_images[i] = pygame.transform.scale(img, (self.dice_image_width, self.dice_image_height))
            except pygame.error as e:
                print(f"Błąd: Nie można załadować obrazka '{img_path}'. Błąd: {e}")
                self.dice_images[i] = pygame.Surface((self.dice_image_width, self.dice_image_height))
                self.dice_images[i].fill(settings.DICE_FALLBACK_IMAGE_COLOR)

        self.dice_display_rect = self.dice_images[1].get_rect()
        self.dice_display_rect.centerx = initial_x_center
        self.dice_display_rect.bottom = initial_y_bottom_of_image


    def start_animation_and_roll(self):
        if not self.is_animating:
            self.is_animating = True
            self.animation_timer = 0.0 # Resetuj timer
            self.frame_timer = 0.0   # Resetuj timer
            print("Kostka: Rozpoczęto animację rzutu.")

    def get_final_roll_result(self):
        self.current_roll = random.randint(1, 6)
        print(f"Kostka: Wyrzucono ostatecznie: {self.current_roll}")
        return self.current_roll

    def update(self, dt_seconds): # dt jest teraz dt_seconds
        if self.is_animating:
            self.animation_timer += dt_seconds
            self.frame_timer += dt_seconds
            # print(f"Dice Update: dt_s={dt_seconds:.4f}, anim_timer={self.animation_timer:.2f}/{self.animation_duration:.2f}, frame_timer={self.frame_timer:.2f}, display_roll={self.animation_display_roll}")


            if self.frame_timer >= self.frame_duration:
                self.frame_timer -= self.frame_duration # Poprawne resetowanie timera klatki
                self.animation_display_roll = random.randint(1, 6)

            if self.animation_timer >= self.animation_duration:
                self.is_animating = False
                print("Kostka: Animacja ZAKOŃCZONA (is_animating = False)")

    def draw(self, screen):
        image_to_draw = self.dice_images[self.animation_display_roll if self.is_animating else self.current_roll]
        screen.blit(image_to_draw, self.dice_display_rect)