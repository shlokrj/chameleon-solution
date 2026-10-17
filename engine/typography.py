"""Bounded font fitting against the vendored renderer's wrapping behavior."""
from functools import lru_cache
from pathlib import Path
import skia
from renderer.converter.brand_fonts import load_brand_font_manager
from renderer.converter.wrap import wrap_text


@lru_cache(maxsize=1)
def font_manager():
    return load_brand_font_manager(str(Path(__file__).resolve().parents[1] / 'brand_kit/fonts'))


@lru_cache(maxsize=64)
def font_data(family, weight, style):
    return skia.Typeface.MakeFromData(font_manager().lookup(family, weight, style))


def style_name(weight, italic):
    return ('bolditalic' if italic else 'bold') if weight == 'bold' else ('italic' if italic else 'regular')


def text_extent(el, size, width):
    """Return wrapped width, height, lines; never rewrite source content.

    Wrap uses the base font, as in convert.py. Measuring styled characters
    includes the converter's inclusive run end and conservatively includes
    spacing at run boundaries. This is a fit estimate, not a pixel oracle.
    """
    text = el['content']
    if not text:
        return 0.0, 0.0, 0
    family = el['font_family']
    weight = el.get('font_weight', 'regular')
    italic = el.get('font_style', 'normal') == 'italic'
    style = style_name(weight, italic)
    # Match renderer glyph advances while reusing the bounded typeface cache.
    # Font objects stay local: sizes vary during fitting and must not leak state.
    base_font = skia.Font(font_data(family, weight, style), size)
    widths = base_font.getWidths(base_font.textToGlyphs(text))
    wrapped = wrap_text(text, widths, width)
    styles = [(weight, italic)] * len(text)
    for run in el.get('style_runs', []):
        for i in range(max(0, run['start']), min(len(text), run['end'] + 1)):
            old_weight, old_italic = styles[i]
            styles[i] = (run.get('font_weight', old_weight),
                         run.get('font_style', 'italic' if old_italic else 'normal') == 'italic')
    base_metrics = base_font.getMetrics()
    metrics = ({(weight, italic): (widths, base_metrics.fDescent-base_metrics.fAscent)}
               if (weight, italic) in styles else {})
    for w, it in set(styles) - {(weight, italic)}:
        font = skia.Font(font_data(family, w, style_name(w, it)), size)
        glyph_widths = font.getWidths(font.textToGlyphs(text))
        fm = font.getMetrics()
        metrics[(w, it)] = (glyph_widths, fm.fDescent - fm.fAscent)
    line_width, widest, count = 0.0, 0.0, 1
    spacing = max(0, el.get('letter_spacing', 0))
    for i, c in enumerate(wrapped):
        if c == '\n':
            widest = max(widest, line_width)
            line_width = 0.0
            count += 1
        else:
            advances = metrics[styles[i]][0]
            line_width += (advances[i] if i < len(advances) else size) + spacing
    height = (count - 1) * size * el.get('line_height', 1.2) + max(m[1] for m in metrics.values())
    return max(widest, line_width), height, count


def fit_text(el, upper):
    low, high = 1.0, max(1.0, upper)
    w, h, lines = text_extent(el, high, el['width'])
    if w <= el['width'] and h <= el['height'] and (el.get('max_lines') is None or lines <= el['max_lines']):
        el['font_size'] = high
        return
    for _ in range(18):
        size = (low + high) / 2
        w, h, lines = text_extent(el, size, el['width'])
        if w <= el['width'] and h <= el['height'] and (el.get('max_lines') is None or lines <= el['max_lines']):
            low = size
        else:
            high = size
    el['font_size'] = low
