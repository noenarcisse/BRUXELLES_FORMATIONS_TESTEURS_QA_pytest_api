import json
from pathlib import Path

import pytest
import requests
from jsonschema import ValidationError, validate

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def schemaEvents() : 
    with open(f"{PROJECT_ROOT}/tests/schemas/eventOut.json") as file :
        event_schema = json.load(file)
        return {
            "type" : "array",
            "items" : event_schema
        }
    

def test_json_events(baseurl) :
    events_schema = schemaEvents()

    res = requests.get(f"{baseurl}events")
    obj = res.json()

    validate(obj, events_schema)

def test_schemaQuiRate(baseurl) :
    res = requests.get(f"{baseurl}events/1")
    obj = res.json()
    del obj["id"]

    with open(f"{PROJECT_ROOT}/tests/schemas/eventDetail.json") as f :
        eventSchema = json.load(f)

        with pytest.raises(ValidationError) :
            validate(obj, eventSchema)
