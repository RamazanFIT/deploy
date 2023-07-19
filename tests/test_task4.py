import requests


def test_cart():
    session = requests.session()

    data = {"id": 1}
    response = session.post("http://127.0.0.1:8000/shop?", data=data)
    response = session.get("http://127.0.0.1:8000/shop?", data=data)

    assert "1" in response.text
