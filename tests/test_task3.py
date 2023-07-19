import requests


def test_post_flowers_invalid():
    data = {"name": ""}
    response = requests.post("http://127.0.0.1:8000/flowers/add?", data=data)
    assert response.status_code == 422


def test_post_flowers_valid():
    data = {"name": "Розы", "count": 1, "cost": 5}

    response = requests.post(
        "http://127.0.0.1:8000/flowers/add?", data=data, allow_redirects=False
    )
    assert response.status_code == 303
    assert "/flowers" in response.headers.get("location")


def test_get_flowers():
    response = requests.get("http://127.0.0.1:8000/shop?")
    assert "Розы" in response.text
    assert "5" in response.text
