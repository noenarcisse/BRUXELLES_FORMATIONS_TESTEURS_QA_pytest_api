import os

from constants import BASE_URL, TO
from dotenv import load_dotenv
from helpers import getAllEvents, getEventsWithAvailability, login
from pytest import fixture as f
import uuid
from datetime import timedelta, timezone, datetime
import requests

load_dotenv()

@f(scope="session")
def baseurl() : return os.getenv("API_URL", BASE_URL)
@f(scope="session")
def timeout() : return os.getenv("TIMEOUT", TO)


@f 
def all_events() : return getAllEvents()

@f 
def events_with_6_available(baseurl, all_events) : 
    return getEventsWithAvailability(baseurl, all_events, 6)

@f(scope="session")
def auth_header_client(baseurl) :
    token = login(os.getenv("CLIENT_USERNAME"), os.getenv("CLIENT_PASSWORD"), baseurl)
    return {
        "Authorization": f"Bearer {token}"
}

@f(scope="session")
def auth_header_admin(baseurl) :
    token = login(os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD"), baseurl)
    return {
        "Authorization": f"Bearer {token}"
}

@f(scope="session")
def auth_header_orga(baseurl) :
    token = login(os.getenv("ORGA_USERNAME"), os.getenv("ORGA_PASSWORD"), baseurl)
    return {
        "Authorization": f"Bearer {token}"
}

@f
def small_event(baseurl, auth_header_orga) :
    starts_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=30)

    payload = {
        "title" : f"Un event de tests - {uuid.uuid1()}",
        "description" : "non",
        "city" : "Bruxelles",
        "venue" : "Au parc Albert",
        "starts_at" : starts_at.isoformat(),
        "capacity" : 10,
        "status" : "published",
        "cover_color" : "#FF00FF",
        "categories" : [
        ]
    }

    print(f"{baseurl}admin/events")

    res = requests.post(f"{baseurl}admin/events", json=payload, headers=auth_header_orga)
    assert res.status_code == 201, res.text
    event = res.json()

    id = event["id"]
    
    yield event

    payload["status"] = "archived"

    res2 = requests.put(f"{baseurl}admin/events/{id}", json=payload, headers=auth_header_orga) 
    assert res2.status_code == 200, res2.text

    
