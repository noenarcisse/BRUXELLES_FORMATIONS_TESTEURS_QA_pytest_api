import os

from constants import BASE_URL, TO
from dotenv import load_dotenv
from helpers import getAllEvents, getEventsWithAvailability, login
from pytest import fixture as f

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
def auth_orga_admin(baseurl) :
    token = login(os.getenv("ORGA_USERNAME"), os.getenv("ORGA_PASSWORD"), baseurl)
    return {
        "Authorization": f"Bearer {token}"
}