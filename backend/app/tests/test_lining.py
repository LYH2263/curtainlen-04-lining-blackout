import pytest
from fastapi import HTTPException

from app import seed
from app.engines.curtain_math import lining_meters
from app.repositories import history, settings_repo
from app.services import estimate_service


@pytest.fixture()
def fresh_db(tmp_path, monkeypatch):
    monkeypatch.setattr("app.db.DB_PATH", tmp_path / "t.db")
    seed.init_db()
    yield


def test_lining_engine_negative_hem():
    with pytest.raises(ValueError):
        lining_meters(2.6, 5, -0.1, 0.1)


def test_lining_matches_main_panels(fresh_db):
    r = estimate_service.run_estimate(1, 1, False, "", True, 0.10, 0.20)
    assert r["panels"] == 5
    assert r["meters"] == 14.25
    assert r["lining"]["panels"] == r["panels"]
    assert r["lining"]["cut_height"] == 2.9
    assert r["lining"]["meters"] == 14.5
    assert r["lining"]["hem_top"] == 0.10
    assert r["lining"]["hem_bottom"] == 0.20


def test_lining_off_matches_base(fresh_db):
    r = estimate_service.run_estimate(1, 1, False, "")
    assert r["panels"] == 5
    assert r["meters"] == 14.25
    assert r["lining_enabled"] is False
    assert r["lining"] is None


def test_negative_hem_fails_and_no_history(fresh_db):
    with pytest.raises(HTTPException) as ei:
        estimate_service.run_estimate(1, 1, True, "", True, -0.1, 0.1)
    assert ei.value.status_code == 422
    assert history.list_runs() == []


def test_saved_record_contains_lining(fresh_db):
    r = estimate_service.run_estimate(1, 1, True, "n1", True, 0.10, 0.20)
    assert r["run_id"]
    rows = history.list_runs()
    assert len(rows) == 1
    res = rows[0]["result"]
    assert res["meters"] == 14.25
    assert res["lining_enabled"] is True
    assert res["lining"]["meters"] == 14.5
    assert res["lining"]["hem_top"] == 0.10
    assert res["lining"]["hem_bottom"] == 0.20


def test_settings_default_used_and_old_runs_frozen(fresh_db):
    settings_repo.set_many({"lining_hem_top": "0.5", "lining_hem_bottom": "0.5"})
    r = estimate_service.run_estimate(1, 1, True, "", True)
    assert r["lining"]["cut_height"] == 3.6
    assert r["lining"]["meters"] == 18.0
    settings_repo.set_many({"lining_hem_top": "0.9", "lining_hem_bottom": "0.9"})
    saved = history.list_runs()[0]["result"]
    assert saved["lining"]["hem_top"] == 0.5
    assert saved["lining"]["meters"] == 18.0
    preview = estimate_service.run_estimate(1, 1, False, "", True)
    assert preview["lining"]["cut_height"] == 4.4


def test_fabrics_main_panels(fresh_db):
    items = estimate_service.panels_by_fabric(1)
    by_name = {f["name"]: f["main_panels"] for f in items}
    assert by_name["遮光1.4m"] == 5
    assert by_name["纱帘2.8m"] == 3
    assert by_name["脏数据-零门幅"] is None
