import os
from operator import itemgetter
from screen import Menu
from api import Api
from db import DB

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
    
    dadata = Api(token, key)
    if dadata.check_validation() == True:
        db.update(token=token, key=key)
        dadata.close()
    else: 
        return


def sign_in(db):
    print("Введите свои данные для подключения к Dadata")
    try:
        token = input("Токен: ")
        key = input("Ключ: ")
        lang = input("Язык (ru/en): ")
    except KeyboardInterrupt:
        return 
    
    dadata = Api(token, key, lang)
    if dadata.check_validation() == True:
        db.insert(token,key,lang)
        dadata.close()
    else: 
        sign_in(db)


def search_coordinates(db):
    os.system('cls')
    token, secret, lang = db.get_data()
    dadata = Api(token, secret, lang)
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
                sublist = api_call(dadata, value)
        else:
            sublist = api_call(dadata, value)

def api_call(dadata, value):
        result=dadata.get_suggest(value)
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


    settings_menu = Menu("Настройки Dadata coordinates",
                    {
                        "Сменить токен и ключ": lambda: change_api_key(db),
                        "Сменить язык": lambda: change_lang(db)
                    })
    

    main_menu = Menu("Dadata coordinates",
                {
                    "Настройки": settings_menu,
                    "Поиск": lambda: search_coordinates(db)
                })
    
    main_menu.run()


if __name__ == "__main__":
    main()
