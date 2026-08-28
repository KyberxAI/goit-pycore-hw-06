# Консольний бот помічник

import re
from collections import UserDict


class Field:
    # Батьківський клас для полів Name і Phone
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # Клас наслідує конструктор і методи Field
    pass


class Phone(Field):
    # Клас наслідує конструктор і методи Field
    # екземпляр Field створюється тільки після валідації
    def __init__(self, value):
        if self.phone_validation(value):
            super().__init__(value)
        else:
            raise ValueError("Телефон повинен мати 10 цифр.")

    # перевірка на 10 цифр
    def phone_validation(self, phone_number: str) -> bool:
        return bool(re.fullmatch(r"\d{10}", phone_number))


class Record:
    # Клас для зберігання інформації про контакт, включно з іменем та списком телефонів.
    def __init__(self, name: str):
        # Магічний метод конструктор нового екземпляра
        self.name = Name(name)
        self.phones = []

    def __str__(self) -> str:
        # Магічний метод представлення строкою
        return f"Ім'я контакта: {self.name.value}, номер: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone_number: str) -> None:
        # метод додавання номера телефона
        self.phones.append(Phone(phone_number))


    def find_phone(self, phone_number: str) -> Phone | None:
        # метод пошуку об'єктів Phone
        for phone_el in self.phones:
            if phone_el.value == phone_number:
                return phone_el
        return None


    def edit_phone(self, current_phone_number: str, new_phone_number: str) -> None:
        # метод редагування номера телефона
        phone_record = self.find_phone(current_phone_number)
        if phone_record:
            phone_index = self.phones.index(phone_record)
            self.phones[phone_index] = Phone(new_phone_number)
        else:
            raise ValueError(f"Номер телефону {current_phone_number} відсутній.")


    def remove_phone(self, phone_number: str) -> None:
        # метод видалення номера телефона
        phone_record = self.find_phone(phone_number)
        if phone_record:
            self.phones.remove(phone_record)
        else:
            raise ValueError(f"Номер телефону {phone_number} відсутній.")


class AddressBook(UserDict):
    # Клас для зберігання записів та керування ними

    def add_record(self, record: Record) -> None:
        # Метод додає запис до self.data
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        # Метод пошуку запису за ім'ям
        return self.data.get(name)

    def delete(self, name: str) -> None:
        # Метод видалення запису за ім'ям
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Запис {name} відсутній.")


# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону в записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")
