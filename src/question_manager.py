# src/question_manager.py
import json
import random
import os
import settings
import copy

# --- Zmienne globalne modułu ---
_master_questions_db = {}
_available_questions_db = {}
_all_questions_loaded = False


def load_questions_from_file():
    """Ładuje pytania z pliku JSON. Jest wywoływana tylko raz."""
    global _master_questions_db, _all_questions_loaded
    questions_file_path = os.path.join(settings.BASE_ASSET_PATH, 'data', 'questions.json')
    try:
        with open(questions_file_path, 'r', encoding='utf-8') as f:
            _master_questions_db = json.load(f)
        _all_questions_loaded = True
        print(f"Załadowano bazę pytań. Znaleziono pytania dla {len(_master_questions_db)} przedmiotów.")
        reset_available_questions()
    except Exception as e:
        print(f"BŁĄD KRYTYCZNY podczas ładowania pytań: {e}")
        _all_questions_loaded = False


def reset_available_questions():
    """Resetuje pulę dostępnych pytań, kopiując wszystko z bazy głównej."""
    global _available_questions_db
    _available_questions_db = copy.deepcopy(_master_questions_db)
    print("Zresetowano pulę dostępnych pytań na nową grę.")


def get_random_question_for_subject(subject_name):
    """Zwraca losowe, nieużyte jeszcze pytanie dla danego przedmiotu."""
    if not _all_questions_loaded: return None
    if subject_name in _available_questions_db and _available_questions_db[subject_name]:
        chosen_question = random.choice(_available_questions_db[subject_name])
        _available_questions_db[subject_name].remove(chosen_question)
        return chosen_question
    else:
        # Można dodać logikę odświeżania puli, jeśli się skończy
        return None


# === NOWA FUNKCJA DO DODANIA ===
def get_random_question_from_any_subject():
    """
    Zwraca losowe pytanie z DOWOLNEGO przedmiotu z puli dostępnych pytań.
    Używane do trybu Egzaminu.
    """
    if not _all_questions_loaded: return None

    # Stwórz listę wszystkich dostępnych pytań ze wszystkich przedmiotów
    all_available_questions = []
    for subject, questions in _available_questions_db.items():
        for question in questions:
            # Dodaj informację o oryginalnym przedmiocie do słownika pytania
            # aby wiedzieć, skąd pochodzi i móc je później usunąć
            q_copy = question.copy()
            q_copy['original_subject'] = subject
            all_available_questions.append(q_copy)

    if not all_available_questions:
        print("Brak jakichkolwiek dostępnych pytań w całej bazie do egzaminu.")
        # Opcjonalnie: zresetuj całą pulę pytań, jeśli chcemy, aby egzamin zawsze miał pytania
        # reset_available_questions()
        # return get_random_question_from_any_subject() # Uważaj na nieskończoną pętlę!
        return None

    # Wybierz losowe pytanie z tej połączonej listy
    chosen_question_with_subject = random.choice(all_available_questions)

    # Znajdź i usuń to pytanie z oryginalnej puli _available_questions_db, aby się nie powtórzyło
    original_subject = chosen_question_with_subject['original_subject']
    # Tworzymy słownik oryginalnego pytania, aby znaleźć je na liście
    original_question = {k: v for k, v in chosen_question_with_subject.items() if k != 'original_subject'}

    if original_subject in _available_questions_db:
        # Sprawdź, czy pytanie faktycznie istnieje przed próbą usunięcia
        if original_question in _available_questions_db[original_subject]:
            _available_questions_db[original_subject].remove(original_question)
        else:
            # To może się zdarzyć, jeśli to samo pytanie jest w bazie wielokrotnie
            # i zostało już wylosowane. Na razie to tylko ostrzeżenie.
            print(f"OSTRZEŻENIE: Nie można znaleźć pytania do usunięcia w puli dla {original_subject}")

    return chosen_question_with_subject


# Inicjalizacyjne załadowanie pytań przy pierwszym imporcie modułu
load_questions_from_file()