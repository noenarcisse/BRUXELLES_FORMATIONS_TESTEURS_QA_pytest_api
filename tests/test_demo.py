# warm up pour reprendre un peu de snek

import json
from pathlib import Path

import pytest
import requests
from jsonschema import ValidationError, validate

PROJECT_ROOT = Path(__file__).resolve().parent.parent

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


def test_schema() :

    schema = {
        "type" : "object",
        "required" : ["id", "title"],
        "properties" : {
            "id" : {"type" : "integer", "minimum" : 0},
            "title" : {"type" : "string"}
        }
    }

    obj = {
        "id" : 42,
        "title" : "Harry Potté"
    }

    validate(obj, schema=schema)


def test_schema_events() : 
    # test cassé : 
    obj = {
            "id" : 42,
            "title" : "Harry Potté"
        }

    # tets qui marche
    res = requests.get(f"{url}/api/events/5")
    obj = res.json()
    
    with open(f"{PROJECT_ROOT}/tests/schemas/eventDetail.json") as file :
        eventSchema = json.load(file)
        validate(obj, eventSchema)




def test_schema_events_casse() : 
    # test cassé : 
    obj = {
            "id" : 42,
            "title" : "Harry Potté"
        }
    
    with open(f"{PROJECT_ROOT}/tests/schemas/eventDetail.json") as file :
        eventSchema = json.load(file)

        with pytest.raises(ValidationError) :
            validate(obj, eventSchema)

def test_connecteMooooooi(auth_header_client, baseurl) : 
    res = requests.get(f"{baseurl}auth/me", headers=auth_header_client)
    content = res.json()

    print(content)

    assert "full_name" in content
    assert content["full_name"] == "Camille Client"
