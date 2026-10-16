# warm up pour reprendre un peu de snek

import requests
import pytest

url = "http://localhost:8000"
res = requests.get(f"{url}/api/events", timeout=5)
events : list[dict] = res.json()

# for e in events :
#     print(e)
# events.sort(key=lambda e : e["id"], reverse=True)
# print(events)

def test_recupTousLesElements() :
    res = requests.get(f"{url}/api/events", timeout=5)
    assert res.status_code == 200, res.text

    events : list[dict] = res.json()
    assert len(events) > 0

@pytest.mark.skip
def test_askip():
    assert False == False