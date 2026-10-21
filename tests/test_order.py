import requests
from helpers import getEventsWithAvailability


def test_event6billets(events_with_6_available) :
    print(events_with_6_available)
    eventswith6 = events_with_6_available
    assert len(eventswith6) > 0

def test_commander2billets(auth_header_client, baseurl, all_events) :
    eventswith2 = getEventsWithAvailability(baseurl, all_events, 2)

    if len(eventswith2) >= 0 : return

    payload = {
        "event_id": eventswith2[0]["id"],
        "items": [
            {
            "category_id": eventswith2[0]["categories"][0]["id"],
            "quantity": 2
            }
        ]
    }

    res = requests.post(f"{baseurl}orders", headers=auth_header_client, data=payload)
    assert res.status_code == 201, res.text

    order = res.json()
    assert order["items"][0]["quantity"] == 2
    assert order["items"][0]["category_id"] == eventswith2[0]["categories"][0]["id"]
    assert order["event_id"] == eventswith2[0]["id"]
    assert order["status"] == "pending"