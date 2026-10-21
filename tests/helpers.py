import constants
import requests


def hasSameKeys(a : dict, b : dict) -> bool :
    """
        Check if two dicts have the exact same keys. No more, no less.
    """
    keys : list[str] = list(a.keys())
    keys2 : list[str] = b.keys()

    for k in keys2 :
        if not k in keys : return False
        keys.remove(k)
    return len(keys) == 0 


def getAllEvents() -> list[dict] : 
    """
        Get events from EventFlow.
    """
    res = requests.get(constants.BASE_URL+"events", timeout=constants.TO)
    events = res.json()
    assert len(events) > 0, "Events list is empty, test aborted"
    return events

def login(email : str, password : str, baseurl : str) -> str :
    payload = {
        "username" : email,
        "password" : password
    }
    res = requests.post(f"{baseurl}auth/token", data=payload)
    assert res.status_code == 200, res.text

    jason : dict = res.json()
    token : str = jason.get("access_token")
    assert  token != None

    return token

def getEventsWithAvailability(baseurl : str, events : list[dict], available : int = 1) -> list[dict] : 
    """
        Get events from EventFlow with a specific number of available seats.
    """
    eventids = [e["id"] for e in events]
    eventswith6 = []

    for id in eventids :
        res = requests.get(f"{baseurl}events/{id}", timeout=5)
        assert res.status_code == 20, res.text
        event = res.json()

        if event["status"] != "pusblished" : continue
        if event["available"] < available : continue
        if len(event["categories"]) <= 0 : continue

        for c in event["categories"] :
            if c["availaible"] >= available :
                eventswith6.append(event)
            
    return eventswith6