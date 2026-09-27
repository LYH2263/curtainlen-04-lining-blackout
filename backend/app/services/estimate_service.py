from fastapi import HTTPException
from app.engines.curtain_math import fabric_meters, lining_meters
from app.repositories import fabrics, history, settings_repo, windows

DEFAULT_LINING_HEM = 0.1

def run_estimate(window_id: int, fabric_id: int, save: bool, note: str, lining: bool = False, lining_hem: float = None):
    w = windows.get_window(window_id)
    f = fabrics.get_fabric(fabric_id)
    if not w or not f:
        raise HTTPException(404, "not found")
    if w.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty window")
    settings = settings_repo.get_all()
    fullness = float(w.get("fullness") or settings.get("default_fullness", 2.0))
    calc = fabric_meters(w["width"], w["height"], fullness, f["hem_top"], f["hem_bottom"], f["fabric_width"])
    if lining:
        hem = lining_hem if lining_hem is not None else float(settings.get("default_lining_hem") or DEFAULT_LINING_HEM)
        hem = float(hem)
        if hem < 0:
            raise HTTPException(422, "lining hem must be >= 0")
        lining_block = {"enabled": True, "hem": hem, **lining_meters(w["height"], hem, calc["panels"])}
    else:
        lining_block = {"enabled": False}
    result = {**calc, "lining": lining_block}
    run_id = history.insert_run(window_id, fabric_id, result, note) if save else None
    return {"window": w, "fabric": f, "run_id": run_id, **result}
