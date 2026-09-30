# Track pipeline tools

Scripts that turn a racetrackdesigner.com track into the mod's track JSON. They
live outside the `2026_f1` pack so they are never shipped with the mod.

## Setup

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt     # Windows; use .venv/bin/pip elsewhere
```

## Build a track

Inputs, per track (see the pipeline guide for how the images are prepared):
1. the line-art image with the coloured markers (red start/finish, green DRS detection,
   magenta DRS start/end, cyan sector splits);
2. the speed-map image with the 10-band legend and the white start dot.

```bash
.venv/Scripts/python build_track.py lineart.png speedmap.png \
    --name Bahrain --nationality bahraini --length-km 5.01 \
    --out ../../2026_f1/tracks/Bahrain.json --overlay bahrain-check.png
```

`--length-km` is the length label printed on the designer image; it is not derived.
Useful options: `--smooth` (default 15), `--min-frac` (default 0.016, sweep 0.014-0.018),
`--direction forward|reverse`.

Always open the overlay PNG and confirm every marker lines up with its source dot. The
script warns when the direction of travel is a close call or when there are no DRS
markers (then it cannot infer the direction and you must pass `--direction`).

## Check a finished track

```bash
.venv/Scripts/python check_track.py ../../2026_f1/tracks
```

Checks required fields, `length_pct` summing to 100, the 15-22 micro-sector range,
sectors under 1.4% of the lap, type vs speed consistency, sector splits, DRS values and
the loop closing. It does not replace the single-lap in-game test.

## What was verified (Sept 2026)

Rebuilt Bahrain, Canada and Australia from the source images and compared with the
finished files. Sector splits matched to within 0.001, DRS zones within 0.003 and the
weighted-average speed within about 2% (Australia within 0.1%). Not verified: the exact
low/med/high/straight speed boundaries (117, 168 and 240 km/h were inferred from the finished
tracks), the direction-of-travel rule (the original process is undocumented) and anything
on tracks other than these three.
