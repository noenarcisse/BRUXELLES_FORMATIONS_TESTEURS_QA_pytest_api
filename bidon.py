a = {
        "id": 0,
        "title": "string",
        "description": "string",
        "city": "string",
        "venue": "string",
        "starts_at": "string",
        "capacity": 0,
        "status": "string",
        "cover_color": "string"
    }

b = {
        "id": 0,
        "title": "string",
        "description": "string",
        "city": "string",
        "venue": "string",
        "starts_at": "string",
        "capacity": 0,
        "status": "string",
        "cover_color": "string"
    }

k = list(a.keys())
k2 = b.keys()

def hasSameKeys(a : dict, b : dict) -> bool :
    keys : list[str] = list(a.keys())
    keys2 : list[str] = list(b.keys())

    for k in keys2 :
        print(k)
        print(keys)
        if not k in keys : return False
        keys.remove(k)

    print(keys)
    print(len(keys))
    return len(keys) == 0 

print(hasSameKeys(a,b))

def truc():
    func1 = lambda m : m
    func2 = lambda m : m.lower()
    func3 = lambda m : m.upper()

    print(func2("TEST"))
    print(func3("test"))

truc()