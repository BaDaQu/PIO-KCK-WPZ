# src/text_utility.py
import pygame
import settings


def render_text_in_rect(surface, text, font_path, initial_font_size, color, rect, vertical_align='top',
                        horizontal_align='center', line_spacing_multiplier=1.1, padding=5, min_font_size=14,
                        return_final_y=False):
    """
    Renderuje tekst wieloliniowy, dynamicznie zmniejszając czcionkę, aby zmieścił się
    w danym prostokącie. Obsługuje wyrównanie pionowe i poziome.
    """
    current_font_size = initial_font_size
    font = pygame.font.Font(font_path, current_font_size)

    # Pętla dopasowująca rozmiar czcionki
    while current_font_size > min_font_size:
        max_width = rect.width - 2 * padding
        max_height = rect.height - 2 * padding

        # --- Sprawdzenie, czy najdłuższe słowo mieści się w szerokości ---
        words = text.split(' ')
        longest_word_width = 0
        if words:
            longest_word_width = max(font.size(word)[0] for word in words)

        if longest_word_width > max_width:
            current_font_size -= 1
            font = pygame.font.Font(font_path, current_font_size)
            continue

        # --- Złamanie tekstu na linie dla bieżącej czcionki ---
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

        # --- Sprawdzenie, czy złamane linie mieszczą się w pionie ---
        line_height = font.get_linesize() * line_spacing_multiplier
        total_height_needed = len(lines_text_processed) * line_height

        if total_height_needed <= max_height:
            break
        else:
            current_font_size -= 1
            if current_font_size < min_font_size: current_font_size = min_font_size
            font = pygame.font.Font(font_path, current_font_size)
            if current_font_size <= min_font_size: break

    # --- Ostateczne renderowanie ---
    rendered_line_surfaces = [font.render(line, True, color) for line in lines_text_processed if line.strip()]
    if not rendered_line_surfaces:
        if return_final_y:
            return rect.top
        else:
            return

    final_line_height = font.get_linesize() * line_spacing_multiplier
    final_total_height = (len(rendered_line_surfaces) - 1) * final_line_height + font.get_height()

    if vertical_align == 'center':
        start_y = rect.centery - final_total_height / 2
    elif vertical_align == 'bottom':
        start_y = rect.bottom - final_total_height - padding
    else:
        start_y = rect.top + padding

    final_y = start_y
    for i, line_surface in enumerate(rendered_line_surfaces):
        if horizontal_align == 'left':
            line_rect = line_surface.get_rect(left=rect.left + padding, top=start_y + i * final_line_height)
        elif horizontal_align == 'right':
            line_rect = line_surface.get_rect(right=rect.right - padding, top=start_y + i * final_line_height)
        else:  # 'center'
            line_rect = line_surface.get_rect(centerx=rect.centerx, top=start_y + i * final_line_height)

        final_y = line_rect.bottom
        clipped_rect = line_rect.clip(rect)
        if clipped_rect.width > 0 and clipped_rect.height > 0:
            surface.blit(line_surface, line_rect, area=clipped_rect.move(-line_rect.left, -line_rect.top))

    if return_final_y:
        return final_y


def render_text_with_outline(font, text, base_color, outline_color, outline_width=2):
    """
    Renderuje tekst z obrysem. Zwraca jedną powierzchnię z efektem.
    """
    # 1. Renderuj tekst obrysu
    outline_surface = font.render(text, True, outline_color)

    # 2. Renderuj główny tekst
    base_surface = font.render(text, True, base_color)

    # 3. Stwórz nową, większą powierzchnię, która pomieści tekst i obrys
    w = base_surface.get_width() + 2 * outline_width
    h = base_surface.get_height() + 2 * outline_width
    final_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    final_surface.fill((0, 0, 0, 0))  # Wypełnij przezroczystością

    # 4. Narysuj tekst obrysu kilka razy z przesunięciem (8 kierunków)
    offsets = [
        (outline_width, 0), (-outline_width, 0), (0, outline_width), (0, -outline_width),
        (outline_width, outline_width), (-outline_width, -outline_width),
        (outline_width, -outline_width), (-outline_width, outline_width)
    ]

    for dx, dy in offsets:
        final_surface.blit(outline_surface, (outline_width + dx, outline_width + dy))

    # 5. Narysuj główny tekst na wierzchu
    final_surface.blit(base_surface, (outline_width, outline_width))

    return final_surface