# src/question_manager.py
import json
import random
import os
import settings
import copy  # Użyjemy do stworzenia kopii pytań, aby nie modyfikować oryginału

# Zmienne globalne modułu
_master_questions_db = {}  # Słownik z oryginalnymi pytaniami załadowanymi z pliku
_available_questions_db = {}  # Słownik z pytaniami dostępnymi w bieżącej sesji gry
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
        # Po załadowaniu, od razu przygotowujemy pulę dostępnych pytań na nową grę
        reset_available_questions()

    except FileNotFoundError:
        print(f"BŁĄD KRYTYCZNY: Nie znaleziono pliku z pytaniami: {questions_file_path}")
        _all_questions_loaded = False
    except json.JSONDecodeError:
        print(f"BŁĄD KRYTYCZNY: Błąd dekodowania pliku JSON z pytaniami: {questions_file_path}")
        _all_questions_loaded = False
    except Exception as e:
        print(f"BŁĄD KRYTYCZNY: Nieoczekiwany błąd podczas ładowania pytań: {e}")
        _all_questions_loaded = False


def reset_available_questions():
    """
    Resetuje pulę dostępnych pytań, kopiując wszystko z bazy głównej.
    Należy wywołać na początku każdej nowej gry.
    """
    global _available_questions_db
    # Tworzymy głęboką kopię, aby modyfikacje _available_questions_db nie wpływały na _master_questions_db
    _available_questions_db = copy.deepcopy(_master_questions_db)
    print("Zresetowano pulę dostępnych pytań na nową grę.")


def get_random_question_for_subject(subject_name):
    """
    Zwraca losowe, *nieużyte jeszcze* pytanie dla danego przedmiotu.
    Po zwróceniu, pytanie jest usuwane z puli dostępnych pytań dla tej sesji.
    """
    if not _all_questions_loaded:
        print("OSTRZEŻENIE: Próba pobrania pytania, ale baza pytań nie jest załadowana.")
        return None

    # Sprawdź, czy mamy jakiekolwiek dostępne pytania dla tego przedmiotu
    if subject_name in _available_questions_db and _available_questions_db[subject_name]:

        # Wybierz losowe pytanie z listy dostępnych
        chosen_question = random.choice(_available_questions_db[subject_name])

        # Usuń wylosowane pytanie z listy dostępnych pytań, aby się nie powtórzyło
        _available_questions_db[subject_name].remove(chosen_question)

        return chosen_question
    else:
        print(f"Brak dostępnych (nowych) pytań dla przedmiotu: '{subject_name}'")
        # Opcjonalnie: Można tu zresetować pulę pytań dla tego przedmiotu, jeśli się skończyły
        # if subject_name in _master_questions_db:
        #     _available_questions_db[subject_name] = copy.deepcopy(_master_questions_db[subject_name])
        #     print(f"Pula pytań dla '{subject_name}' została odnowiona.")
        #     return get_random_question_for_subject(subject_name) # Spróbuj jeszcze raz
        return None


# Inicjalizacyjne załadowanie pytań przy pierwszym imporcie modułu
load_questions_from_file()