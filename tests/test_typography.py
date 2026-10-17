"""Compare optimized measurements to the unchanged renderer's font operations."""
import unittest
from unittest.mock import patch
import skia
from engine.typography import text_extent, font_data, font_manager
from renderer.converter.wrap import char_widths, wrap_text


class TypographyTests(unittest.TestCase):
    def element(self, content, **fields):
        return dict(content=content, font_family='Solstice Sans', **fields)

    def test_base_metrics_match_renderer_at_wrap_thresholds(self):
        for content in ['Hello world', 'A\nB', 'café — summer', '', 'NoSpacesHere', ' A  B ']:
            for size in [1, 12.25, 28, 55.5]:
                for width in [1, 40, 200]:
                    element = self.element(content)
                    result = text_extent(element, size, width)
                    if not content:
                        self.assertEqual(result, (0, 0, 0))
                        continue
                    advances = char_widths(font_manager(), 'Solstice Sans', 'regular', 'regular', size, content)
                    wrapped = wrap_text(content, advances, width)
                    lines, line_width = [], 0
                    for i, char in enumerate(wrapped):
                        if char == '\n':
                            lines.append(line_width)
                            line_width = 0
                        else:
                            line_width += advances[i]
                    lines.append(line_width)
                    font = skia.Font(skia.Typeface.MakeFromData(font_manager().lookup('Solstice Sans', 'regular', 'regular')), size)
                    m = font.getMetrics()
                    self.assertEqual(result, (max(lines), (len(lines)-1)*size*1.2+m.fDescent-m.fAscent, len(lines)))

    def test_fully_styled_text_does_not_inherit_unused_base_height(self):
        element = self.element('Styled', style_runs=[{'start': 0, 'end': 6, 'font_weight': 'bold', 'font_style': 'italic'}])
        measured = text_extent(element, 30, 500)
        font = skia.Font(font_data('Solstice Sans', 'bold', 'bolditalic'), 30)
        m = font.getMetrics()
        self.assertEqual(measured, (sum(font.getWidths(font.textToGlyphs('Styled'))), m.fDescent-m.fAscent, 1))

    def test_cache_is_bounded_and_sizes_remain_local(self):
        font_data.cache_clear()
        before = text_extent(self.element('Repeated text'), 24, 180)
        with patch('engine.typography.skia.Typeface.MakeFromData', side_effect=AssertionError('typeface rebuilt')):
            text_extent(self.element('Different text'), 12, 80)
            self.assertEqual(before, text_extent(self.element('Repeated text'), 24, 180))
        self.assertEqual(font_data.cache_info().maxsize, 64)
