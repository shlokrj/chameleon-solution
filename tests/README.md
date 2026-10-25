# Tests and regression fixtures

Run unit tests with `python -m unittest discover -s tests -v`, or use `scripts/verify-container.sh` from the repository root for offline Docker validation.

Saved task fixtures cover backing panels, rotation, source grids, styled and multiline text, explicit groups, transparent images, and small target canvases. Folder names reflect the development batches in which they were added. All are now ordinary regression cases, not unseen benchmarks.

```sh
python -m evaluation.regressions --fixtures tests/fixtures/m3 --output artifacts/m3
python -m evaluation.regressions --fixtures tests/fixtures/m5-review --output artifacts/group-labels
python -m evaluation.regressions --fixtures tests/fixtures/m5-holdout --output artifacts/group-interactions
python -m evaluation.regressions --fixtures tests/fixtures/m5-final --output artifacts/tail-copy
```

These commands validate the source and output, save output JSON, and render source/output PNG pairs. Inspect the images as well as the reports; structural validity does not guarantee readability.

`tests/fixtures/m5-final/verify.py` additionally compares the final text refinement with that pass disabled, checks input preservation and repeatability, and writes measured text-fit results. Run it from the repository root with `PYTHONPATH=.` and the development dependencies installed.
