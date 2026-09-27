from app.engines.helpers import ceil_units


def panel_count(window_w: float, fullness: float, fabric_width: float) -> int:
    if fabric_width <= 0:
        raise ValueError("fabric width required")
    finished_w = float(window_w) * float(fullness)
    return max(1, ceil_units(finished_w / float(fabric_width)))


def fabric_meters(
    window_w: float,
    window_h: float,
    fullness: float,
    hem_top: float,
    hem_bottom: float,
    fabric_width: float,
) -> dict:
    panels = panel_count(window_w, fullness, fabric_width)
    finished_w = float(window_w) * float(fullness)
    cut_h = float(window_h) + float(hem_top) + float(hem_bottom)
    meters = panels * cut_h
    return {
        "finished_width": round(finished_w, 3),
        "panels": panels,
        "cut_height": round(cut_h, 3),
        "meters": round(meters, 2),
        "fabric_width": float(fabric_width),
    }


def lining_meters(window_h: float, panels: int, hem_top: float, hem_bottom: float) -> dict:
    hem_top = float(hem_top)
    hem_bottom = float(hem_bottom)
    if hem_top < 0 or hem_bottom < 0:
        raise ValueError("lining hem must be >= 0")
    cut_h = float(window_h) + hem_top + hem_bottom
    meters = int(panels) * cut_h
    return {
        "panels": int(panels),
        "cut_height": round(cut_h, 3),
        "meters": round(meters, 2),
        "hem_top": hem_top,
        "hem_bottom": hem_bottom,
    }
