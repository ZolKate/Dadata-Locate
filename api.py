import httpx
from dadata import Dadata
from typing import Tuple
from dataclasses import dataclass
from config import UserConfiguration


BASE_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address"


class APIException(Exception):
    ...

@dataclass
class Suggest:
    address:str
    lat: str
    lon:str 

class SuggestConnect:
    def __init__(self, user: UserConfiguration) -> None:
        self.user_config = user

    def suggest(self, query: str) -> Tuple[Suggest]:
        config = self.user_config.dict()
        try:
            dadata = Dadata(config["token"], config["key"])
            return tuple(
                Suggest(
                    address = x['value'],
                    lat=x['data']['geo_lat'],
                    lon=x['data']['geo_lon']
                ) for x in dadata.suggest(name='address', query=query, language = config["lang"].value, count=10)
            )

        except httpx.HTTPError as e:
            raise APIException(f'Ошибка выполнения запроса: {e.response.status_code}') from e


