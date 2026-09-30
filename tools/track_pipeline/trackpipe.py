"""Track map -> JSON pipeline (stages follow track-map-pipeline-guide.md).

Every stage is a separate function so it can be re-run on its own.
"""
import json
import math

import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.ndimage import convolve, uniform_filter1d
from scipy.spatial import cKDTree
from skimage.measure import approximate_polygon
from skimage.morphology import skeletonize

KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
LEGEND_SPEEDS = np.array([345, 305, 267, 242, 217, 190, 160, 122, 80, 45], float)
# boundaries between low/med/high/straight, inferred from the finished tracks
CAT_BOUNDS = (117.0, 168.0, 240.0)
CATS = ("low", "med", "high", "straight")


def load_rgb(path):
    return np.asarray(Image.open(path).convert("RGB")).astype(int)


# ------------------------------------------------------------------ line art
def extract_track_mask(arr, ymin=0.06, ymax=0.80, xmin=0.03, xmax=0.97):
    H, W, _ = arr.shape
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    mx, mn = arr.max(axis=2), arr.min(axis=2)
    sat = mx - mn
    region = np.zeros((H, W), bool)
    region[int(ymin * H):int(ymax * H), int(xmin * W):int(xmax * W)] = True
    white = (mx > 150) & (sat < 30) & region
    color = (sat > 60) & (mx > 80) & region
    lbl, n = ndimage.label(color, structure=np.ones((3, 3)))
    blobs = []
    for i in range(1, n + 1):
        m = lbl == i
        area = int(m.sum())
        if area < 30:
            continue
        ys, xs = np.nonzero(m)
        col = arr[m].mean(axis=0)
        blobs.append(dict(mask=m, area=area, x=float(xs.mean()), y=float(ys.mean()), color=col, kind=classify(col)))
    return white, blobs


def classify(col):
    r, g, b = col
    # most specific first: cyan needs high g AND high b, green needs high g and LOW b
    if g > 140 and b > 140 and r < 100:
        return "cyan"
    if r > 140 and b > 140 and g < 100:
        return "magenta"
    if g > 140 and r < 100 and b < 100:
        return "green"
    if r > 140 and g < 100 and b < 100:
        return "red"
    return "other"


def mark_on_line(white, blobs):
    track_dil = ndimage.binary_dilation(white, iterations=2)
    for bl in blobs:
        dil = ndimage.binary_dilation(bl["mask"], iterations=2)
        bl["overlap"] = int((dil & track_dil).sum())
        bl["on_line"] = bl["overlap"] > 5
    return blobs


def neighbour_counts(skel):
    return convolve(skel.astype(int), KERNEL, mode="constant") * skel.astype(int)


def prune_spurs(skel, iterations=30):
    sk = skel.copy()
    for _ in range(iterations):
        nc = neighbour_counts(sk)
        ends = (nc == 1) & sk
        if ends.sum() == 0:
            break
        sk[ends] = False
    return sk


def bridge_and_skeletonize(white, blobs, bridge_iters=(1, 0, 2, 3), prune=True):
    """Try several bridge dilations, prune spurs; return the first clean skeleton."""
    best = None
    for it in bridge_iters:
        fill = np.zeros_like(white)
        for bl in blobs:
            if bl["on_line"]:
                fill |= ndimage.binary_dilation(bl["mask"], iterations=it) if it else bl["mask"]
        mask = white | fill
        sk = skeletonize(mask)
        sk_p = prune_spurs(sk) if prune else sk
        nc = neighbour_counts(sk_p)
        branches = int((nc >= 3).sum())
        ends = int(((nc == 1) & sk_p).sum())
        cand = dict(skel=sk_p, iters=it, branches=branches, endpoints=ends)
        if best is None or (branches + ends) < (best["branches"] + best["endpoints"]):
            best = cand
        if branches == 0 and ends == 0:
            break
    return best


def trace_ordered_path(skel, start_xy):
    ys, xs = np.nonzero(skel)
    pts = np.column_stack([xs, ys]).astype(float)
    n = len(pts)
    tree = cKDTree(pts)
    cur = int(np.argmin((pts[:, 0] - start_xy[0]) ** 2 + (pts[:, 1] - start_xy[1]) ** 2))
    visited = np.zeros(n, bool)
    order = [cur]
    visited[cur] = True
    for _ in range(n - 1):
        d, idx = tree.query(pts[cur], k=min(12, n))
        nxt = None
        for dd, ii in zip(d, idx):
            if not visited[ii]:
                nxt = int(ii)
                break
        if nxt is None:
            rest = np.nonzero(~visited)[0]
            if len(rest) == 0:
                break
            dd = ((pts[rest] - pts[cur]) ** 2).sum(axis=1)
            nxt = int(rest[np.argmin(dd)])
        order.append(nxt)
        visited[nxt] = True
        cur = nxt
    o = pts[order]
    jumps = np.linalg.norm(np.diff(o, axis=0), axis=1)
    return o, dict(n=n, max_jump=float(jumps.max()), big_jumps=int((jumps > 5).sum()))


def progress_axis(ordered):
    diffs = np.linalg.norm(np.diff(ordered, axis=0), axis=1)
    cum = np.concatenate([[0], np.cumsum(diffs)])
    total = cum[-1] + np.linalg.norm(ordered[0] - ordered[-1])
    return cum, total


def nearest_progress(ordered, cum, total, px, py):
    idx = int(np.argmin((ordered[:, 0] - px) ** 2 + (ordered[:, 1] - py) ** 2))
    return cum[idx] / total


def reverse_keep_start(ordered):
    return np.concatenate([ordered[:1], ordered[1:][::-1]])


# ------------------------------------------------------------------ markers
def marker_progress(blobs, ordered):
    cum, total = progress_axis(ordered)
    out = {"cyan": [], "magenta": [], "green": []}
    for bl in blobs:
        if bl["kind"] in out:
            out[bl["kind"]].append(nearest_progress(ordered, cum, total, bl["x"], bl["y"]))
    return {k: sorted(v) for k, v in out.items()}


def _fwd(a, b):
    return (b - a) % 1.0


def pair_drs_zones(mag, green, reverse=False):
    """Pair magenta dots into zones using the green detection points.

    In the direction of travel a zone reads: detection -> start -> end.
    Returns (zones, score) where score is lower for a more consistent pairing.
    """
    mag = sorted(mag)
    green = sorted(green)
    if reverse:
        mag = sorted((1 - m) % 1.0 for m in mag)
        green = sorted((1 - g) % 1.0 for g in green)
    zones, gaps = [], []
    for g in green:
        nxt = sorted(range(len(mag)), key=lambda i: _fwd(g, mag[i]))
        s = nxt[0]
        e = min((i for i in range(len(mag)) if i != s), key=lambda i: _fwd(mag[s], mag[i]))
        zones.append(dict(detection=g, start=mag[s], end=mag[e]))
        gaps.append(_fwd(g, mag[s]))
    score = float(np.std(gaps) + max(gaps) * 0.5) if gaps else 9.9
    # zone ends must not pass the next detection point
    for i, z in enumerate(zones):
        nxt_det = zones[(i + 1) % len(zones)]["detection"]
        if _fwd(z["start"], z["end"]) > _fwd(z["start"], nxt_det) + 1e-9 and len(zones) > 1:
            score += 1.0
    return zones, score


def choose_direction(mag, green):
    _, s_f = pair_drs_zones(mag, green, reverse=False)
    _, s_r = pair_drs_zones(mag, green, reverse=True)
    return ("forward" if s_f <= s_r else "reverse"), s_f, s_r


def sector_splits_from(cyan, reverse=False, near_start=0.02):
    vals = sorted(((1 - c) % 1.0) if reverse else c for c in cyan)
    vals = [v for v in vals if near_start < v < 1 - near_start]
    return [round(v, 4) for v in vals[:2]]


# ------------------------------------------------------------------ speed map
def legend_colors(arr):
    H, W, _ = arr.shape
    x0, x1 = int(0.75 * W), int(0.79 * W)
    y0, y1 = int(0.19 * H), int(0.58 * H)
    sub = arr[y0:y1, x0:x1]
    sat = sub.max(axis=2) - sub.min(axis=2)
    m = (sat > 60) & (sub.max(axis=2) > 120)
    lbl, n = ndimage.label(m)
    sw = []
    for i in range(1, n + 1):
        mm = lbl == i
        if mm.sum() < 30:
            continue
        ys, _ = np.nonzero(mm)
        sw.append((ys.mean(), sub[mm].mean(axis=0)))
    sw.sort(key=lambda t: t[0])
    return np.array([c for _, c in sw])


def extract_speed_trace(arr):
    H, W, _ = arr.shape
    mx, mn = arr.max(axis=2), arr.min(axis=2)
    sat = mx - mn
    region = np.zeros((H, W), bool)
    region[int(0.17 * H):int(0.93 * H), int(0.02 * W):int(0.74 * W)] = True
    ribbon = (sat > 40) & (mx > 80) & region
    white = (mx > 215) & (sat < 40) & region
    lbl, n = ndimage.label(white, structure=np.ones((3, 3)))
    dots = [(int((lbl == i).sum()), i) for i in range(1, n + 1)]
    dots = [d for d in dots if d[0] > 20]
    if not dots:
        raise RuntimeError("no white start dot found")
    _, best = max(dots)
    dm = lbl == best
    ys, xs = np.nonzero(dm)
    start = (float(xs.mean()), float(ys.mean()))
    return ribbon, dm, start


def speed_profile(arr, ordered, start_xy, colors, ignore_r=13):
    """Return raw speed sample per ordered point (NaN near the start dot, then interpolated)."""
    H, W, _ = arr.shape
    sp = np.full(len(ordered), np.nan)
    for i, (x, y) in enumerate(ordered):
        if math.dist((x, y), start_xy) < ignore_r:
            continue
        x0, x1 = int(x) - 3, int(x) + 4
        y0, y1 = int(y) - 3, int(y) + 4
        patch = arr[max(y0, 0):y1, max(x0, 0):x1].reshape(-1, 3).astype(float)
        s = patch.max(axis=1) - patch.min(axis=1)
        good = patch[s > 40]
        c = good.mean(axis=0) if len(good) else patch.mean(axis=0)
        d2 = ((colors - c) ** 2).sum(axis=1) + 1.0
        w = 1.0 / d2
        sp[i] = (w * LEGEND_SPEEDS[: len(colors)]).sum() / w.sum()
    idx = np.arange(len(sp))
    ok = ~np.isnan(sp)
    sp[~ok] = np.interp(idx[~ok], idx[ok], sp[ok])
    return sp


def normalised(pts):
    p = pts - pts.mean(axis=0)
    h = np.ptp(pts[:, 1]) or 1.0
    return p / h


def check_trace_direction(line_pts, speed_pts, samples=40):
    """True when the speed-map trace must be reversed to run the same way as the line-art."""
    a, b = normalised(line_pts), normalised(speed_pts)
    fr = np.linspace(0, len(a) - 1, samples).astype(int)
    fb = np.linspace(0, len(b) - 1, samples).astype(int)
    fwd = np.linalg.norm(a[fr] - b[fb], axis=1).mean()
    rb = reverse_keep_start(b)
    rev = np.linalg.norm(a[fr] - rb[fb], axis=1).mean()
    return rev < fwd, float(fwd), float(rev)


# ------------------------------------------------------------------ micro sectors
def categorise(v):
    return np.digitize(v, CAT_BOUNDS)  # 0..3


def build_micro_sectors(raw, smooth_window=15, min_frac=0.016):
    """raw: per-point speeds in lap order, index 0 at start/finish (circular)."""
    N = len(raw)
    sm = uniform_filter1d(raw, size=smooth_window, mode="wrap")
    cats = categorise(sm)
    if np.all(cats == cats[0]):
        boundary = 0
    else:
        boundary = next(i for i in range(1, N) if cats[i] != cats[i - 1])
    rot = np.roll(raw, -boundary)
    rcat = np.roll(cats, -boundary)
    runs = []  # [start, end) in rotated frame
    s = 0
    for i in range(1, N + 1):
        if i == N or rcat[i] != rcat[s]:
            runs.append([s, i])
            s = i
    minlen = min_frac * N

    def stats(r):
        return rot[r[0]:r[1]].mean()

    while True:
        # relabel from the run's actual average, merge equal neighbours
        labs = [int(categorise(stats(r))) for r in runs]
        merged = True
        while merged and len(runs) > 1:
            merged = False
            for i in range(len(runs) - 1):
                if labs[i] == labs[i + 1]:
                    runs[i] = [runs[i][0], runs[i + 1][1]]
                    del runs[i + 1]
                    labs = [int(categorise(stats(r))) for r in runs]
                    merged = True
                    break
        short = [i for i, r in enumerate(runs) if r[1] - r[0] < minlen]
        if not short or len(runs) <= 2:
            break
        i = min(short, key=lambda k: runs[k][1] - runs[k][0])
        left = runs[i - 1] if i > 0 else None
        right = runs[i + 1] if i < len(runs) - 1 else None
        if left is None:
            tgt = i + 1
        elif right is None:
            tgt = i - 1
        else:
            m = stats(runs[i])
            tgt = i - 1 if abs(stats(left) - m) <= abs(stats(right) - m) else i + 1
        a, b = sorted((i, tgt))
        runs[a] = [runs[a][0], runs[b][1]]
        del runs[b]
    # rotate back so the list starts at lap index 0 (start/finish)
    out = []
    for r in runs:
        s0, e0 = r
        # positions in original frame
        os_, oe = (s0 + boundary) % N, (e0 + boundary) % N
        idxs = [(k + boundary) % N for k in range(s0, e0)]
        out.append(dict(start=idxs[0], idxs=idxs))
    # split any run crossing the seam
    pieces = []
    for o in out:
        idxs = o["idxs"]
        cut = next((j for j in range(1, len(idxs)) if idxs[j] < idxs[j - 1]), None)
        if cut is None:
            pieces.append(idxs)
        else:
            pieces.append(idxs[:cut])
            pieces.append(idxs[cut:])
    pieces.sort(key=lambda p: p[0])
    # a sliver left at the start/finish seam cannot be merged across it, so absorb it into its neighbour
    minlen = min_frac * N
    while len(pieces) > 2 and len(pieces[0]) < minlen:
        pieces[1] = pieces[0] + pieces[1]
        del pieces[0]
    while len(pieces) > 2 and len(pieces[-1]) < minlen:
        pieces[-2] = pieces[-2] + pieces[-1]
        del pieces[-1]
    secs = []
    for p in pieces:
        v = float(raw[p].mean())
        secs.append(dict(type=CATS[int(categorise(v))], length_pct=len(p) / N * 100.0, target_speed_kmh=round(v, 1)))
    tot = sum(s["length_pct"] for s in secs)
    for s in secs:
        s["length_pct"] = round(s["length_pct"] * 100.0 / tot, 4)
    secs[-1]["length_pct"] = round(100.0 - sum(s["length_pct"] for s in secs[:-1]), 4)
    return secs, pieces


def sanity_check_micro_sectors(secs, pieces, raw):
    bad = []
    for s, p in zip(secs, pieces):
        lo, hi = float(raw[p].min()), float(raw[p].max())
        if not (lo - 1e-6 <= s["target_speed_kmh"] <= hi + 1e-6):
            bad.append((s, lo, hi))
        if CATS[int(categorise(s["target_speed_kmh"]))] != s["type"]:
            bad.append((s, "category/speed mismatch"))
    return bad


# ------------------------------------------------------------------ assembly
def simplify(ordered, epsilon=1.3):
    closed = np.vstack([ordered, ordered[0]])
    return approximate_polygon(closed, tolerance=epsilon)


def assemble_track_json(points, splits, drs, secs, length_km, name, nationality, canvas):
    return {
        "points": [[int(round(x)), int(round(y))] for x, y in points],
        "sector_splits": [float(s) for s in splits],
        "tyre_wear_mult": 1.0,
        "fuel_consumption": 1.0,
        "dnf_modifier": 1.0,
        "lap_modifier": 1.0,
        "length_km": length_km,
        "track_name": name,
        "nationality": nationality,
        "overtaking_difficulty": 1.0,
        "use_raw_canvas_coordinates": True,
        "raw_canvas_size": list(canvas),
        "hide_polyline_visual": False,
        "micro_sectors": secs,
        "drs_zones": [dict(detection_progress=round(float(z["detection"]), 4), start_progress=round(float(z["start"]), 4),
                           end_progress=round(float(z["end"]), 4)) for z in drs],
    }


def build_track(lineart_path, speedmap_path, length_km, name, nationality, canvas=(1080, 1350),
                smooth_window=15, min_frac=0.016, epsilon=1.3, force_direction=None, log=print):
    la = load_rgb(lineart_path)
    white, blobs = extract_track_mask(la)
    mark_on_line(white, blobs)
    reds = [b for b in blobs if b["kind"] == "red"]
    start_blob = max(reds, key=lambda b: b["overlap"])
    log("markers:", {k: sum(1 for b in blobs if b["kind"] == k) for k in ("red", "green", "magenta", "cyan", "other")},
        "on-line:", [(b["kind"], round(b["x"]), round(b["y"])) for b in blobs if b["on_line"]])
    res = bridge_and_skeletonize(white, blobs)
    log("skeleton:", {k: res[k] for k in ("iters", "branches", "endpoints")})
    ordered, tinfo = trace_ordered_path(res["skel"], (start_blob["x"], start_blob["y"]))
    log("trace:", tinfo)
    prog = marker_progress(blobs, ordered)
    direction, sf, sr = choose_direction(prog["magenta"], prog["green"])
    if force_direction:
        direction = force_direction
    log("DRS direction:", direction, "scores", round(sf, 3), round(sr, 3),
        "(forced)" if force_direction else "")
    if not prog["green"] or not prog["magenta"]:
        log("WARNING: no DRS markers found - drs_zones will be empty and the direction of travel is a guess; "
            "pass force_direction='forward' or 'reverse'")
    elif abs(sf - sr) < 0.05 and not force_direction:
        log("WARNING: direction of travel is ambiguous (scores within 0.05) - check it with force_direction")
    rev = direction == "reverse"
    if rev:
        ordered = reverse_keep_start(ordered)
        prog = marker_progress(blobs, ordered)
    zones, score = pair_drs_zones(prog["magenta"], prog["green"])
    splits = sector_splits_from(prog["cyan"])
    # ---- speed map
    sm = load_rgb(speedmap_path)
    ribbon, dotmask, sxy = extract_speed_trace(sm)
    bridge = ndimage.binary_dilation(dotmask, iterations=3)
    best = None
    for it in (3, 2, 4, 1):
        mask = ribbon | ndimage.binary_dilation(dotmask, iterations=it)
        sk = prune_spurs(skeletonize(mask))
        nc = neighbour_counts(sk)
        b_, e_ = int((nc >= 3).sum()), int(((nc == 1) & sk).sum())
        if best is None or b_ + e_ < best[1] + best[2]:
            best = (sk, b_, e_, it)
        if b_ == 0 and e_ == 0:
            break
    sk_s, b_, e_, it = best
    log("speed skeleton:", dict(iters=it, branches=b_, endpoints=e_))
    sp_ord, sinfo = trace_ordered_path(sk_s, sxy)
    log("speed trace:", sinfo)
    need_rev, dfwd, drev = check_trace_direction(ordered, sp_ord)
    log("direction match: reverse speed trace?", need_rev, round(dfwd, 3), round(drev, 3))
    if need_rev:
        sp_ord = reverse_keep_start(sp_ord)
    colors = legend_colors(sm)
    log("legend swatches found:", len(colors))
    raw = speed_profile(sm, sp_ord, sxy, colors)
    secs, pieces = build_micro_sectors(raw, smooth_window, min_frac)
    bad = sanity_check_micro_sectors(secs, pieces, raw)
    simp = simplify(ordered, epsilon)
    sx, sy = canvas[0] / la.shape[1], canvas[1] / la.shape[0]
    pts = [(x * sx, y * sy) for x, y in simp]
    track = assemble_track_json(pts, splits, zones, secs, length_km, name, nationality, canvas)
    diag = dict(sanity_bad=bad, n_sectors=len(secs), pct_sum=round(sum(s["length_pct"] for s in secs), 4),
                short=[round(s["length_pct"], 2) for s in secs if s["length_pct"] < min_frac * 100],
                raw=raw, ordered=ordered, sp_ord=sp_ord)
    return track, diag


# ------------------------------------------------------------------ verification overlay
SEC_COL = {"low": (230, 40, 40), "med": (240, 150, 30), "high": (230, 220, 40), "straight": (40, 210, 90)}


def render_verification_overlay(lineart_path, track, out_path):
    """Draw the extracted geometry, DRS zones, sector splits and micro-sector colours on the line-art image."""
    from PIL import ImageDraw
    im = Image.open(lineart_path).convert("RGB")
    W, H = im.size
    cw, ch = track["raw_canvas_size"]
    pts = np.array(track["points"], float) * [W / cw, H / ch]
    # arc-length progress along the extracted polyline
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    cum = np.concatenate([[0], np.cumsum(seg)])
    cum /= cum[-1]
    dr = ImageDraw.Draw(im)

    def at(p):
        p = p % 1.0
        x = np.interp(p, cum, pts[:, 0])
        y = np.interp(p, cum, pts[:, 1])
        return x, y

    pos = 0.0
    for s in track["micro_sectors"]:
        a, b = pos, pos + s["length_pct"] / 100.0
        steps = max(2, int((b - a) * 400))
        line = [at(a + (b - a) * k / steps) for k in range(steps + 1)]
        dr.line(line, fill=SEC_COL[s["type"]], width=7)
        pos = b
    for z in track["drs_zones"]:
        for key, colr in (("detection_progress", (0, 200, 255)), ("start_progress", (255, 0, 255)), ("end_progress", (255, 0, 255))):
            x, y = at(z[key])
            dr.ellipse([x - 9, y - 9, x + 9, y + 9], outline=colr, width=3)
    for sp in track["sector_splits"]:
        x, y = at(sp)
        dr.rectangle([x - 8, y - 8, x + 8, y + 8], outline=(255, 255, 255), width=3)
    x, y = at(0.0)
    dr.ellipse([x - 11, y - 11, x + 11, y + 11], outline=(255, 0, 0), width=4)
    im.save(out_path)
