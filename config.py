from typing import Optional
from dataclasses import dataclass, asdict
from enum import Enum
from db import SqliteDB

class Lang(Enum):
    RU = "ru"
    EN = "en"

class UrlID(Enum):
    Dadata = 1

@dataclass
class User:
    token: Optional[str]
    key: Optional[str]
    lang: Lang.RU


class UserConfiguration(User):

    db = SqliteDB("config.db")

    def change_lang(self, lang: Lang):
        self.lang = lang
    
    def change_token(self, token: str):
        self.token = token
    
    def change_key(self, key:str):
        self.key = key

    def get_config(self, ID):
        if self.db.select(ID):
            self.token, self.key, self.lang = self.db.select(ID)
            self.lang = Lang(self.lang)

    def set_config(self, ID):
        self.db.update(ID, self.token, self.key, self.lang.value)

    def dict(self):
        return  {k: v for k,v in asdict(self).items()}

