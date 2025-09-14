API_KEY = "StantechAI"

def test_create_and_get_item(client):
    payload = {"title": "Test Item", "description": "desc", "price": 9.99}
    headers = {"x-api-key": API_KEY}

    # create
    r = client.post("/items/", json=payload, headers=headers)
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == payload["title"]

    # get list
    r2 = client.get("/items/?limit=10&offset=0")
    assert r2.status_code == 200
    assert any(x["title"] == payload["title"] for x in r2.json())

    # get single
    item_id = data["id"]
    r3 = client.get(f"/items/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["id"] == item_id
