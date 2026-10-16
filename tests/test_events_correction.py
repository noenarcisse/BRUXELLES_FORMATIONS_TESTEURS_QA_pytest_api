import pytest
import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 5

def test_event_published_only():
    response = requests.get(f"{BASE_URL}/api/events", timeout=TIMEOUT)
    assert response.status_code == 200, response.text

    events = response.json()

    for e in events:
        assert e["status"] == "published"

def test_event_list_not_empty():
    response = requests.get(f"{BASE_URL}/api/events", timeout=TIMEOUT)
    assert response.status_code == 200, response.text
    events = response.json()
    # Verifie si la lsite est vide
    assert len(events) > 0, "Liste vide"

def test_event_structure_ok():
    response = requests.get(f"{BASE_URL}/api/events", timeout=TIMEOUT)
    assert response.status_code == 200, response.text
    events = response.json()
    for e in events:
        assert "id" in e
        assert type(e["id"]) == int
        assert "title" in e
        assert type(e["title"]) == str
        assert "description" in e
        assert type(e["description"]) == str
        assert "city" in e
        assert type(e["city"]) == str
        assert "venue" in e
        assert type(e["venue"]) == str
        assert "starts_at" in e
        assert type(e["starts_at"]) == str
        assert "capacity" in e
        assert type(e["capacity"]) == int
        assert "status" in e
        assert type(e["status"]) == str
        assert "cover_color" in e
        assert type(e["cover_color"]) == str


# TEST C1 + C2 — un seul scénario : « un mot du titre retrouve l'event, quelle que soit la casse ».
# Ce qui change d'un cas à l'autre, ce n'est pas une valeur, c'est une TRANSFORMATION du mot.
# En Python, une fonction est une valeur comme une autre : on peut donc la mettre dans la liste.
# PyTest lance le test 3 fois, en passant à chaque fois UNE de ces fonctions dans `transformation`.
@pytest.mark.parametrize("transformation", [
    (lambda m: m),   # fonction « identité » : renvoie le mot tel quel        -> "Festival" reste "Festival"
    (str.upper),     # méthode des chaînes, utilisée comme fonction :           str.upper("Festival") -> "FESTIVAL"
    (str.lower)      # pas de parenthèses : on passe la fonction, on ne l'appelle pas encore
], ids=["CAS NORMAL", "CAS MAJUSCULE", "CAS MINUSCULE"])  # noms lisibles dans le rapport (pytest -v),
                                                         # sinon PyTest afficherait <function <lambda> at 0x...>
def test_param_q_trouve_event(transformation):
    # 1) On lit le catalogue pour y choisir un event réel (on ne suppose pas qu'un titre existe).
    response = requests.get(f"{BASE_URL}/api/events", timeout=TIMEOUT)
    events = response.json()

    # Précondition : sans event, le test n'a rien à vérifier. Message clair plutôt qu'un IndexError.
    assert len(events) > 0, "Test impossible, aucun event sur lequel tester"
    mot = events[0]["title"].split()[0]  # premier mot du titre du premier event (ex. "Festival")

    # 2) C'est ICI qu'on appelle la fonction reçue en paramètre : transformation(mot).
    #    Selon le cas, ça donne "Festival", "FESTIVAL" ou "festival".
    params = {
        'q': transformation(mot)
    }

    # requests construit l'URL pour nous : /api/events?q=FESTIVAL
    detail = requests.get(f"{BASE_URL}/api/events", params=params, timeout=TIMEOUT).json()

    # 3) L'event d'origine doit faire partie des résultats (il peut y en avoir d'autres).
    #    [e["id"] for e in detail] = la liste des ids trouvés (compréhension de liste).
    assert events[0]["id"] in [e["id"] for e in detail]

    # Version longue équivalente de la compréhension de liste ci-dessus :
    # idList = []
    # for d in detail:
    #     idList.append(d["id"])

    # assert events[0]["id"] in idList
