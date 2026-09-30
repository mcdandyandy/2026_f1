"""Check finished track JSON files against the mod's track rules (read-only).

Usage:  python check_track.py path/to/track.json [more.json ...]
        python check_track.py ../../2026_f1/tracks        (every .json in a folder)

Exits 1 if any ERROR is found. WARN means "look at it".
"""
import glob
import json
import math
import os
import sys

SPEED_RANGES = {"low": (0, 130), "med": (100, 190), "high": (150, 260), "straight": (230, 400)}
REQUIRED = ["points", "sector_splits", "length_km", "micro_sectors", "drs_zones"]
# older tracks in the pack lack these and still load, so they only warn
EXPECTED = ["tyre_wear_mult", "fuel_consumption", "dnf_modifier", "lap_modifier",
            "use_raw_canvas_coordinates", "raw_canvas_size"]
MIN_FRAC = 1.4  # percent of the lap
ZONES = (15, 22)


def check(path):
    e, w = [], []
    try:
        t = json.load(open(path, encoding="utf-8"))
    except Exception as ex:  # noqa: BLE001
        return [f"invalid JSON: {ex}"], []
    for k in REQUIRED:
        if k not in t:
            e.append(f"missing '{k}'")
    for k in EXPECTED:
        if k not in t:
            w.append(f"missing '{k}' (older tracks omit it)")
    if "track_name" not in t and "name" not in t:
        w.append("no track_name/name field")
    ms = t.get("micro_sectors") or []
    if not ms:
        e.append("micro_sectors is empty (the game refuses to practise without it)")
    total = sum(m.get("length_pct", 0) for m in ms)
    if ms and abs(total - 100.0) > 0.01:
        e.append(f"length_pct sums to {total:.4f}, not 100")
    for i, m in enumerate(ms):
        ty, sp = m.get("type"), m.get("target_speed_kmh")
        if ty not in SPEED_RANGES:
            e.append(f"micro_sectors[{i}] bad type '{ty}'")
            continue
        lo, hi = SPEED_RANGES[ty]
        if sp is None or not (lo <= sp <= hi):
            w.append(f"micro_sectors[{i}] {ty} at {sp} km/h looks inconsistent (expected {lo}-{hi})")
        if m.get("length_pct", 0) < MIN_FRAC:
            w.append(f"micro_sectors[{i}] is only {m['length_pct']:.2f}% of the lap (under {MIN_FRAC}%)")
    if ms and not (ZONES[0] <= len(ms) <= ZONES[1]):
        w.append(f"{len(ms)} micro-sectors (target {ZONES[0]}-{ZONES[1]})")
    ss = t.get("sector_splits", [])
    if len(ss) > 2:
        e.append("more than 2 sector_splits (game cap)")
    if any(not (0 < s < 1) for s in ss) or ss != sorted(ss):
        e.append(f"sector_splits {ss} must be ascending values between 0 and 1")
    if not ss:
        w.append("no sector_splits")
    for i, z in enumerate(t.get("drs_zones", [])):
        for k in ("detection_progress", "start_progress", "end_progress"):
            if k not in z or not (0 <= z[k] <= 1):
                e.append(f"drs_zones[{i}].{k} missing or outside 0-1")
        if all(k in z for k in ("detection_progress", "start_progress")):
            gap = (z["start_progress"] - z["detection_progress"]) % 1.0
            if not (0.0 < gap < 0.15):
                w.append(f"drs_zones[{i}] detection->start gap {gap:.3f} looks wrong (usually about 0.05-0.08)")
    pts = t.get("points", [])
    if len(pts) < 10:
        e.append("fewer than 10 points")
    elif math.dist(pts[0], pts[-1]) > 1e-6:
        w.append("points do not close the loop (first != last)")
    cs = t.get("raw_canvas_size")
    if cs and pts:
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        if min(xs) < 0 or min(ys) < 0 or max(xs) > cs[0] or max(ys) > cs[1]:
            e.append("points fall outside raw_canvas_size")
    if not t.get("length_km") or not (1.0 < t["length_km"] < 10.0):
        w.append(f"length_km {t.get('length_km')} looks odd")
    return e, w


def main():
    paths = []
    for a in sys.argv[1:] or ["."]:
        paths += sorted(glob.glob(os.path.join(a, "*.json"))) if os.path.isdir(a) else [a]
    bad = 0
    for p in paths:
        e, w = check(p)
        status = "FAIL" if e else ("warn" if w else "ok")
        print(f"[{status:4}] {os.path.basename(p)}")
        for m in e:
            print("        ERROR", m)
        for m in w:
            print("        warn ", m)
        bad += bool(e)
    print(f"\n{len(paths)} file(s), {bad} with errors")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
