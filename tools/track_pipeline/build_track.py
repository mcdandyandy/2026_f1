"""Build a track JSON from a line-art marker image and a speed-map image.

Example:
    python build_track.py bahrain-poster.png bahrain-speed-map.png \
        --name Bahrain --nationality bahraini --length-km 5.01 \
        --out ../../2026_f1/tracks/Bahrain.json --overlay bahrain-check.png

The line-art image needs the coloured markers (red start/finish, green DRS
detection, magenta DRS start/end, cyan sector splits). Without DRS markers the
direction of travel cannot be inferred: pass --direction forward|reverse.
"""
import argparse
import json

import trackpipe as tp


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lineart")
    ap.add_argument("speedmap")
    ap.add_argument("--name", required=True, help="track_name written to the JSON")
    ap.add_argument("--nationality", required=True, help="lowercase demonym, e.g. australian")
    ap.add_argument("--length-km", type=float, required=True, help="length label from the designer image")
    ap.add_argument("--out", required=True, help="output JSON path")
    ap.add_argument("--canvas", nargs=2, type=int, default=[1080, 1350], help="raw_canvas_size (default 1080 1350)")
    ap.add_argument("--smooth", type=int, default=15, help="smooth_window (default 15)")
    ap.add_argument("--min-frac", type=float, default=0.016, help="min_frac, sweep 0.014-0.018 (default 0.016)")
    ap.add_argument("--epsilon", type=float, default=1.3, help="Douglas-Peucker epsilon (default 1.3)")
    ap.add_argument("--direction", choices=["forward", "reverse"], help="force the direction of travel")
    ap.add_argument("--overlay", help="also write a verification overlay PNG")
    a = ap.parse_args()

    track, diag = tp.build_track(a.lineart, a.speedmap, a.length_km, a.name, a.nationality, canvas=tuple(a.canvas),
                                 smooth_window=a.smooth, min_frac=a.min_frac, epsilon=a.epsilon,
                                 force_direction=a.direction)
    if diag["sanity_bad"]:
        print("SANITY CHECK FAILED for", len(diag["sanity_bad"]), "micro-sector(s):")
        for b in diag["sanity_bad"]:
            print("  ", b)
    print(f"{diag['n_sectors']} micro-sectors (target 15-22), length_pct sum {diag['pct_sum']}, "
          f"sectors under min_frac: {diag['short'] or 'none'}")
    with open(a.out, "w", encoding="utf-8", newline="") as fh:
        json.dump(track, fh, indent=2)
    print("wrote", a.out)
    if a.overlay:
        tp.render_verification_overlay(a.lineart, track, a.overlay)
        print("wrote overlay", a.overlay, "- check every marker lines up before trusting the JSON")
    print("Next: run check_track.py on the output, then a single-lap in-game test (guide section 8).")


if __name__ == "__main__":
    main()
