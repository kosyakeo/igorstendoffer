class Worker:
    def __init__(self, name, surname, rate, days):
        self.name = name
        self.surname = surname
        self.rate = rate
        self.days = days
    def GetSalary(self):
        return self.rate * self.days
worker = Worker("Сергея", "Пенкина", 0, 30)
print(f"ЗП {worker.name} {worker.surname}: {worker.GetSalary()} руб.")