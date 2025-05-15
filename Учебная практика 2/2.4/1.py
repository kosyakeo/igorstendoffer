class Student:
    def __init__(self, name, surname, group, grades):
        self.name = name
        self.surname = surname
        self.group = group
        self.grades = grades
    def average(self):
        return sum(self.grades) / len(self.grades)
students = []
def add_student():
    name = input("Имя: ")
    surname = input("Фамилия: ")
    group = input("Группа: ")
    grades = list(map(int, input("4 оценки через пробел: ").split()))
    students.append(Student(name, surname, group, grades))
    print("Добавлен!")
def show_all():
    for i, student in enumerate(students, 1):
        print(f"{i}. {student.surname} {student.name}, {student.group}, средний: {student.average():.1f}")
def show_one():
    num = int(input("Номер студента: ")) - 1
    s = students[num]
    print(f"{s.surname} {s.name}, {s.group}")
    print(f"Оценки: {s.grades}, средний: {s.average():.1f}")
def group_avg():
    group = input("Группа: ")
    group_students = [s for s in students if s.group == group]
    if not group_students:
        print("Нет студентов")
        return
    avg = sum(s.average() for s in group_students) / len(group_students)
    print(f"Средний по группе: {avg:.1f}")
while True:
    print("\n1. Добавить\n2. Все студенты\n3. Один студент\n4. Средний группы\n0. Выход")
    choice = input("Выбор: ")
    if choice == "1":
        add_student()
    elif choice == "2":
        show_all()
    elif choice == "3":
        show_one()
    elif choice == "4":
        group_avg()
    elif choice == "0":
        break