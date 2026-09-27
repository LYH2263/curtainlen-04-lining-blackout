from fastapi import HTTPException
from app.engines.curtain_math import fabric_meters, lining_meters, panel_count
from app.repositories import fabrics, history, settings_repo, windows

def _resolve_hem(param, settings, key, default):
    if param is not None:
        return float(param)
    v = settings.get(key)
    if v is None or v == "":
        return float(default)
    return float(v)

def run_estimate(window_id: int, fabric_id: int, save: bool, note: str,
                 lining_enabled: bool = False, lining_hem_top=None, lining_hem_bottom=None):
    w = windows.get_window(window_id)
    f = fabrics.get_fabric(fabric_id)
    if not w or not f:
        raise HTTPException(404, "not found")
    if w.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty window")
    settings = settings_repo.get_all()
    fullness = float(w.get("fullness") or settings.get("default_fullness", 2.0))
    calc = fabric_meters(w["width"], w["height"], fullness, f["hem_top"], f["hem_bottom"], f["fabric_width"])
    lining = None
    if lining_enabled:
        hem_top = _resolve_hem(lining_hem_top, settings, "lining_hem_top", 0.10)
        hem_bottom = _resolve_hem(lining_hem_bottom, settings, "lining_hem_bottom", 0.10)
        if hem_top < 0 or hem_bottom < 0:
            raise HTTPException(422, "lining hem must be >= 0")
        lining = lining_meters(w["height"], calc["panels"], hem_top, hem_bottom)
    result = {**calc, "lining_enabled": bool(lining_enabled), "lining": lining}
    run_id = history.insert_run(window_id, fabric_id, result, note) if save else None
    return {"window": w, "fabric": f, "run_id": run_id, **result}

def panels_by_fabric(window_id: int):
    w = windows.get_window(window_id)
    if not w:
        raise HTTPException(404, "not found")
    settings = settings_repo.get_all()
    fullness = float(w.get("fullness") or settings.get("default_fullness", 2.0))
    items = fabrics.list_fabrics()
    for it in items:
        try:
            it["main_panels"] = panel_count(w["width"], fullness, it["fabric_width"])
        except (ValueError, TypeError):
            it["main_panels"] = None
    return items
