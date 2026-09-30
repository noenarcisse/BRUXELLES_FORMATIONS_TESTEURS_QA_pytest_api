import requests
from constants import BASE_URL, TO


def test_health_repond_ok(baseurl, timeout) :
    res = requests.get(f"{baseurl}health", timeout=timeout)

    assert res.status_code == 200, res.text
    assert res.headers["content-type"].startswith("application/json")
    assert res.json()["status"] == "ok"