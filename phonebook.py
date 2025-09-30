import sqlite3

conn = sqlite3.connect("phonebook.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    email TEXT
);
""")
conn.commit()



def add_contact(name, phone, email):
    try:
        cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
        conn.commit()
        print("✅ Контакт добавлен!")
    except sqlite3.IntegrityError:
        print("❌ Ошибка: такой номер уже существует!")

def show_contacts():
    cursor.execute("SELECT id, name, phone, email FROM contacts")
    contacts = cursor.fetchall()
    if contacts:
        for c in contacts:
            print(f"{c[0]}. {c[1]} — {c[2]} ({c[3]})")
    else:
        print("📭 Телефонная книга пуста!")

def find_contact(keyword):
    cursor.execute("SELECT id, name, phone, email FROM contacts WHERE name LIKE ? OR phone LIKE ?", (f"%{keyword}%", f"%{keyword}%"))
    contacts = cursor.fetchall()
    if contacts:
        for c in contacts:
            print(f"{c[0]}. {c[1]} — {c[2]} ({c[3]})")
    else:
        print("🔍 Контактов не найдено.")

def update_contact(contact_id, name, phone, email):
    cursor.execute("UPDATE contacts SET name=?, phone=?, email=? WHERE id=?", (name, phone, email, contact_id))
    conn.commit()
    print("✏️ Контакт обновлён!")

def delete_contact(contact_id):
    cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()
    print("🗑️ Контакт удалён!")



while True:
    print("\n📒 Телефонная книга:")
    print("1. Добавить контакт")
    print("2. Показать все контакты")
    print("3. Найти контакт")
    print("4. Обновить контакт")
    print("5. Удалить контакт")
    print("6. Выйти")

    choice = input("Выберите действие: ")

    if choice == "1":
        name = input("Имя: ")
        phone = input("Телефон: ")
        email = input("Email: ")
        add_contact(name, phone, email)
    elif choice == "2":
        show_contacts()
    elif choice == "3":
        keyword = input("Введите имя или телефон: ")
        find_contact(keyword)
    elif choice == "4":
        contact_id = int(input("ID контакта для обновления: "))
        name = input("Новое имя: ")
        phone = input("Новый телефон: ")
        email = input("Новый Email: ")
        update_contact(contact_id, name, phone, email)
    elif choice == "5":
        contact_id = int(input("ID контакта для удаления: "))
        delete_contact(contact_id)
    elif choice == "6":
        print("👋 Выход...")
        break
    else:
        print("❌ Неверный выбор!")