import requests

PORT = 8000
BASE_URL = "http://localhost:"+str(PORT)
TO = 5 # en sec

def test_health_repond_ok() :
    res = requests.get(f"{BASE_URL}/api/health", timeout=TO)

    assert res.status_code == 200, res.text
    assert res.headers["content-type"].startswith("application/json")
    assert res.json()["status"] == "ok"