import httpx
from dadata import Dadata

HTTP_ERROR = {
        400: "Некорректный запрос (невалидный JSON или XML)",
        401: "В запросе отсутствует API-ключ",
        403: "В запросе указан несуществующий API-ключ \n Или исчерпан дневной лимит по количеству запросов \n Или не подтверждена почта",
        413: "Слишком большая длина запроса или слишком много условий",
        429: "Слишком много запросов в секунду или новых соединений в минуту"
}

class Api:
    def __init__(self, token, secret, lang="ru"):
        self.__token = token
        self.__secret = secret
        self.lang = lang
        self.dadata = Dadata(self.__token, self.__secret)
    
    def check_validation(self):
        try:
            return bool(self.get_suggest("Москва", 1))
        except httpx.HTTPError as exc:
            print(HTTP_ERROR[exc.response.status_code])
            return
    
    def get_suggest(self, value, count = 10):
        return self.dadata.suggest(name='address', query=value, language = self.lang, count=count)

    def close(self):
        self.dadata.close()