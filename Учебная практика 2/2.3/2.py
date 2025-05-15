class Worker:
    def __init__(self, name, surname, rate, days):
        self.__name = name
        self.__surname = surname
        self.__rate = rate
        self.__days = days
    def name(self):
        return self.__name
    def surname(self):
        return self.__surname
    def rate(self):
        return self.__rate
    def days(self):
        return self.__days
    def GetSalary(self):
        return self.__rate * self.__days
worker = Worker("Сергей", "Пенкин", 0, 365)
print(f"Имя: {worker.name()}")
print(f"Фамилия: {worker.surname()}")
print(f"Ставка: {worker.rate()} руб./день")
print(f"Отработано дней: {worker.days()}")
print(f"Зарплата: {worker.GetSalary()} руб.")