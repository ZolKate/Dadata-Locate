import os
import httpx
from dadata import Dadata
from operator import itemgetter
from screen import Menu
from db import DB

HTTP_ERROR = {
        401: "В запросе отсутствует API-ключ",
        403: "В запросе указан несуществующий API-ключ или исчерпан дневной лимит по количеству запросов",
        413: "Слишком большая длина запроса или слишком много условий",
        429: "Слишком много запросов в секунду или новых соединений в минуту"
}

def change_lang(db):
    os.system('cls')
    lang = input("Язык (ru/en): ")
    if lang == "ru" or lang == "en":
        db.update(lang = lang)
    else:
        print("Язык должен быть ru либо en")

def change_api_key(db):
    os.system('cls')
    try:
        token = input("Токен: ")
        key = input("Ключ: ")
    except KeyboardInterrupt:
        return
    db.update(token=token, key=key)

def sign_in(db):
    print("Введите свои данные для подключения к Dadata")
    try:
        token = input("Токен: ")
        key = input("Ключ: ")
        lang = input("Язык (ru/en): ")
    except KeyboardInterrupt:
        return 
    db.insert(token,key,lang)


def search_coordinates(dadata, lang):
    os.system('cls')
    print("Напишите адрес, который вам нужен...")
    sublist = []
    while True: 
        try:
            value = input(">>")
        except KeyboardInterrupt:
            break 
        
        if bool(sublist):
            if value.isdigit() and int(value) in range(1,len(sublist)+1):
                address, coord = itemgetter('value', 'data')(sublist[int(value)-1])
                print("Адрес: {} Широта: {} Долгота: {}".format(address, coord["geo_lat"], coord["geo_lon"]))
                break
            else:
                sublist = api_call(dadata, lang, value)
        else:
            sublist = api_call(dadata, lang, value)

def api_call(dadata, lang, value): 
        try:
            result = dadata.suggest(name='address', query=value, language = lang, count=2)
        except httpx.HTTPStatusError as exc:
            print(HTTP_ERROR[exc.response.status_code])
            return
        data = []
        i=1
        for item in result:
            print("{}) {}".format(str(i), str(item["value"])))
            data.append(item)
            i+=1

        print("Выберите номер нужного варианта или введите запрос заново...")
        return data


def main():
    os.system('cls')
    db = DB('client.db')
    db.create_table()

    if not db.has_rows():
        sign_in(db)

    token, secret, lang = db.get_data()
    dadata = Dadata(token, secret)

    settings_menu = Menu("Настройки Dadata coordinates",
                    {
                        "Сменить токен и ключ": lambda: change_api_key(db),
                        "Сменить язык": lambda: change_lang(db)
                    })
    

    main_menu = Menu("Dadata coordinates",
                {
                    "Настройки": settings_menu,
                    "Поиск": lambda: search_coordinates(dadata, lang)
                })
    
    main_menu.run()
    


if __name__ == "__main__":
    main()
