# src/text_utility.py
import pygame


def _render_single_line_with_outline(font, text, base_color, outline_color, outline_width):
    """Pomocnicza funkcja do renderowania JEDNEJ linii tekstu z obrysem."""
    base_surface = font.render(text, True, base_color)
    outline_surface = font.render(text, True, outline_color)
    w = base_surface.get_width() + 2 * outline_width
    h = base_surface.get_height() + 2 * outline_width
    final_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    final_surface.fill((0, 0, 0, 0))
    offsets = [
        (-outline_width, -outline_width), (-outline_width, 0), (-outline_width, outline_width),
        (0, -outline_width), (0, outline_width), (outline_width, -outline_width),
        (outline_width, 0), (outline_width, outline_width)
    ]
    for dx, dy in offsets:
        final_surface.blit(outline_surface, (outline_width + dx, outline_width + dy))
    final_surface.blit(base_surface, (outline_width, outline_width))
    return final_surface


def render_text(surface, text, font_path, initial_font_size, color, rect,
                outline_color=None, outline_width=0,
                vertical_align='center', horizontal_align='center',
                line_spacing_multiplier=1.1, padding=5, min_font_size=14,
                return_final_y=False):  # <-- DODANY BRAKUJĄCY ARGUMENT
    """
    Główna, uniwersalna funkcja do renderowania tekstu.
    Inteligentnie dopasowuje rozmiar czcionki, łamie linie i opcjonalnie dodaje obrys.
    Rysuje tekst bezpośrednio na podanej powierzchni `surface`.
    """
    max_width = rect.width - 2 * padding
    max_height = rect.height - 2 * padding

    current_font_size = initial_font_size
    font = pygame.font.Font(font_path, current_font_size)

    # --- Pętla dopasowująca rozmiar czcionki ---
    while current_font_size >= min_font_size:
        words = text.replace('\n', ' \n ').split(' ')
        longest_word = max(words, key=lambda w: font.size(w)[0]) if words else ""
        if font.size(longest_word)[0] > max_width:
            current_font_size -= 1
            if current_font_size < min_font_size: break
            font = pygame.font.Font(font_path, current_font_size)
            continue

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

        line_height = font.get_linesize() * line_spacing_multiplier
        total_height_needed = (
                                          len(lines_text_processed) - 1) * line_height + font.get_height() if lines_text_processed else 0

        if total_height_needed <= max_height:
            break
        else:
            current_font_size -= 1
            if current_font_size < min_font_size: break
            font = pygame.font.Font(font_path, current_font_size)

    # --- Ostateczne renderowanie ---
    final_y = rect.top  # Domyślna wartość, jeśli nic nie zostanie narysowane

    if not lines_text_processed:
        if return_final_y: return final_y
        return

    final_line_height = font.get_linesize() * line_spacing_multiplier
    final_total_height = (len(lines_text_processed) - 1) * final_line_height + font.get_height()

    if vertical_align == 'center':
        start_y = rect.centery - final_total_height / 2
    elif vertical_align == 'bottom':
        start_y = rect.bottom - final_total_height - padding
    else:  # 'top'
        start_y = rect.top + padding

    for i, line_text in enumerate(lines_text_processed):
        if not line_text.strip():
            final_y = start_y + (i + 1) * final_line_height  # Aktualizuj Y nawet dla pustych linii
            continue

        if outline_color and outline_width > 0:
            line_surface = _render_single_line_with_outline(font, line_text, color, outline_color, outline_width)
        else:
            line_surface = font.render(line_text, True, color)

        if horizontal_align == 'left':
            line_rect = line_surface.get_rect(left=rect.left + padding, top=start_y + i * final_line_height)
        elif horizontal_align == 'right':
            line_rect = line_surface.get_rect(right=rect.right - padding, top=start_y + i * final_line_height)
        else:  # 'center'
            line_rect = line_surface.get_rect(centerx=rect.centerx, top=start_y + i * final_line_height)

        final_y = line_rect.bottom  # Zapisz pozycję dolnej krawędzi ostatnio narysowanej linii

        clipped_rect = line_rect.clip(rect)
        if clipped_rect.width > 0 and clipped_rect.height > 0:
            surface.blit(line_surface, clipped_rect, area=clipped_rect.move(-line_rect.left, -line_rect.top))

    if return_final_y:
        return final_y