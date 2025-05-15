import sqlite3, psutil, datetime, time
conn = sqlite3.connect('monitor.db')
conn.execute('CREATE TABLE IF NOT EXISTS stats(time TEXT, cpu REAL, mem REAL, disk REAL)')
def get_stats():
    return (
        datetime.datetime.now().strftime("%H:%M:%S"),
        psutil.cpu_percent(),
        psutil.virtual_memory().percent,
        psutil.disk_usage('/').percent
    )
def save_stats():
    conn.execute("INSERT INTO stats VALUES(?, ?, ?, ?)", get_stats())
    conn.commit()
def show_stats():
    print("\n1. Текущие показатели\n2. История\n3. Автомониторинг\n0. Выход")
    choice = input("Выберите: ")
    if choice == "1":
        time, cpu, mem, disk = get_stats()
        print(f"CPU: {cpu}%  Память: {mem}%  Диск: {disk}%")
        save_stats()
    elif choice == "2":
        print("\nПоследние записи:")
        for row in conn.execute("SELECT * FROM stats ORDER BY time DESC LIMIT 5"):
            print(f"{row[0]}  CPU:{row[1]}%  Mem:{row[2]}%  Disk:{row[3]}%")
    elif choice == "3":
        try:
            while True:
                save_stats()
                print(f"\r{get_stats()}", end='')
                time.sleep(2)
        except KeyboardInterrupt:
            pass
while True:
    show_stats()
    if input("\nПродолжить? (y/n): ") != 'y':
        break
conn.close()