import requests


class InfoLoader:
    """
    Singleton class to load and store coordinates
    """

    __instance = None

    def __init__(self):
        if type(self).__instance:
            raise Exception("Singleton class can have only one instance")
        self._city_cache = {}
        type(self).__instance = self

    @classmethod
    def get_instance(cls):
        return cls.__instance or InfoLoader()

    def get(self, city):

        if city in self._city_cache:
            return self._city_cache[city]

        url = f"https://htmlweb.ru/geo/api.php?city_name={city}&json"
        print("sending request...")

        try:
            data = requests.get(url).json()
        except requests.exceptions.ConnectionError:
            return {
                "latitude": None,
                "longitude": None
            }

        coordinate = {}
        try:
            coordinate["latitude"] = data["0"]["latitude"]
            coordinate["longitude"] = data["0"]["longitude"]
        except KeyError:
            return {
                "latitude": None,
                "longitude": None
            }

        self._city_cache[city] = coordinate
        return coordinate


def city_info(city):
    loader = InfoLoader.get_instance()
    return loader.get(city)
