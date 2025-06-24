# src/sound_manager.py
import pygame
import settings
import os

# Słownik do przechowywania załadowanych EFEKTÓW dźwiękowych
_sounds = {}

# --- Zmienne Głośności ---
master_volume = settings.DEFAULT_MASTER_VOLUME
music_volume = settings.DEFAULT_MUSIC_VOLUME
sfx_volume = settings.DEFAULT_SFX_VOLUME


def load_sounds():
    """Ładuje wszystkie zdefiniowane EFEKTY dźwiękowe do pamięci."""
    global _sounds
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            print("Zainicjalizowano Pygame Mixer.")

        script_dir = os.path.dirname(__file__)
        project_root_dir = os.path.abspath(os.path.join(script_dir, ".."))

        for sound_name, filename in settings.SOUND_PATHS.items():
            full_path = os.path.join(project_root_dir, 'assets', 'sounds', filename)
            try:
                sound = pygame.mixer.Sound(full_path)
                sound.set_volume(master_volume * sfx_volume)
                _sounds[sound_name] = sound
            except pygame.error as e:
                print(f"OSTRZEŻENIE: Nie można załadować dźwięku '{sound_name}' ze ścieżki '{full_path}'. Błąd: {e}")

        print("Wszystkie dostępne efekty dźwiękowe zostały załadowane.")
    except Exception as e:
        print(f"BŁĄD KRYTYCZNY: Nie udało się zainicjalizować dźwięków. Gra będzie bezdźwięczna. Błąd: {e}")
        _sounds = {}


def set_master_volume(value):
    """Ustawia głośność ogólną (0-100) i aktualizuje głośność muzyki i efektów."""
    global master_volume
    master_volume = value / 100.0
    set_music_volume(music_volume * 100)
    set_sfx_volume(sfx_volume * 100)


def set_music_volume(value):
    """Ustawia głośność muzyki (0-100)."""
    global music_volume
    music_volume = value / 100.0
    if pygame.mixer.get_init():
        pygame.mixer.music.set_volume(master_volume * music_volume)


def set_sfx_volume(value):
    """Ustawia głośność wszystkich efektów dźwiękowych (0-100)."""
    global sfx_volume
    sfx_volume = value / 100.0
    for sound in _sounds.values():
        sound.set_volume(master_volume * sfx_volume)


def play_music(track_name_key, loops=-1):
    """Ładuje i odtwarza utwór muzyczny w tle na podstawie klucza z settings.py."""
    if not pygame.mixer.get_init():
        print("OSTRZEŻENIE: Mixer nie jest zainicjalizowany. Nie można odtworzyć muzyki.")
        return

    try:
        track_path_relative = ""
        if track_name_key == 'menu':
            track_path_relative = settings.MUSIC_PATH_MENU
        elif track_name_key == 'gameplay':
            track_path_relative = settings.MUSIC_PATH_GAMEPLAY
        elif track_name_key == 'game_over':
             # Załóżmy, że masz muzykę końca gry zdefiniowaną w settings
            if hasattr(settings, 'MUSIC_PATH_GAME_OVER'):
                track_path_relative = settings.MUSIC_PATH_GAME_OVER
            else:
                print(f"OSTRZEŻENIE: Brak zdefiniowanej ścieżki MUSIC_PATH_GAME_OVER w settings.py")
                return
        else:
            print(f"OSTRZEŻENIE: Nieznany klucz muzyki: {track_name_key}")
            return

        script_dir = os.path.dirname(__file__)
        project_root_dir = os.path.abspath(os.path.join(script_dir, ".."))
        full_path = os.path.join(project_root_dir, track_path_relative.replace("../", "", 1))

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.set_volume(master_volume * music_volume)
        pygame.mixer.music.play(loops)
        print(f"Odtwarzam muzykę: {full_path}")
    except pygame.error as e:
        print(f"BŁĄD: Nie można załadować lub odtworzyć muzyki '{track_name_key}'. Błąd: {e}")


def play_sound(sound_name, loops=0):
    """Odtwarza załadowany efekt dźwiękowy o podanej nazwie."""
    if sound_name in _sounds:
        try:
            _sounds[sound_name].play(loops)
        except Exception as e:
            print(f"Błąd podczas odtwarzania dźwięku '{sound_name}': {e}")
    else:
        print(f"OSTRZEŻENIE: Próba odtworzenia niezdefiniowanego dźwięku: '{sound_name}'")


def stop_sound(sound_name):
    """Zatrzymuje odtwarzanie danego efektu dźwiękowego."""
    if sound_name in _sounds:
        try:
            _sounds[sound_name].stop()
        except Exception as e:
            print(f"Błąd podczas zatrzymywania dźwięku '{sound_name}': {e}")


def stop_all_sounds():
    """Zatrzymuje wszystkie efekty dźwiękowe i muzykę."""
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.quit()