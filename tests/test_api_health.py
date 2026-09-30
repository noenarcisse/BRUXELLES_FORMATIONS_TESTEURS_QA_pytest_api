import requests
from constants import BASE_URL, TO


def test_health_repond_ok() :
    res = requests.get(f"{BASE_URL}health", timeout=TO)

    assert res.status_code == 200, res.text
    assert res.headers["content-type"].startswith("application/json")
    assert res.json()["status"] == "ok"