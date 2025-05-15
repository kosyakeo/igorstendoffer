import sqlite3
conn = sqlite3.connect('drinks.db')
cursor = conn.cursor()
conn.commit()
def add_drink():
    name = input("Название напитка: ")
    strength = float(input("Крепость (%): "))
    quantity = int(input("Количество: "))
    price = float(input("Цена: "))
    cursor.execute("INSERT INTO drinks VALUES (NULL, ?, ?, ?, ?)",
                   (name, strength, quantity, price))
    conn.commit()
    print("Напиток добавлен!")
def show_drinks():
    print("\nСписок напитков:")
    for row in cursor.execute("SELECT * FROM drinks"):
        print(f"{row[0]}. {row[1]} ({row[2]}%), {row[3]} шт., {row[4]} руб.")
def add_cocktail():
    name = input("Название коктейля: ")
    recipe = input("Рецепт (через запятую): ")
    price = float(input("Цена: "))
    cursor.execute("INSERT INTO cocktails VALUES (NULL, ?, ?, ?)",
                   (name, recipe, price))
    conn.commit()
    print("Коктейль добавлен!")
def show_cocktails():
    print("\nСписок коктейлей:")
    for row in cursor.execute("SELECT * FROM cocktails"):
        print(f"{row[0]}. {row[1]} - {row[3]} руб. (Рецепт: {row[2]})")
def sell_drink():
    show_drinks()
    drink_id = int(input("ID напитка: "))
    quantity = int(input("Количество: "))
    cursor.execute("SELECT quantity FROM drinks WHERE id=?", (drink_id,))
    current = cursor.fetchone()[0]
    if current >= quantity:
        cursor.execute("UPDATE drinks SET quantity=? WHERE id=?",
                       (current - quantity, drink_id))
        conn.commit()
        print("Продажа совершена!")
    else:
        print("Недостаточно на складе")
def restock():
    show_drinks()
    drink_id = int(input("ID напитка: "))
    quantity = int(input("Количество для пополнения: "))

    cursor.execute("SELECT quantity FROM drinks WHERE id=?", (drink_id,))
    current = cursor.fetchone()[0]
    cursor.execute("UPDATE drinks SET quantity=? WHERE id=?",
                   (current + quantity, drink_id))
    conn.commit()
    print("Запас пополнен!")
while True:
    print("\n1. Добавить напиток")
    print("2. Показать напитки")
    print("3. Добавить коктейль")
    print("4. Показать коктейли")
    print("5. Продать напиток")
    print("6. Пополнить запас")
    print("0. Выход")
    choice = input("Выберите: ")
    if choice == "1":
        add_drink()
    elif choice == "2":
        show_drinks()
    elif choice == "3":
        add_cocktail()
    elif choice == "4":
        show_cocktails()
    elif choice == "5":
        sell_drink()
    elif choice == "6":
        restock()
    elif choice == "0":
        break
conn.close()