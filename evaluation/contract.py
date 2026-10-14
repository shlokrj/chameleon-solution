"""Structural checks independent of the starter self-check.

These do not prove readability, intentional overlap, or generalization.
"""
import math
from collections import Counter
from jsonschema import Draft202012Validator


def check_contract(source, target, output, schema):
    issues = []

    def add(code, detail):
        issues.append({"code": code, "detail": detail})

    def finite(value, path="output"):
        if isinstance(value, float) and not math.isfinite(value):
            add("C2", f"{path}: nonfinite number")
        elif isinstance(value, dict):
            for key, child in value.items():
                finite(child, f"{path}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                finite(child, f"{path}[{index}]")

    finite(output)
    errors = list(Draft202012Validator(schema).iter_errors(output))
    for error in errors:
        add("C2", f"{list(error.absolute_path)}: {error.message}")
    if errors or issues:
        return issues  # avoid arithmetic on malformed output
    if output["canvas"] != target:
        add("C2", "output canvas differs from target")
    src_ids = Counter(el["id"] for el in source["elements"])
    out_ids = Counter(el["id"] for el in output["elements"])
    if src_ids != out_ids or any(n != 1 for n in out_ids.values()):
        add("C1", "element IDs/counts are not preserved exactly once")
    originals = {el["id"]: el for el in source["elements"]}
    cw, ch = target["width"], target["height"]
    for el in output["elements"]:
        eid = el["id"]
        original = originals.get(eid)
        if original is None:
            continue
        if el["type"] != original["type"]:
            add("C1", f"{eid}: type changed")
        # Engineering policy: geometry/font size only, preserving absent fields too.
        mutable = {"x", "y", "width", "height", "font_size"}
        for key in (set(original) | set(el)) - mutable:
            if key not in original or key not in el or original[key] != el[key]:
                code = "C4" if key in {"content", "font_family"} else "C5" if key == "asset_id" else "policy"
                add(code, f"{eid}: {key} changed")
        x, y, w, h = (el[k] for k in ("x", "y", "width", "height"))
        angle = math.radians(el.get("rotation", 0))
        rw = abs(w * math.cos(angle)) + abs(h * math.sin(angle))
        rh = abs(w * math.sin(angle)) + abs(h * math.cos(angle))
        cx, cy = x + w / 2, y + h / 2
        if min(x, y, cx - rw / 2, cy - rh / 2) < -1e-6 or max(x+w, cx+rw/2) > cw+1e-6 or max(y+h, cy+rh/2) > ch+1e-6:
            add("C3", f"{eid}: box or rotated extent off canvas")
        if el["type"] == "image" and original.get("fit", "contain") != "cover":
            ow, oh = original["width"], original["height"]
            if ow > 0 and oh > 0 and (w <= 0 or h <= 0 or not math.isclose(w * oh, h * ow, rel_tol=1e-6)):
                add("C6", f"{eid}: source box aspect ratio changed")
    return issues
