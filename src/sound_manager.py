# src/sound_manager.py
import pygame
import settings
import os

# Słownik do przechowywania załadowanych EFEKTÓW dźwiękowych
_sounds = {}

# Zmienne Głośności
master_volume = settings.DEFAULT_MASTER_VOLUME
music_volume = settings.DEFAULT_MUSIC_VOLUME
sfx_volume = settings.DEFAULT_SFX_VOLUME

is_globally_muted = False  # Globalny przełącznik MUTE
_previous_master_volume_before_mute = settings.DEFAULT_MASTER_VOLUME


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
                # Początkowa głośność uwzględnia wszystkie poziomy
                sound.set_volume(master_volume * sfx_volume if not is_globally_muted else 0)
                _sounds[sound_name] = sound
            except pygame.error as e:
                print(f"OSTRZEŻENIE: Nie można załadować dźwięku '{sound_name}' ze ścieżki '{full_path}'. Błąd: {e}")

        print("Wszystkie dostępne efekty dźwiękowe zostały załadowane.")
    except Exception as e:
        print(f"BŁĄD KRYTYCZNY: Nie udało się zainicjalizować dźwięków. Gra będzie bezdźwięczna. Błąd: {e}")
        _sounds = {}


def set_master_volume(value, from_mute_toggle=False):
    """Ustawia głośność ogólną (0-100) i aktualizuje głośność muzyki i efektów."""
    global master_volume, _previous_master_volume_before_mute, is_globally_muted

    new_volume = max(0.0, min(1.0, value / 100.0))

    if not from_mute_toggle:
        _previous_master_volume_before_mute = new_volume
        # Jeśli użytkownik przesuwa suwak master_volume i odcisza (było 0, teraz > 0),
        # a globalny mute był aktywny, to wyłączamy globalny mute.
        if is_globally_muted and master_volume <= 0.001 and new_volume > 0.001:
            is_globally_muted = False
            print("Dźwięk odciszony przez suwak Master Volume (globalny mute wyłączony).")
            # _previous_master_volume_before_mute jest już ustawione na new_volume

    master_volume = new_volume

    # Aktualizuj głośność zależnych komponentów
    _update_actual_music_volume()
    _update_actual_sfx_volume()
    print(f"Głośność ogólna ustawiona na: {master_volume * 100:.0f}%")


def set_music_volume(value, from_master_update=False):  # Zmieniono nazwę flagi
    """Ustawia głośność muzyki (0-100)."""
    global music_volume, is_globally_muted, _previous_master_volume_before_mute

    new_music_vol = max(0.0, min(1.0, value / 100.0))

    # Jeśli użytkownik odcisza muzykę suwakiem muzyki, a globalny mute był aktywny (bo master był 0)
    if not from_master_update and is_globally_muted and new_music_vol > 0.001:
        is_globally_muted = False
        # Przywróć master volume, jeśli było 0 z powodu mute
        if _previous_master_volume_before_mute > 0.001:
            set_master_volume(_previous_master_volume_before_mute * 100, from_mute_toggle=True)
        else:  # Jeśli poprzedni master też był 0, ustaw na jakąś domyślną wartość
            set_master_volume(settings.DEFAULT_MASTER_VOLUME * 100, from_mute_toggle=True)
        print("Muzyka odciszona przez suwak, odciszono też globalnie (jeśli master był 0).")

    music_volume = new_music_vol
    _update_actual_music_volume()
    # print(f"Głośność muzyki (ustawienie) na: {music_volume*100:.0f}%")


def set_sfx_volume(value, from_master_update=False):  # Zmieniono nazwę flagi
    """Ustawia głośność wszystkich efektów dźwiękowych (0-100)."""
    global sfx_volume, is_globally_muted, _previous_master_volume_before_mute

    new_sfx_vol = max(0.0, min(1.0, value / 100.0))

    if not from_master_update and is_globally_muted and new_sfx_vol > 0.001:
        is_globally_muted = False
        if _previous_master_volume_before_mute > 0.001:
            set_master_volume(_previous_master_volume_before_mute * 100, from_mute_toggle=True)
        else:
            set_master_volume(settings.DEFAULT_MASTER_VOLUME * 100, from_mute_toggle=True)
        print("SFX odciszone przez suwak, odciszono też globalnie (jeśli master był 0).")

    sfx_volume = new_sfx_vol
    _update_actual_sfx_volume()
    # print(f"Głośność SFX (ustawienie) na: {sfx_volume*100:.0f}%")


def _update_actual_music_volume():
    """Aktualizuje faktyczną głośność odtwarzanej muzyki."""
    if pygame.mixer.get_init():
        effective_vol = master_volume * music_volume if not is_globally_muted else 0
        pygame.mixer.music.set_volume(effective_vol)
        # print(f"Efektywna głośność muzyki: {effective_vol*100:.0f}%")


def _update_actual_sfx_volume():
    """Aktualizuje faktyczną głośność wszystkich załadowanych efektów SFX."""
    effective_vol = master_volume * sfx_volume if not is_globally_muted else 0
    for sound in _sounds.values():
        sound.set_volume(effective_vol)
    # print(f"Efektywna głośność SFX: {effective_vol*100:.0f}%")


def toggle_mute_all_sounds():
    """Przełącza globalne wyciszenie wszystkich dźwięków."""
    global is_globally_muted, master_volume, _previous_master_volume_before_mute

    is_globally_muted = not is_globally_muted

    if is_globally_muted:
        # Zapamiętaj TYLKO jeśli master_volume > 0, inaczej zapamiętasz 0 i nie będzie do czego wrócić
        if master_volume > 0.001:
            _previous_master_volume_before_mute = master_volume
        # Wycisz ustawiając master na 0, ale tylko jeśli nie jest już 0 z innego powodu
        set_master_volume(0, from_mute_toggle=True)
        print("Wszystkie dźwięki WYCISZONE globalnie.")
    else:
        # Przywróć poprzednią zapamiętaną głośność (lub domyślną, jeśli była 0)
        volume_to_restore = _previous_master_volume_before_mute if _previous_master_volume_before_mute > 0.001 else settings.DEFAULT_MASTER_VOLUME
        set_master_volume(volume_to_restore * 100, from_mute_toggle=True)
        print("Wszystkie dźwięki ODCISZONE globalnie.")
    return is_globally_muted


def play_music(track_name_key, loops=-1):
    if not pygame.mixer.get_init(): print("OSTRZEŻENIE: Mixer nie jest zainicjalizowany."); return
    try:
        track_path_relative = "";
        if track_name_key == 'menu':
            track_path_relative = settings.MUSIC_PATH_MENU
        elif track_name_key == 'gameplay':
            track_path_relative = settings.MUSIC_PATH_GAMEPLAY
        elif track_name_key == 'game_over':
            if hasattr(settings, 'MUSIC_PATH_GAME_OVER'):
                track_path_relative = settings.MUSIC_PATH_GAME_OVER
            else:
                print(f"OSTRZEŻENIE: Brak MUSIC_PATH_GAME_OVER w settings.py"); return
        else:
            print(f"OSTRZEŻENIE: Nieznany klucz muzyki: {track_name_key}"); return
        script_dir = os.path.dirname(__file__);
        project_root_dir = os.path.abspath(os.path.join(script_dir, ".."))
        full_path = os.path.join(project_root_dir, track_path_relative.replace("../", "", 1))
        pygame.mixer.music.stop();
        pygame.mixer.music.unload();
        pygame.mixer.music.load(full_path)
        _update_actual_music_volume()  # Ustaw głośność z uwzględnieniem mute i master
        pygame.mixer.music.play(loops);
        print(f"Odtwarzam muzykę: {full_path}")
    except Exception as e:
        print(f"BŁĄD: Nie można załadować lub odtworzyć muzyki '{track_name_key}'. Błąd: {e}")


def play_sound(sound_name, loops=0):
    # Nie sprawdzamy tu `is_globally_muted`, bo głośność efektów jest już ustawiona na 0
    # przez `_update_actual_sfx_volume` jeśli jest mute.
    if sound_name in _sounds:
        try:
            _sounds[sound_name].play(loops)
        except Exception as e:
            print(f"Błąd podczas odtwarzania dźwięku '{sound_name}': {e}")
    else:
        print(f"OSTRZEŻENIE: Próba odtworzenia niezdefiniowanego dźwięku: '{sound_name}'")


def stop_sound(sound_name):
    if sound_name in _sounds:
        try:
            _sounds[sound_name].stop()
        except Exception as e:
            print(f"Błąd podczas zatrzymywania dźwięku '{sound_name}': {e}")


def stop_all_sounds():
    if pygame.mixer.get_init(): pygame.mixer.music.stop(); pygame.mixer.stop()


def is_music_playing():
    if pygame.mixer.get_init(): return pygame.mixer.music.get_busy()
    return False


# === POPRAWIONA FUNKCJA ===
def is_effectively_muted():
    """
    Sprawdza, czy dźwięk jest efektywnie wyciszony.
    """
    if is_globally_muted:  # Jeśli globalny MUTE jest włączony
        return True
    if master_volume <= 0.001:  # Jeśli głośność ogólna jest na 0
        return True
    # Jeśli głośność ogólna jest > 0, ale zarówno muzyka jak i efekty są na 0
    if music_volume <= 0.001 and sfx_volume <= 0.001:
        return True
    return False
# =========================