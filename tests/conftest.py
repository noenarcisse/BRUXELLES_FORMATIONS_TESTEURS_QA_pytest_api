import os

from constants import BASE_URL, TO
from pytest import fixture as f


@f
def baseurl() : return os.getenv("API_URL", BASE_URL)
@f
def timeout() : return TO