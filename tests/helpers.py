import requests
import constants

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