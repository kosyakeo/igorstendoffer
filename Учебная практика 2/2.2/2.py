class Train:
    def __init__(self, destination, train_number, departure_time):
        self.destination = destination
        self.train_number = train_number
        self.departure_time = departure_time
    def display_info(self):
        print(f"Пункт назначения: {self.destination}")
        print(f"Номер поезда: {self.train_number}")
        print(f"Время отправления: {self.departure_time}")
train1 = Train("Красноярск", "124К", "14:00 по местному времени")
train2 = Train("Санкт-Петербург", "052С", "14:30 по местному времени")
trains = [train1, train2]
train_number_to_find = input("Введите номер поезда: ")
for train in trains:
    if train.train_number == train_number_to_find:
        train.display_info()
        break
else:
    print("Поезд с таким номером не найден.")
