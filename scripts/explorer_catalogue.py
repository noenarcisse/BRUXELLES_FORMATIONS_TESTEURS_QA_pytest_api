"""Point de départ : un script d'exploration « façon J2 ».

Il affiche des choses. Il ne dit jamais si c'est correct.
Le J4 commence ici : on le transforme en tests.
"""
import requests

BASE_URL = "http://localhost:8000"

# response = requests.get(f"{BASE_URL}/api/events", timeout=5)
# print(response.status_code)
# print(response.headers.get("content-type"))

# for event in response.json():
#     print(event["id"], event["title"], "-", event["city"], "-", event["status"])

# detail = requests.get(f"{BASE_URL}/api/events/{response.json()[0]['id']}", timeout=5)
# print(detail.status_code)
# print(detail.json())

# query_params = {
#     "city": "Gand"
# }

# response_city = requests.get(f"{BASE_URL}/api/events", params=query_params)

response = requests.get(f"{BASE_URL}/api/events/abc", timeout=5)
print(response.status_code)
print(response.text)
