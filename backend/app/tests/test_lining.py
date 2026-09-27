import pytest
from fastapi import HTTPException

from app import seed
from app.db import connect
from app.engines.curtain_math import fabric_meters, lining_meters
from app.repositories import history, settings_repo
from app.services import estimate_service

seed.init_db()


def run_count():
    c = connect()
    try:
        return c.execute("SELECT COUNT(*) c FROM calc_runs").fetchone()["c"]
    finally:
        c.close()


def test_lining_math_uses_main_panels():
    main = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4)
    r = lining_meters(2.6, 0.1, main["panels"])
    assert r["panels"] == 5
    assert r["cut_height"] == 2.8
    assert r["meters"] == 14.0


def test_lining_negative_hem_raises():
    with pytest.raises(ValueError):
        lining_meters(2.6, -0.1, 5)


def test_lining_off_matches_pre_change_numbers():
    r = estimate_service.run_estimate(1, 1, False, "", lining=False)
    assert r["panels"] == 5
    assert r["meters"] == 14.25
    assert r["lining"] == {"enabled": False}


def test_lining_on_uses_settings_default_hem():
    r = estimate_service.run_estimate(1, 1, False, "", lining=True)
    assert r["meters"] == 14.25
    assert r["lining"]["enabled"] is True
    assert r["lining"]["hem"] == 0.1
    assert r["lining"]["panels"] == 5
    assert r["lining"]["cut_height"] == 2.8
    assert r["lining"]["meters"] == 14.0


def test_save_stores_main_and_lining_in_one_record():
    r = estimate_service.run_estimate(1, 1, True, "", lining=True, lining_hem=0.2)
    assert r["run_id"]
    row = next(x for x in history.list_runs(100) if x["id"] == r["run_id"])
    assert row["result"]["meters"] == 14.25
    assert row["result"]["lining"]["enabled"] is True
    assert row["result"]["lining"]["hem"] == 0.2
    assert row["result"]["lining"]["panels"] == 5
    assert row["result"]["lining"]["meters"] == 15.0


def test_negative_hem_fails_whole_order_without_history_row():
    before = run_count()
    with pytest.raises(HTTPException) as e:
        estimate_service.run_estimate(1, 1, True, "", lining=True, lining_hem=-0.1)
    assert e.value.status_code == 422
    assert run_count() == before


def test_settings_change_does_not_rewrite_saved_runs():
    r = estimate_service.run_estimate(1, 1, True, "", lining=True, lining_hem=0.2)
    settings_repo.set_many({"default_lining_hem": "0.5"})
    try:
        row = next(x for x in history.list_runs(100) if x["id"] == r["run_id"])
        assert row["result"]["lining"]["hem"] == 0.2
        assert row["result"]["lining"]["meters"] == 15.0
    finally:
        settings_repo.set_many({"default_lining_hem": "0.1"})
