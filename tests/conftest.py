import os

from constants import BASE_URL, TO
from dotenv import load_dotenv
from pytest import fixture as f

load_dotenv()

@f(scope="session")
def baseurl() : return os.getenv("API_URL", BASE_URL)
@f(scope="session")
def timeout() : return os.getenv("TIMEOUT", TO)