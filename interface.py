import os
from abc import ABC, abstractmethod
from typing import Optional, Callable, List
from api import Suggest

# Интерфейс состояния 
class State(ABC):

    def __init__(self, title:str) -> None:
        self.title = title
        self._prev_state: Optional['State'] = None

    @property
    def prev_state(self)->'StateManager':
        return self._prev_state
    
    @prev_state.setter
    def prev_state(self, state: Optional['State']):
        self._prev_state = state

    @abstractmethod
    def display(self, state_manager: 'StateManager'):
        ...



# Менеджер состояний
class StateManager:
    
    def __init__(self, state: State) -> None:
        self._cur_state = state
    
    @property
    def cur_state(self)->'StateManager':
        return self._cur_state
    
    @cur_state.setter
    def cur_state(self, state: Optional['State']):
        self._cur_state = state

    def run(self):
        while self._cur_state:
            os.system('cls')
            self._cur_state.display(self)


# Состояние подменю
class SelectState(State):
    def __init__(self, title: str, states: List[State]) -> None:
        super().__init__(title)
        self.states = states
    
    def display(self, state_manager: 'StateManager'):
        print(f"----- {self.title} -----")
        for i in range(len(self.states)):
            print(f"{i+1}) {self.states[i].title}")
        
        if self._prev_state:
            print(f"{len(self.states)+1}) Назад")
        else:
            print(f"{len(self.states)+1}) Выйти")

        try:
            choice = int(input(">> "))
        except ValueError:
            print("Такого пункта меню нет")
            return
        except KeyboardInterrupt:
            exit()
        
        if choice == len(self.states)+1:
            state_manager.cur_state = self.prev_state
        else:
            state_manager.cur_state = self.states[choice - 1]
            state_manager.cur_state.prev_state = self


# Функциональное состояние
class FunctionalState(State):
    def __init__(self, title: str, func: Callable[[], None]) -> None:
        super().__init__(title)
        self.action = func

    def display(self, state_manager: StateManager):
        ...

# Функциональное состояние без ввода
class FunctionWithoutInput(FunctionalState):
    def display(self, state_manager: 'StateManager'):
        print(f"----- {self.title} -----\n")
        print(f"{state_manager.cur_state.prev_state.title} был изменен")
        self.action()
        os.system('pause')
        state_manager.cur_state = self.prev_state

# Функциональное состояние с вводом
class FunctionWithInput(FunctionalState):
    def display(self, state_manager: 'StateManager'):
        print(f"----- {self.title} -----\n")
        try:
            query = input(">> ")
        except KeyboardInterrupt:
            exit()
        os.system('pause')
        self.action(query)
        state_manager.cur_state = self.prev_state

class SuggestState(FunctionalState):
    def __init__(self, title: str, func: Callable[[], None]) -> None:
        super().__init__(title, func)

    def display(self, state_manager: StateManager):
        print(f"----- {self.title} -----\n")
        try:
            query = input(">> ")
            res = self.action(query)
            if len(res) > 0:
                ctn = SelectState(
                    "Варианты адреса\n",
                    [
                      FunctionWithoutInput(
                            x.address, 
                            lambda : print(f"Кординаты места: {x.lat} {x.lon}")
                        ) for x in res
                    ]
                )
                ctn.prev_state = self
                return ctn.display(state_manager)
            else:
                print("Ничего не найдено")
        except KeyboardInterrupt:
            exit()
        
