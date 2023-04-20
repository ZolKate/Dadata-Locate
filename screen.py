import os
from abc import ABC, abstractmethod
from typing import Dict, Optional


class State(ABC):

    @property
    def context(self)->'Context':
        return self._context
    
    @context.setter
    def context(self, context: 'Context'):
        self._context = context
        
    @abstractmethod
    def next_state(self):
        ...
    
    @abstractmethod
    def prev_state(self):
        ...

    @abstractmethod
    def display(self):
        ...


class Context:
    _cur_state = None
    _prev_state = None

    def __init__(self, state: State) :
        self.setState(state)

    def setState(self, state: State):
        self._cur_state = state
        self._cur_state.context=self
    
    def display(self):
        os.system('cls')
        self._cur_state.display()


class SelectState(State):
    states: Dict[int, State] = {}
    def __init__(self, title:str, substate: Optional[State]):
        self.title = title
        self.items = substate

    def format_action(self):
        for i in range(len(self.items)):
            self.states[i] = self.items[i]
        return self.states

    def next_state(self, state:State)->State:
        self.context.setState(state)
        return self.context.display()

    def prev_state(self):
        ...
    
    def display(self):
        print(f"----- {self.title} -----")
        for item in self.format_action().items():
            print(f"{item[0]+1}) {item[1].title}")
        try:
            print(f"Chose action")
            choice = int(input(">>"))
        except ValueError:
            return 
        self.next_state(self.states[choice-1])

class FunctionalState(State):
    def __init__(self, title:str) -> None:
        self.title = title

    def prev_state(self):
        ...

    def next_state(self):
        ...
    
    def display(self):
        print(f"{self.title}")

def print_something():
    print('okay')

def print_something1():
    print('okay1')

if __name__ == "__main__":
    
    menu = Context(SelectState(
            "Меню",
            (
                FunctionalState("Поиск"),
                SelectState("Настройки", (
                    FunctionalState("Токен"),
                    FunctionalState("Ключ"),
                    FunctionalState("Язык"),
                    FunctionalState("Назад")
                )),
                FunctionalState("Выйти")
            ),
        )).display()