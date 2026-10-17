# M4 typography optimization: static independent review

Base HEAD/origin main verified at 338b50c7ec2a9ef5d3b556d414cdded6aebe75f2. Reviewed uncommitted engine/typography.py and new tests/test_typography.py, together with renderer/converter/wrap.py, convert.py text handling and brand font loading. Read-only code review only while parent runs sequential profiles: no tests, render jobs, benchmarks or performance claims from this reviewer. Only this report written; no Git/production/tracker changes.

**No actionable correctness regression found in the inspected optimization.**

- The removed char_widths call uses lookup → Typeface.MakeFromData → local skia.Font(size) → textToGlyphs → getWidths. Replacement performs the same operations with the existing cached typeface and fresh local Font. getWidths output is consumed identically by wrap_text; no different line-breaking algorithm introduced.
- Wrapping continues to use base font even for styled text, matching converter. Style-run inclusive endpoints, precedence and unchanged string indices remain as before; the schema/end-exclusive discrepancy is preexisting and not worsened.
- Unstyled and mixed text reuse base advances/height exactly when that base style occurs in the styles array. Fully overridden text excludes the unused base metrics, preserving previous max-height behavior. The set subtraction computes each non-base style once. Empty text returns before metrics/max operations.
- Cached state remains only typefaces in the preexisting 64-entry LRU and one font manager. No size, glyph list, text or mutable Font object stored globally. Per-call Font creation avoids interleaved sizes contaminating one another. No new unbounded cache or input mutation found. Brand-font contents are assumed immutable during a process, an existing cache assumption.

Tests read, not run: base width/height parity covers varying sizes/widths, Unicode, newlines, spaces and empty text; fully styled bolditalic case; repeated/interleaved calls and cache-size declaration. Optional validation strengthening: use deliberately unequal mocked font ascents/descents for the fully styled case, since shipped font variants may share metrics and therefore accidentally including unused base height might escape that particular fixture. Mixed/overlapping style-run parity is not directly covered by the new file, though that loop is unchanged.

Preexisting limitations remain: positive letter spacing handled conservatively, negative spacing clamped in measurement, renderer/schema style endpoint discrepancy, and measured glyph advances do not prove full rendered pixel bounds. No claim that this optimization fixes those issues. Parent's structural/render parity and sequential profiles are still required before acceptance.

Same inherited model, separate context, shared checkout with procedural isolation only; not cross-model or sealed review.
