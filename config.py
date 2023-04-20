from typing import Optional
from dataclasses import dataclass, asdict
from enum import Enum

class Lang(Enum):
    RU = "ru"
    EN = "en"

@dataclass
class User:
    token: Optional[str]
    key: Optional[str]
    lang: Lang.RU
    
    def set_user(self, config: dict):
        for k,v in asdict(self).items():
            if v is None:
                v = config[k]

    def get_user(self):
        return self

if __name__ == "__main__":
    user = User(
        "dsfweag",
        "sdaf",
        Lang.EN
    )
    user.set_user({})

