from io import BytesIO
import requests
from PIL import Image


def get_coords_and_address(name):
    toponym_to_find = name

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]

    address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]

    try:
        toponym_index = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
    except KeyError:
        toponym_index = ""

    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return toponym_longitude, toponym_lattitude, address, toponym_index


def get_address_by_coords(coords):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": f"{coords[1]},{coords[0]}",
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
    toponym_index = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
    return address, toponym_index


def load_map(toponym_longitude, toponym_lattitude, spn, mode='map'):
    org_point = "{0},{1}".format(toponym_longitude, toponym_lattitude)
    map_params = {
        "ll": ",".join([str(toponym_longitude), str(toponym_lattitude)]),
        # "spn": ",".join([delta, delta]),
        "z": spn,
        "l": mode,
        "pt": f"{org_point},pm2dgl"
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    return response.content
