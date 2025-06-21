# Wyścig po Zaliczenie

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Cyfrowa gra planszowa wspierająca proces nauki i utrwalania wiedzy dla studentów Politechniki Łódzkiej.**

 <!-- Przykładowy screenshot, możesz podmienić na własny -->

## Spis Treści

*   [Zespół](#zespół)
*   [Cel Projektu](#cel-projektu)
*   [Opis i Zasady Gry](#opis-i-zasady-gry)
*   [Technologie](#technologie)
*   [Status Funkcji](#status-funkcji)
*   [Struktura Projektu](#struktura-projektu)
*   [Dokumentacja Projektowa](#dokumentacja-projektowa)
*   [Licencja](#licencja)

## Zespół

*   Bartłomiej Raj
*   Marcel Podlecki
*   Bartłomiej Jedyk
*   Wojciech Stochmiałek
*   Marcin Świstak

## Cel Projektu

Głównym celem projektu "Wyścig po Zaliczenie" jest stworzenie **angażującej i motywującej formy grywalizacyjnej**, która:

*   **Wspiera studentów Politechniki Łódzkiej** w procesie nauki i przygotowań do zaliczeń.
*   **Uatrakcyjnia powtarzanie materiału** z kluczowych przedmiotów, czerpiąc inspirację z platformy Wikamp.
*   **Zmniejsza stres** związany z sesją egzaminacyjną poprzez zabawę i element rywalizacji.
*   **Integruje elementy wiedzy akademickiej z rozrywką**, wzmacniając poczucie wspólnoty wśród studentów.

## Opis i Zasady Gry

"Wyścig po Zaliczenie" to cyfrowa gra planszowa dla dwóch graczy, w której celem jest przetrwanie sesji i zdobycie przepustki na kolejny semestr. Uczestnicy wcielają się w studentów poruszających się po planszy symbolizującej ścieżkę edukacyjną, odpowiadając na pytania i stawiając czoła wyzwaniom akademickiego życia.

### Warunki Zwycięstwa i Porażki

Grę można wygrać lub przegrać na dwa sposoby:

*   **Zwycięstwo przez Punkty:** Pierwszy gracz, który zdobędzie **30 punktów ECTS**, wygrywa grę!
*   **Porażka przez Utratę Żyć:** Każdy gracz rozpoczyna z **3 życiami** (sercami). Jeśli stracisz wszystkie życia (np. przez wielokrotne złapanie przez Profesora), przegrywasz, a Twój przeciwnik zostaje zwycięzcą.

### Przebieg Tury

1.  **Rzut Kostką:** W swojej turze kliknij przycisk **"Rzuć Kostką"**. Twój pionek przesunie się o wylosowaną liczbę oczek.
2.  **Akcja Pola:** Po zatrzymaniu się na polu, następuje odpowiednia akcja:
    *   **Pola Przedmiotowe** (np. "FIZYKA", "BAZY DANYCH"): Na ekranie pojawia się karta z pytaniem z danej dziedziny.
        *   **Poprawna odpowiedź:** Zdobywasz **+1 punkt ECTS**.
        *   **Błędna odpowiedź:** Nie zdobywasz punktów, a **Pionek Profesora natychmiast przesuwa się o 1 pole do przodu!**
    *   **Pola Specjalne:**
        *   **START:** Twoja przygoda zaczyna się tutaj.
        *   **STYPENDIUM:** Za ciężką pracę otrzymujesz premię **+2 punkty ECTS**.
        *   **POPRAWKA:** Niestety, coś poszło nie tak. Tracisz **-2 punkty ECTS**.
        *   **EGZAMIN:** Czas na test! Odpowiadasz na 3 losowe pytania z całej puli przedmiotów.
            *   **+1 ECTS** za każdą poprawną odpowiedź.
            *   **-1 ECTS** i **ruch Profesora o 1 pole** za każdą błędną.
            *   **Nagroda:** Za minimum 2 poprawne odpowiedzi odzyskujesz **1 życie** (jeśli masz mniej niż 3).

### Pionek Profesora - Nieustanne Zagrożenie

Profesor to Twój największy rywal, który nieustannie depcze Ci po piętach. Jego celem jest utrudnienie Ci drogi do zaliczenia.

*   **Ruch Podstawowy:** Przesuwa się o 1 pole co **3 tury graczy** (po turze drugiego gracza, jeśli licznik się zgadza).
*   **Ruch za Karę:** Przesuwa się o 1 pole za **każdą błędną odpowiedź** gracza.
*   **Złapanie przez Profesora:** Jeśli Profesor wyląduje na polu, na którym stoisz, ponosisz surowe konsekwencje: tracisz **1 życie** oraz **1 punkt ECTS**.

### Poddanie Gry

Jeśli presja okaże się zbyt duża, możesz w każdej chwili poddać grę, używając przycisku **"Zakończ Grę"** w panelu bocznym. Zwycięstwo zostanie wtedy przyznane Twojemu przeciwnikowi.

## Technologie

*   **Język programowania:** Python 3.13
*   **Główna biblioteka:** Pygame
*   **Format danych:** JSON (dla bazy pytań)

## Status Funkcji

Lista zaimplementowanych i planowanych funkcjonalności.

*   [x] **Menu Główne i Nawigacja:** Ekran startowy, instrukcji i wyjścia.
*   [x] **Ekran Wprowadzania Imion:** Możliwość personalizacji rozgrywki.
*   [x] **Interfejs Rozgrywki:** Wyświetlanie planszy, panelu bocznego, widgetów graczy.
*   [x] **System Pionków:** Renderowanie pionków graczy i Profesora, animacja ruchu pole po polu, unikanie nakładania się.
*   [x] **System Rzutu Kostką:** Interaktywny przycisk z animacją losowania.
*   [x] **System Tur:** Logika przełączania tur między dwoma graczami.
*   [x] **System Pytań:** Ładowanie pytań z pliku JSON i wyświetlanie ich na karcie "popup".
*   [x] **Weryfikacja Odpowiedzi:** Logika sprawdzania poprawności i wizualny feedback na karcie.
*   [x] **System Punktacji ECTS:** Zliczanie punktów, animacja zmian.
*   [x] **System Żyć:** Zliczanie żyć, wizualizacja utraty/zdobycia.
*   [x] **Logika Pól Specjalnych:** Działanie pól "Stypendium", "Poprawka", "Egzamin".
*   [x] **Logika Ruchu Profesora:** Dynamiczny ruch oparty na turach i błędach graczy.
*   [ ] **Warunki Zwycięstwa/Porażki:** Implementacja logiki końca gry (dotarcie do mety, utrata wszystkich żyć).
*   [ ] **Ekran Końca Gry:** Wyświetlanie wyników i opcji po zakończeniu rozgrywki.
*   [ ] **Efekty Dźwiękowe i Muzyka:** Dodanie oprawy audio.

*(Legenda: [x] - Zaimplementowane, [ ] - Do zaimplementowania)*

## Struktura Projektu
```plaintext
WyscigPoZaliczenie/
├── src/                     # Główny folder z kodem źródłowym gry
│   ├── main.py              # Punkt startowy, główna pętla gry
│   ├── settings.py          # Centralny plik konfiguracyjny
│   ├── game_logic.py        # Główna logika gry i zarządzanie stanem
│   ├── menu_screen.py       # Logika i rysowanie menu głównego
│   ├── gameplay_screen.py   # Logika i rysowanie ekranu rozgrywki
│   ├── question_screen.py   # Logika i rysowanie karty pytania
│   ├── name_input_screen.py # Logika i rysowanie ekranu wprowadzania imion
│   ├── player_widget.py     # Klasa dla widgetu informacji o graczu
│   ├── pawn.py              # Klasa dla pionków
│   ├── dice.py              # Klasa dla kostki
│   ├── button.py            # Klasa dla przycisków
│   ├── effects.py           # Klasa dla efektów wizualnych (np. pływający tekst)
│   ├── question_manager.py  # Zarządzanie bazą pytań
│   └── text_utility.py      # Funkcje pomocnicze do renderowania tekstu
│
├── assets/                  # Zasoby gry
│   ├── images/              # Pliki graficzne (.png, .jpg)
│   ├── fonts/               # Pliki czcionek (.ttf, .otf)
│   ├── data/                # Pliki danych (np. questions.json)
│   └── sounds/              # Pliki dźwiękowe (opcjonalnie)
│
├── docs/                    # Dokumentacja projektowa
│   ├── DOKUMENTACJA_PROJEKTOWA.pdf
│   └── BRAND_BOOK.pdf
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
