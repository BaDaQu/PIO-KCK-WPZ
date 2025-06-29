# src/settings.py
import pygame

# --- Główne Ustawienia Okna ---
INITIAL_SCREEN_WIDTH = 1436
INITIAL_SCREEN_HEIGHT = 1024
GAMEPLAY_SCREEN_WIDTH = 1436
GAMEPLAY_SCREEN_HEIGHT = 1024
SCREEN_TITLE = "Wyścig po Zaliczenie"
FPS = 60

# --- Kolory ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DEFAULT_BG_COLOR = BLACK
MENU_BG_FALLBACK_COLOR = (200, 180, 160)
MENU_BUTTON_BASE_COLOR = (240, 190, 100)
MENU_BUTTON_HOVER_COLOR = (255, 210, 120)
MENU_TEXT_COLOR = (80, 50, 20)
MENU_TITLE_COLOR = MENU_TEXT_COLOR
PANEL_BG_COLOR = (50, 50, 70)
PANEL_TEXT_COLOR_INFO = (220, 220, 220)
PANEL_BUTTON_BASE_COLOR = MENU_BUTTON_BASE_COLOR
PANEL_BUTTON_HOVER_COLOR = MENU_BUTTON_HOVER_COLOR
PANEL_BUTTON_TEXT_COLOR = MENU_TEXT_COLOR
LEFT_PANEL_WIDTH = 412
BOARD_BG_FALLBACK_COLOR = (200, 180, 160)
FIELD_LABEL_TEXT_COLOR = (10, 10, 10)
FIELD_LABEL_BG_COLOR_SUBJECT = (230, 230, 210)
FIELD_LABEL_BG_COLOR_SPECIAL = (200, 220, 240)
FIELD_LABEL_BG_COLOR_START = (180, 240, 180)
DICE_FALLBACK_IMAGE_COLOR = (255, 0, 0)
QUESTION_CARD_BG_COLOR = (245, 245, 220)
QUESTION_CARD_TEXT_COLOR = (80, 50, 20)
ANSWER_BUTTON_HOVER_COLOR = (242, 182, 53, 50)
ANSWER_CORRECT_COLOR = (144, 238, 144, 150)
ANSWER_INCORRECT_COLOR = (255, 105, 97, 150)
INSTRUCTIONS_FALLBACK_BG_COLOR = (40, 30, 20)
INSTRUCTIONS_TITLE_COLOR = (240, 190, 100)
INSTRUCTIONS_HEADER_COLOR = (220, 220, 200)
INSTRUCTIONS_BODY_COLOR = (200, 200, 180)
INSTRUCTIONS_OUTLINE_COLOR = BLACK
GAME_OVER_BG_COLOR = (40, 30, 20, 220)
GAME_OVER_TEXT_COLOR = (240, 190, 100)
GAME_OVER_WIN_TEXT = "ZWYCIĘSTWO!"
GAME_OVER_LOSE_TEXT = "PORAŻKA..."

# --- Ustawienia Dźwięku ---
DEFAULT_MASTER_VOLUME = 0.4
DEFAULT_MUSIC_VOLUME = 0.4
DEFAULT_SFX_VOLUME = 0.4

# --- Ścieżki do Zasobów ---
BASE_ASSET_PATH = "../assets/"
FIELD_ICONS_BASE_PATH = BASE_ASSET_PATH + "images/field_icons/"
SOUND_ASSET_PATH = BASE_ASSET_PATH + "sounds/"
SOUND_PATHS = { 'button_click': 'button_click.wav', 'dice_roll': 'dice_roll_loop.wav', 'pawn_move': 'pawn_move_step.wav', 'correct': 'answer_correct.wav', 'wrong': 'answer_wrong.wav', 'lose_life': 'lose_life.wav', 'gain_points': 'points_gain.wav', 'lose_points': 'points_lose.wav', 'typing': 'typing_key.wav', 'backspace': 'typing_backspace.wav', 'game_win': 'game_win.wav', 'game_lose': 'game_lose.wav' }
FIELD_ICON_MAPPING = { "START": "start.png", "ANALIZA MAT. I": "analiza_mat_i.png", "ALGEBRA LINIOWA": "algebra_liniowa.png", "OPROGRAMOWANIE UŻYTKOWE": "oprogramowanie_uzytkowe.png", "STYPENDIUM": "stypendium.png", "PROGRAMOWANIE SKRYPTOWE": "programowanie_skryptowe.png", "BHP": "bhp.png", "FIZYKA": "fizyka.png", "EGZAMIN": "egzamin.png", "MATEMATYKA DYSKRETNA": "matematyka_dyskretna.png", "PODSTAWY ELEKTROTECHNIKI": "podstawy_elektrotechniki.png", "PODSTAWY PROGRAMOWANIA I": "podstawy_programowania_i.png", "POPRAWKA": "poprawka.png", "PODSTAWY PROGRAMOWANIA II": "podstawy_programowania_ii.png", "SYSTEMY OPERACYJNE I": "systemy_operacyjne_i.png", "ANALIZA MAT. II": "analiza_mat_ii.png", "PODSTAWY GRAFIKI KOMP.": "podstawy_grafiki_komp.png", "SYSTEMY OPERACYJNE II": "systemy_operacyjne_ii.png", "ALGORYTMY I STRUKTURY DANYCH": "algorytmy_i_struktury_danych.png", "METODY PROBABILISTYCZNE": "metody_probabilistyczne.png", "METODY NUMERYCZNE": "metody_numeryczne.png", "TECHNIKA CYFROWA": "technika_cyfrowa.png", "PROGRAMOWANIE OBIEKTOWE I": "programowanie_obiektowe_i.png", "ARCHITEKTURA KOMPUTERÓW": "architektura_komputerow.png", "DESIGN THINKING": "design_thinking.png", "JĘZYK ANGIELSKI": "jezyk_angielski.png", "SIECI KOMPUTEROWE": "sieci_komputerowe.png", "BAZY DANYCH": "bazy_danych.png" }
MUSIC_PATH_MENU = BASE_ASSET_PATH + "sounds/music_menu.mp3"
MUSIC_PATH_GAME_OVER = BASE_ASSET_PATH + "sounds/music_menu.mp3" # Przykład, możesz zmienić
MUSIC_PATH_GAMEPLAY = BASE_ASSET_PATH + "sounds/music_gameplay.wav"
FONT_PATH_PT_SERIF_REGULAR = BASE_ASSET_PATH + "fonts/PTSerif-Regular.ttf"
FONT_PATH_NOTO_SERIF_REGULAR = BASE_ASSET_PATH + "fonts/NotoSerif_Condensed-Black.ttf"
FONT_PATH_HUNINN_REGULAR = BASE_ASSET_PATH + "fonts/Huninn-Regular.ttf"
IMAGE_PATH_MENU_BG = BASE_ASSET_PATH + "images/MENU_GLOWNE.png"
IMAGE_PATH_ICON = BASE_ASSET_PATH + "images/IKONA_GRY.png"
IMAGE_PATH_GAMEPLAY_LEFT_PANEL_BG = BASE_ASSET_PATH + "images/GAMEBOARD_LEFT_PANEL.png"
IMAGE_PATH_BOARD_BG = BASE_ASSET_PATH + "images/PLANSZA_GRY.png"
IMAGE_PATH_QUESTION_CARD_BG = BASE_ASSET_PATH + "images/KARTA_PYTANIA.png"
IMAGE_PATH_PLAYER1_PAWN = BASE_ASSET_PATH + "images/PIONEK_STUDENT1.png"
IMAGE_PATH_PLAYER2_PAWN = BASE_ASSET_PATH + "images/PIONEK_STUDENT2.png"
IMAGE_PATH_PROFESSOR_PAWN = BASE_ASSET_PATH + "images/PIONEK_PROFESOR.png"
IMAGE_PATH_PLAYER_WIDGET_BG = BASE_ASSET_PATH + "images/WIDGET_GRACZA1.png"
IMAGE_PATH_PLAYER_WIDGET_BG_2 = BASE_ASSET_PATH + "images/WIDGET_GRACZA2.png"
IMAGE_PATH_ECTS_ICON = BASE_ASSET_PATH + "images/ECTS_ICON.png"
IMAGE_PATH_HEART_ICON = BASE_ASSET_PATH + "images/HEART_ICON.png"
IMAGE_PATH_EMPTY_HEART_ICON = BASE_ASSET_PATH + "images/EMPTY_HEART_ICON.png"
IMAGE_PATH_INSTRUCTIONS_BG = BASE_ASSET_PATH + "images/INSTRUCTIONS_BG.png"
IMAGE_PATH_NAME_INPUT_BG = BASE_ASSET_PATH + "images/NAME_INPUT_BG.png"
IMAGE_PATH_GAME_OVER_BG = BASE_ASSET_PATH + "images/INSTRUCTIONS_BG.png"
IMAGE_PATH_WINNER_CROWN = BASE_ASSET_PATH + "images/KORONA.png"
IMAGE_PATH_SETTINGS_ICON = BASE_ASSET_PATH + "images/SETTINGS_ICON.png"
IMAGE_PATH_MUTE_ICON_OVERLAY = BASE_ASSET_PATH + "images/MUTE_X_ICON.png"
DICE_IMAGES_BASE_PATH = BASE_ASSET_PATH + "images/"

# --- Ustawienia Czcionek ---
MENU_TITLE_FONT_SIZE = 90; MENU_BUTTON_FONT_SIZE = 40; BOARD_LABEL_FONT_SIZE = 18
GAMEPLAY_PANEL_INFO_FONT_SIZE = 28; GAMEPLAY_PANEL_BUTTON_FONT_SIZE = 30; PLAYER_WIDGET_NAME_FONT_SIZE = 19
PLAYER_WIDGET_POINTS_FONT_SIZE = 30; NAME_INPUT_FONT_SIZE = 40; NAME_INPUT_LABEL_FONT_SIZE = 35
NAME_ERROR_FONT_SIZE = 24; QUESTION_CARD_QUESTION_FONT_SIZE = 32; QUESTION_CARD_ANSWER_FONT_SIZE = 28
QUESTION_CARD_ANSWER_LABEL_FONT_SIZE = 48; INSTRUCTIONS_TITLE_FONT_SIZE = 70
INSTRUCTIONS_HEADER_FONT_SIZE = 30; INSTRUCTIONS_BODY_FONT_SIZE = 20
GAME_OVER_TITLE_FONT_SIZE = 100; GAME_OVER_SUBTITLE_FONT_SIZE = 40; GAME_OVER_REASON_FONT_SIZE = 40

# --- Ustawienia Punktacji i Żyć ---
INITIAL_PLAYER_LIVES = 3; POINTS_FOR_CORRECT_ANSWER = 1; POINTS_FOR_SCHOLARSHIP = 2
POINTS_FOR_RETAKE = -2; POINTS_FOR_EXAM_CORRECT = 1; POINTS_FOR_EXAM_INCORRECT = -1
POINTS_TO_WIN = 20; LIVES_TO_LOSE = 0

# --- Ustawienia Przycisków Menu ---
MENU_BUTTON_WIDTH = 470; MENU_BUTTON_HEIGHT = 115; MENU_BUTTON_SPACING = 20
MENU_BUTTON_START_Y_OFFSET_PERCENTAGE = 0.59; MENU_BUTTON_CENTER_X_OFFSET = -140

# --- Ustawienia Przycisków Panelu Gameplay ---
GAMEPLAY_PANEL_BUTTON_WIDTH = 220; GAMEPLAY_PANEL_BUTTON_HEIGHT = 70; GAMEPLAY_PANEL_BUTTON_SPACING = 20
MAX_PLAYER_NAME_LENGTH = 20; FORFEIT_BUTTON_TEXT = "Zakończ Grę"
GAMEPLAY_SETTINGS_ICON_SIZE = 80; GAMEPLAY_SETTINGS_ICON_X = 20; GAMEPLAY_SETTINGS_ICON_Y = 900
GAMEPLAY_SETTINGS_ICON_HOVER_BG_COLOR = (255, 255, 255, 50)
GAMEPLAY_SETTINGS_ICON_HOVER_OUTLINE_COLOR = (255, 255, 255, 180)
GAMEPLAY_SETTINGS_ICON_HOVER_OUTLINE_WIDTH = 2; GAMEPLAY_SETTINGS_ICON_HOVER_BORDER_RADIUS = 10

# --- Ustawienia Ekranu Wprowadzania Imion ---
NAME_INPUT_BOX_WIDTH = 450; NAME_INPUT_BOX_HEIGHT = 60; NAME_INPUT_LABEL_Y_OFFSET = -50
NAME_INPUT_LABEL_X_OFFSET = 0; NAME_ERROR_COLOR = (200, 0, 0); NAME_ERROR_DURATION_SECONDS = 1.0
NAME_ERROR_Y_OFFSET = 10; NAME_INPUT_CURSOR_BLINK_INTERVAL_SECONDS = 0.5
NAME_INPUT_CURSOR_WIDTH = 2; NAME_INPUT_CURSOR_COLOR = WHITE

# --- Ustawienia Karty Pytania ---
QUESTION_CARD_WIDTH = 614; QUESTION_CARD_HEIGHT = 921; QUESTION_CARD_BORDER_RADIUS = 25
QUESTION_TEXT_AREA_RECT = pygame.Rect(90, 330, 430, 190); ANSWER_A_CLICK_RECT = pygame.Rect(89, 550, 436, 77)
ANSWER_B_CLICK_RECT = pygame.Rect(89, 649, 436, 77); ANSWER_C_CLICK_RECT = pygame.Rect(89, 747, 436, 77)
ANSWER_D_CLICK_RECT = pygame.Rect(89, 845, 436, 77); ANSWER_TEXT_AREA_PADDING_X = 50
ANSWER_TEXT_AREA_PADDING_Y = 5; ANSWER_LABEL_CENTER_X = 40; ANSWER_HOVER_BORDER_RADIUS = 10
FEEDBACK_DURATION_SECONDS = 2.0; INTER_QUESTION_DELAY_SECONDS = 0.4

# --- Ustawienia Kostki ---
DICE_IMAGE_WIDTH = 120; DICE_IMAGE_HEIGHT = 120; DICE_ANIMATION_DURATION_SECONDS = 0.5
DICE_ANIMATION_FRAME_DURATION_SECONDS = 0.05

# --- Ustawienia Planszy ---
BOARD_RENDER_WIDTH = 1024; BOARD_RENDER_HEIGHT = 1024

# --- Ustawienia Pionków ---
PAWN_TARGET_HEIGHT = 70; PAWN_FALLBACK_COLOR = (255, 0, 0); PAWN_MOVE_SPEED_PIXELS_PER_SECOND = 300

# --- Ustawienia Widgetu Gracza ---
PLAYER_WIDGET_WIDTH = 405; PLAYER_WIDGET_HEIGHT = 157; PLAYER_WIDGET_1_X_OFFSET = ((LEFT_PANEL_WIDTH - PLAYER_WIDGET_WIDTH) // 2) + 15
PLAYER_WIDGET_1_Y_OFFSET = 30; PLAYER_WIDGET_VERTICAL_SPACING = 15; PLAYER_WIDGET_TEXT_X_PADDING = 140
PLAYER_WIDGET_TEXT_Y_OFFSET = -7; PLAYER_WIDGET_ECTS_ICON_SIZE = 50; PLAYER_WIDGET_ECTS_ICON_X = 140
PLAYER_WIDGET_ECTS_ICON_Y = 100; PLAYER_WIDGET_ECTS_TEXT_X_OFFSET = 3; PLAYER_WIDGET_FLOATING_TEXT_X_OFFSET = 30
PLAYER_WIDGET_FLOATING_TEXT_Y_OFFSET = -10; FLOATING_TEXT_SPEED_Y = -30; FLOATING_TEXT_DURATION_SECONDS = 1.0
PLAYER_WIDGET_HEART_ICON_SIZE = 35; PLAYER_WIDGET_HEARTS_START_X = 240; PLAYER_WIDGET_HEARTS_Y = 108
PLAYER_WIDGET_HEARTS_SPACING = 5; WIDGET_SHAKE_DURATION_SECONDS = 0.4; WIDGET_SHAKE_INTENSITY = 4
WIDGET_SHAKE_FREQUENCY = 0.05; WIDGET_PULSE_DURATION_SECONDS = 1.0; WIDGET_PULSE_SCALE_MAX = 1.4
WIDGET_PULSE_SPEED = 5.0
ACTIVE_TURN_PULSE_DURATION_SECONDS = 1.5
ACTIVE_TURN_PULSE_MIN_ALPHA = 100
ACTIVE_TURN_PULSE_MAX_ALPHA = 255
ACTIVE_TURN_PULSE_BORDER_WIDTH_MIN = 2 # Minimalna grubość ramki
ACTIVE_TURN_PULSE_BORDER_WIDTH_MAX = 7 # Maksymalna grubość ramki
ACTIVE_TURN_PULSE_BORDER_RADIUS = 12
ACTIVE_TURN_PULSE_COLOR = PANEL_BUTTON_HOVER_COLOR # Użyj koloru hover z panelu
# =========================================================

# --- Ustawienia Profesora ---
PROFESSOR_BASE_MOVE_TURN_INTERVAL = 3

# --- Ustawienia dla Ekranu Instrukcji ---
INSTRUCTIONS_FALLBACK_BG_COLOR = (40, 30, 20); INSTRUCTIONS_TITLE_COLOR = (240, 190, 100)
INSTRUCTIONS_HEADER_COLOR = (220, 220, 200); INSTRUCTIONS_BODY_COLOR = (200, 200, 180)
INSTRUCTIONS_OUTLINE_COLOR = BLACK; INSTRUCTIONS_OUTLINE_WIDTH = 1; INSTRUCTIONS_TITLE_Y = 30
INSTRUCTIONS_CONTENT_START_Y = 100; INSTRUCTIONS_CONTENT_X_PADDING = 100; INSTRUCTIONS_LINE_SPACING = 1.3
INSTRUCTIONS_SECTION_SPACING = 3; INSTRUCTIONS_BULLET_INDENT = 40; INSTRUCTIONS_BACK_BUTTON_WIDTH = 300
INSTRUCTIONS_BACK_BUTTON_HEIGHT = -80; INSTRUCTIONS_BACK_BUTTON_Y_OFFSET = -60

# --- Ustawienia Ekranu Końca Gry ---
GAMEOVER_PAWN_SCALE_FACTOR = 1.3
GAMEOVER_PAWN_Y_OFFSET = -20
GAMEOVER_PAWN_SPACING = 380
GAMEOVER_CROWN_SCALE_FACTOR = 0.2
CROWN_Y_OFFSET_FROM_PAWN = -30
CROWN_ANIM_DURATION_SECONDS = 2.0
CROWN_ANIM_AMPLITUDE = 15
GAMEOVER_TITLE_Y_OFFSET = -400
GAMEOVER_REASON_Y_OFFSET = 200
GAMEOVER_BUTTON_Y_OFFSET = 350
GAME_OVER_DELAY_SECONDS = 0.7

# --- Ustawienia dla Ekranu Ustawień ---
SETTINGS_ICON_SIZE = 80; SETTINGS_ICON_X_OFFSET = 20; SETTINGS_ICON_Y_OFFSET = 900
SETTINGS_ICON_HOVER_BG_COLOR = (255, 255, 255, 50); SETTINGS_ICON_HOVER_OUTLINE_COLOR = (255, 255, 255, 180)
SETTINGS_ICON_HOVER_OUTLINE_WIDTH = 2; SETTINGS_ICON_HOVER_BORDER_RADIUS = 10
SLIDER_WIDTH = 500; SLIDER_HEIGHT = 31; SLIDER_START_Y = 300; SLIDER_Y_SPACING = 120
MUTE_ICON_OVERLAY_SCALE_FACTOR = 0.8

# --- Ustawienia Nakładki Potwierdzenia Poddania Gry ---
CONFIRM_OVERLAY_BG_COLOR = (0, 0, 0, 200)
CONFIRM_TEXT_COLOR = WHITE
CONFIRM_BUTTON_WIDTH = 250
CONFIRM_BUTTON_HEIGHT = 80
CONFIRM_BUTTON_SPACING = 50
CONFIRM_FONT_SIZE = 48
CONFIRM_BUTTON_FONT_SIZE = 36
CONFIRM_TEXT_Y_OFFSET = -80
CONFIRM_BUTTONS_Y_OFFSET = 80