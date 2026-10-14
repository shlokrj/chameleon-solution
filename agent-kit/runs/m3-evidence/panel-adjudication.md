# Challenger adjudication at frozen 3324d76

After completing independent six-case pass, inspected challenger reproduce.py and its literal fixtures. Copied script to reproduce_challenger.py with only destination changed to artifacts/m3-judge; executed `.venv/bin/python artifacts/m3-judge/reproduce_challenger.py`. Source schema, immutable inputs, asset hashes and independent structural checks all pass. Inspected real source/output PNGs for contrast-layer and zero-width-line. Challenger production source not inspected; no fixes proposed before judgment.

## Accepted: loss of intentional contrast/layering

contrast-layer is a minimal two-element valid source: ungrouped white SOLSTICE entirely on an opaque black panel, distinct z-indices. Group IDs are optional, so lack of grouping does not invalidate its readable source relationship. Source real render is fully readable. Output panel becomes x=135,y=90,w=210,h=65 while text becomes x=12,y=108,w=876,h=84,font≈60. Most glyphs land on white canvas; only fragments within the black panel remain visible. This violates SPEC quality objectives 1 (readable complete text on actual composited background) and 4 (intentional layering survives). It is not a C1–C6 JSON/box failure. Candidate 0 incorrectly gets local proxy loss 0 and terminates search. Priority P1 quality defect: core reading content is effectively hidden in a feasible sparse composition.

Reproducer, exact literal source, output, full diagnostics and independently rendered PNGs are in this directory. Two elements are minimal for this contrast relationship. Preserve fixture unchanged as exposed regression. Require a real rendered fix with source text still legible on preserved contrast support; merely making proxy loss nonzero is not sufficient.

## Separate: zero-width line collapse

Valid source is one line at (200,100), width 0, height 200, target unchanged 400x400. Returned width and height both become 0 at (200,200). This is reproducible avoidable geometry loss under identity resize, and zero-area handling warrants a regression; however dimension preservation is not a blanket hard contract and source renderer already draws nothing. Both real PNGs are blank. Therefore accept the factual collapse as a semantic preservation concern, not a newly demonstrated visual regression or hard C1–C6 failure. Any future fix preserving 200px extent can establish geometry repair but cannot claim visible line restoration without renderer work.

negative-tracking was run by the shared reproducer but is not a proposed or accepted failure; its real PNGs were not visually adjudicated here.

Roles used same inherited model and shared filesystem with procedural isolation. No independent model comparison, sealed filesystem, Docker, official scoring or benchmark performed.
