import requests

from app.models import User


def check_rights_and_noneless(user, id_, item):
    return (
        user.is_authenticated and
        user.id in (id_, 1) and
        item is not None
    )


def check_users_exists(users_ids):
    return all(User.query.get(user_id) is not None for user_id in users_ids)


def get_city_image(city):
    response = requests.get(
        "http://geocode-maps.yandex.ru/1.x/?",
        params={
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": city,
            "format": "json",
    }).json()

    coords = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]["Point"]["pos"]
    coords = [float(l) for l in coords.split()]

    response = requests.get(
        "https://static-maps.yandex.ru/1.x/?",
        params={
            "l": "map",
            "ll": "{},{}".format(*coords),
            "size": "600,450",
            "z": 10,
    })
    assert response.status_code == 200
    return response.content
