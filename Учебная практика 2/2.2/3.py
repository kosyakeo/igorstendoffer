class Numstorage:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
    def display_numbers(self):
        print(f"Число 1: {self.num1}")
        print(f"Число 2: {self.num2}")
    def change_numbers(self, new_num1, new_num2):
        self.num1 = new_num1
        self.num2 = new_num2
    def sum_numbers(self):
        return self.num1 + self.num2
    def max_number(self):
        return max(self.num1, self.num2)
storage = Numstorage(5, 10)
storage.display_numbers()
storage.change_numbers(15, 20)
storage.display_numbers()
print(f"Сумма чисел: {storage.sum_numbers()}")
print(f"Наибольшее число: {storage.max_number()}")
