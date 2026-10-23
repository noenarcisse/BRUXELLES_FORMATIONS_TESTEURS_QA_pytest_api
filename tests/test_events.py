import helpers
import pytest
import requests
from constants import BASE_URL, TO

d : dict = {
    "a": 1,
    "b": "salut"  
}


def test_events_struct_ok(baseurl) :
    res = requests.get(f"{baseurl}events", timeout=TO)

    eventStruct = {
        "id"         : 0,
        "title"      : "string",
        "description": "string",
        "city"       : "string",
        "venue"      : "string",
        "starts_at"  : "string",
        "capacity"   : 0,
        "status"     : "string",
        "cover_color": "string"
    }

    assert res.status_code == 200, "Allo ?"
    assert res.headers["content-type"].startswith("application/json")

    content = res.json()

    assert len(content) > 0, "C'est vide ?"
    assert helpers.hasSameKeys(eventStruct, content[0]) == True

def test_events_not_empty_list() :
    res = requests.get(BASE_URL+"events", timeout=TO)

    assert res.status_code == 200
    assert len(res.json()) > 0, "Liste vide"

@pytest.mark.parametrize(
        "id, expected_code",
        [
            ("", 200),
            ("-1", 404),
            ("a", 422),
            ("99999", 404)
        ],
        ids=
            [
                "str vide", 
                "moinsun -> 404", 
                "events/a -> 422", 
                "events/9999 -> 404"
            ]               
)
def test_events_badrequests(id, expected_code) :
    res = requests.get(BASE_URL+"events/"+id, timeout=TO)
    assert res.status_code == expected_code

def test_events_ids_are_unique() :
    """
    Test que les IDs des events n'apparaissent jamais en doublon
    """
    res = requests.get(BASE_URL+"events/", timeout=TO)
    assert res.status_code == 200

    events = res.json()
    ids = list(map(lambda e : e["id"], events))
    ids_set = set(ids)
    assert len(ids) == len(ids_set)

def test_events_capacity_natural() :
    res = requests.get(BASE_URL+"events/", timeout=TO)
    assert res.status_code == 200

    events = res.json()
    errs = [e for e in events if e["capacity"] < 0]
    assert len(errs) == 0


# events/{id}

@pytest.mark.parametrize("id, code, exp",
    [
        (1,200, 1),
        (99999, 404, "Event not found"),
        (0,     404, "Event not found"),
        ("a",   422, "integer"),
        ("1.5", 422, "integer")
    ]
)
def test_event_by_id(id, code, exp) :
    res = requests.get(f"{BASE_URL}events/{id}", timeout=TO)
    assert res.status_code == code
    event = res.json()

    if code == 200 :
        assert event["id"] == exp
    if code == 404 :
        assert event["detail"] == exp , res.text
    if code == 422 :
        assert "integer" in event["detail"][0]["msg"]

# cities param
def test_events_city_ok() :
    res = requests.get(BASE_URL+"events?city=Bruxelles")
    assert res.status_code == 200

    events = res.json()
    assert len(res.json()) > 0
    for e in events :
        assert e["city"] == "Bruxelles"

@pytest.mark.parametrize(
    "city",
    [
        ("Bruxelle"),
        ("bruxelles"),
        ("Paris"),
        ("1")
    ],
    ids = [
        "Bruxelles sans S",
        "Bruxelles mais en minuscules",
        "Bruxelles mais en France",
        "Un"
    ]
)
def test_events_city_notfound(city) :
    res = requests.get(BASE_URL+"events?city="+city)
    assert res.status_code == 200
    assert len(res.json()) == 0


# Q param

def test_events_q_ok() :
    res = requests.get(BASE_URL+"events?q=qa")

    assert res.status_code == 200
    assert len(res.json()) > 0

    events = res.json()
    for e in events :
        title : str = e["title"]
        assert "qa" in title.lower()

def test_q_casesensitive():
    res = requests.get(BASE_URL+"events?q=QA")
    assert res.status_code == 200
    events = res.json() 

    for e in events : 
        assert "QA" in e["title"].upper()


def test_events_empty_q() :
    res = requests.get(BASE_URL+"events?q=")
    assert res.status_code == 200
    assert len(res.json()) != 0

def test_events_q_nofin() :
    res = requests.get(BASE_URL+"events?q=darksouls4")

    assert res.status_code == 200
    assert len(res.json()) == 0




# published only

def test_events_all_published() :
    res = requests.get(BASE_URL+"events", timeout=TO)

    assert res.status_code == 200
    events = res.json()
    notpub = [e for e in events if e["status"] != "published"]
    assert len(notpub) == 0


def test_events_q_found() :
    res = requests.get(BASE_URL+"events", timeout=TO)
    events = res.json()

    assert len(events) > 0, "NOOOOOOON aucun event test annulé"

    w = events[0]["title"].split()[0]

    res2 = requests.get(BASE_URL+"events?q="+w, timeout=TO)
    found = res2.json()
    
    assert events[0]["id"] in [e["id"] for e in found]