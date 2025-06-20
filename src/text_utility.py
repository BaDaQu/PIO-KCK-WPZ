# src/text_utility.py
import pygame


def render_text_in_rect(surface, text, font_path, initial_font_size, color, rect, vertical_align='center',
                        line_spacing_multiplier=1.1, padding=5, min_font_size=14):
    """
    Renderuje tekst wieloliniowy wewnątrz danego prostokąta, inteligentnie
    dopasowując rozmiar czcionki, aby zmieścić cały tekst.
    """
    max_width = rect.width - 2 * padding
    max_height = rect.height - 2 * padding

    # Krok 1: Przygotujmy tekst do łamania na linie
    words = text.replace('\n', ' \n ').split(' ')
    current_font_size = initial_font_size
    font = pygame.font.Font(font_path, current_font_size)

    # --- Sprawdzenie, czy najdłuższe słowo w ogóle ma szansę się zmieścić ---
    # Jeśli nie, zmniejszamy czcionkę od razu.
    longest_word = ""
    if words:
        longest_word = max(words, key=lambda w: font.size(w)[0])

    while current_font_size > min_font_size and font.size(longest_word)[0] > max_width:
        current_font_size -= 1
        font = pygame.font.Font(font_path, current_font_size)

    # --- Krok 2: Złamanie tekstu na linie przy użyciu bieżącej (potencjalnie już zmniejszonej) czcionki ---
    lines_text_processed = []
    current_line_text = ""
    for word in words:
        if word == '\n':
            if current_line_text: lines_text_processed.append(current_line_text.strip())
            lines_text_processed.append("")
            current_line_text = ""
            continue

        test_line = current_line_text + word + " "
        if font.size(test_line.strip())[0] <= max_width:
            current_line_text = test_line
        else:
            if current_line_text.strip(): lines_text_processed.append(current_line_text.strip())
            current_line_text = word + " "
    if current_line_text.strip(): lines_text_processed.append(current_line_text.strip())

    # --- Krok 3: Sprawdzenie wysokości i ostateczne dopasowanie rozmiaru czcionki ---
    line_height = font.get_linesize() * line_spacing_multiplier
    total_height_needed = len(lines_text_processed) * line_height

    while total_height_needed > max_height and current_font_size > min_font_size:
        current_font_size -= 1
        font = pygame.font.Font(font_path, current_font_size)
        line_height = font.get_linesize() * line_spacing_multiplier
        total_height_needed = len(lines_text_processed) * line_height

    # --- Krok 4: Renderowanie tekstu z optymalnie dobraną czcionką ---
    rendered_line_surfaces = [font.render(line, True, color) for line in lines_text_processed if line.strip()]
    if not rendered_line_surfaces: return

    # Ponownie obliczamy wysokość dla finalnego rysowania
    final_line_height = font.get_linesize() * line_spacing_multiplier
    final_total_height = len(rendered_line_surfaces) * final_line_height

    # Obliczanie pozycji startowej Y w zależności od wyrównania
    if vertical_align == 'center':
        start_y = rect.centery - final_total_height / 2
    elif vertical_align == 'bottom':
        start_y = rect.bottom - final_total_height - padding
    else:  # 'top'
        start_y = rect.top + padding

    for i, line_surface in enumerate(rendered_line_surfaces):
        line_rect = line_surface.get_rect(centerx=rect.centerx, top=start_y + i * final_line_height)
        # Obcinanie, aby na pewno nie wyjść poza prostokąt
        clipped_rect = line_rect.clip(rect)
        if clipped_rect.width > 0 and clipped_rect.height > 0:
            surface.blit(line_surface, line_rect, area=clipped_rect.move(-line_rect.left, -line_rect.top))