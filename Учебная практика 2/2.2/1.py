class Student:
    def __init__(self, surname, birth_date, group_number, grades):
        self.surname = surname
        self.birth_date = birth_date
        self.group_number = group_number
        self.grades = grades
    def change_surname(self, new_surname):
        self.surname = new_surname
    def change_birth_date(self, new_birth_date):
        self.birth_date = new_birth_date
    def change_group_number(self, new_group_number):
        self.group_number = new_group_number
    def display_info(self):
        print(f"Фамилия: {self.surname}")
        print(f"Дата рождения: {self.birth_date}")
        print(f"Номер группы: {self.group_number}")
        print(f"Успеваемость: {', '.join(map(str, self.grades))}")
student = Student("Бравлов", "01.01.2005", "142", [4, 5, 5, 4, 5])
student.display_info()
#шоб сменить данные студа
student.change_surname("Стандоффов")
student.change_birth_date("04.04.2004")
student.change_group_number("101")
#шоб вывести новую инф
student.display_info()