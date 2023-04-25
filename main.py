from interface import StateManager, SelectState, FunctionWithInput, FunctionWithoutInput, SuggestState
from config import UserConfiguration, Lang, UrlID
from api import SuggestConnect


if __name__ == "__main__":

    user = UserConfiguration(None, None, Lang.RU)
    
    if user.get_config(UrlID.Dadata.value):
        user.set_config(UrlID.Dadata.value)

    dadata = SuggestConnect(user)

    menu = StateManager(
            SelectState("Меню",
                (
                    SuggestState("Поиск", dadata.suggest),
                    SelectState("Настройки", 
                        [
                            FunctionWithInput("Токен", user.change_token),
                            FunctionWithInput("Ключ", user.change_key),
                            SelectState("Язык", 
                                    [
                                        FunctionWithoutInput("Русский", lambda: user.change_lang(Lang.RU)),
                                        FunctionWithoutInput("Английский", lambda: user.change_lang(Lang.EN))
                                    ]
                            )
                        ]
                    )
                )
        )).run()

    user.set_config(UrlID.Dadata.value)