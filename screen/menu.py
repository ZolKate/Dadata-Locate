
class Menu:
    def __init__(self, title: str, menu_items: dict):
        self.title = title
        self.menu_items = menu_items
        self.nested = False

    def display(self):
        print("", end='\n')
        print(self.title)
        print("", end='\n')
        print("Выберите действие...")
        i = 1
        for key in self.menu_items:
            print("{}) {}".format(str(i), str(key)))
            i += 1
        print("{}) {}".format(str(i), "Назад" if self.nested else "Выход"))

    def run(self):
        while True:
            self.display()

            try:
                arg = int(input(">>"))
            except (TypeError, ValueError):
                print("Error: Неверный ввод")
                continue
            except KeyboardInterrupt:
                break

            if arg not in range(1, len(self.menu_items)+2):
                print("Error: Нет такого пункта меню")
                continue

            if arg == len(self.menu_items) + 1:
                break
            
            item = list(self.menu_items.values())[arg-1]
            try:
                if isinstance(item, Menu):
                    item.nested = True
                    item.run()
                    item.nested = False
                else:
                    item()
            except Exception:
                pass