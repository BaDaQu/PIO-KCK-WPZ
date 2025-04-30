# Wyścig po Zaliczenie

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) <!-- Możesz zmienić lub usunąć licencję -->

**Cyfrowa gra planszowa wspierająca proces nauki i utrwalania wiedzy dla studentów Politechniki Łódzkiej.**

<!-- Opcjonalnie: Krótki screenshot lub GIF pokazujący grę -->
<!-- ![Gameplay Screenshot](link_do_obrazka.png) -->

## Spis Treści

*   [Zespół](#zespół)
*   [Cel Projektu](#cel-projektu)
*   [Opis Gry](#opis-gry)
    *   [Koncepcja](#koncepcja)
    *   [Kluczowe Mechaniki](#kluczowe-mechaniki)
*   [Technologie](#technologie)
*   [Główne Funkcje (Zaimplementowane/Planowane)](#główne-funkcje-zaimplementowaneplanowane)
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
*   **Uatrakcyjnia powtarzanie materiału** z kluczowych przedmiotów, czerpiąc inspirację (i potencjalnie dane) z platformy Wikamp.
*   **Zmniejsza stres** związany z sesją egzaminacyjną poprzez zabawę i element rywalizacji.
*   **Integruje elementy wiedzy akademickiej z rozrywką**, wzmacniając poczucie wspólnoty i zdrowej rywalizacji wśród studentów.

Projekt stanowi odpowiedź na zidentyfikowane wyzwania, takie jak monotonia tradycyjnych metod nauki i natłok informacji na początku studiów.

## Opis Gry

### Koncepcja

"Wyścig po Zaliczenie" to **cyfrowa gra planszowa** przeznaczona dla minimum dwóch graczy (studentów), rozgrywana lokalnie na jednym ekranie. Gracze wcielają się w studentów-pionki, poruszających się po planszy symbolizującej ścieżkę edukacyjną (np. pierwsze semestry na PŁ). Celem jest dotarcie do mety (symbolizującej zaliczenie) przed innymi graczami oraz przed goniącym ich "Pionkiem Profesora".

### Kluczowe Mechaniki

1.  **Ruch po Planszy:** Gracze rzucają wirtualną, sześciościenną kostką i przesuwają swoje pionki o wylosowaną liczbę pól.
2.  **Pola Przedmiotowe:** Wylądowanie na polu oznaczonym konkretnym przedmiotem (np. Matematyka, Fizyka, Programowanie, Chemia) aktywuje pytanie testowe z tej dziedziny.
3.  **System Pytań i Odpowiedzi:** Gracz musi wybrać jedną z czterech odpowiedzi (A, B, C, D). Poprawna odpowiedź pozwala kontynuować grę (lub daje bonus), błędna może skutkować karą (np. utratą kolejki, cofnięciem) i przyspieszeniem "Pionka Profesora".
4.  **Pionek Profesora:** Postać sterowana przez komputer, która nieustannie posuwa się do przodu, stanowiąc element presji czasu i rywala dla graczy. Jego szybkość może zależeć od błędnych odpowiedzi graczy.
5.  **Pola Specjalne:** Plansza zawiera pola specjalne, takie jak "Bonus" (nagroda), "Porażka" (kara) czy "Egzamin" (potencjalnie trudniejsze wyzwanie).
6.  **Warunki Końca Gry:** Gra kończy się, gdy pierwszy gracz dotrze do mety (wygrana) lub gdy Pionek Profesora dogoni wszystkich aktywnych graczy (przegrana).

## Technologie

*   **Język programowania:** Python 3.13.3
*   **Główna biblioteka graficzna i gry:** Pygame
*   **(Potencjalnie w przyszłości):** Bazy danych (np. SQLite), narzędzia do budowania interfejsu, obsługa sieci.

## Główne Funkcje (Zaimplementowane/Planowane)

*   [X] **Menu Główne:** Start gry, Wyjście.
*   [ ] **Wyświetlanie Planszy i Pionków:** Statyczny widok planszy, renderowanie pionków graczy i profesora.
*   [ ] **Rzut Kostką:** Logika losowania i wizualny feedback.
*   [ ] **Ruch Pionka Gracza:** Logika i podstawowa animacja ruchu.
*   [ ] **Zarządzanie Turami:** Przełączanie między graczami.
*   [ ] **System Pytań:** Ładowanie pytań z pliku, wyświetlanie karty pytania.
*   [ ] **Weryfikacja Odpowiedzi:** Sprawdzanie poprawności i logika konsekwencji.
*   [ ] **Karty Informacji Zwrotnej:** Wyświetlanie "Poprawna"/"Błędna".
*   [ ] **Ruch Pionka Profesora:** Logika i animacja ruchu AI.
*   [ ] **Logika Pól Specjalnych:** Podstawowe efekty Bonus/Porażka/Egzamin.
*   [ ] **Warunki Zwycięstwa/Porażki:** Sprawdzanie końca gry.
*   [ ] **Ekran Końca Gry:** Wyświetlanie wyników i opcji.
*   [ ] **Obsługa wielu graczy lokalnych** (2+).
*   [ ] **Efekty dźwiękowe.**

*(Legenda: [X] - Częściowo/W pełni zaimplementowane, [ ] - Do zaimplementowania)*

## Struktura Projektu

WyscigPoZaliczenie/
│
├── src/                     # Główny folder z kodem źródłowym gry
│   ├── main.py              # Punkt startowy aplikacji, główna pętla gry
│   └── ...                  # Inne moduły Pythona (.py)
│
├── assets/                  # Zasoby gry
│   ├── images/              # Pliki graficzne (.png, .jpg)
│   ├── fonts/               # Pliki czcionek (.ttf, .otf)
│   ├── sounds/              # Pliki dźwiękowe (.wav, .ogg)
│   └── data/                # Pliki danych (np. pytania .json, .csv)
│
├── docs/                    # Dokumentacja projektowa
│   ├── DOKUMENTACJA PROJEKTOWA.pdf
│   └── BRAND BOOK.pdf
│
├── .gitignore               # Plik ignorowania dla Git
├── LICENSE                  # Plik licencji
├── README.md                # Ten plik
└── requirements.txt         # Zależności Python 

## Dokumentacja Projektowa

Szczegółowa dokumentacja koncepcyjna, analiza potrzeb oraz księga tożsamości wizualnej (Brand Book) znajdują się w folderze `/docs`.

## Licencja

Ten projekt jest udostępniany na licencji MIT
