from collections import UserDict
from datetime import datetime
import pickle
import os.path

PATH_TO_SAVE = "data.bin"

def input_error(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except KeyError:
            return "KeyError. This name is not in phone-book"
        except ValueError:
            return "ValueError. Phone number must be from 10 digit"
        except TypeError:
            return "TypeError. Unknown command"
        except IndexError:
            return "IndexError. Give me name and phone please"
    return inner

class Field: 
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
class Name(Field):
    def __setitem__(self, value):
        if value > 0:
            self.data.append(value)

    def __getitem__(self, idx=None):
        if idx is None:
            return self.data
        return self.data[idx]

class Birthday(Field):
    def __init__(self, value):
        self.value = Birthday.correct_birthday(value)
        
    def correct_birthday(date):
        if date:
            try:
                d = datetime.strptime(date, '%d %B %Y').date()
                return d
            except:
                    try:
                        d = datetime.strptime(date, '%d %b %Y').date()
                        return d 
                    except:
                        print('Invalid birthday date. Format "day" "month" "year"') 
                        return None   

    def __getitem__(self, idx=None):
        if idx is None:
            return self.data
        return self.data[idx]

    def __setitem__(self, date):
        self.value = Birthday.correct_birthday(date)

class Phone(Field):
    def __init__(self, value):
        self.value = value
  
    def __str__(self):
        return f"{self.value}"
    
    def __setitem__(self, value):

        if len(value) != 10 or not value.isdigit():
            raise ValueError("Number is not valid")
        else:
            self.value = value
    
    def __getitem__(self, idx=None):
        if idx is None:
            return self.data
        return self.data[idx]
 
class Record():
    def __init__(self, name, phone = None, birthday = None):
        self.name = Name(value=name)
        self.phones = []
        if phone:
            self.add_phone_number(value = phone)
        if birthday:
            self.birthday = Birthday(value=birthday)

    def __repr__(self):
        return f"Name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def days_to_birthday(self):
        if self.birthday.value != None:
            today = datetime.now().date()
            b_day = datetime(year=today.year, month=self.birthday.value.month, day=self.birthday.value.day).date()
            
            if b_day < today:
                b_day = datetime(year=today.year+1, month=self.birthday.value.month, day=self.birthday.value.day).date()
            time_diff = b_day - today
            tdays = time_diff.days
            if tdays == 0:
                print(f"Your birthday is today.")
            else:
                print(f"Your birthday is in {tdays} days.")

    def edit_phone(self, phone_old, phone_new):
        num = None
        for i in self.phones:
            if i.value == phone_old:
                num = phone_old
                i.value = phone_new

        if num is None:
            raise ValueError
    
    def save_record(self):
        with open(PATH_TO_SAVE, "wb") as fh:
            pickle.dump(self, fh)
        
    def remove_phone(self, phone):
         for i in self.phones:
            if i.value == phone:
                self.phones.remove(i)

    def find_phone(self, phone):
        for i in self.phones:
            if i.value == phone:
                return i
         
class AddressBook(UserDict):
    
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    
    def find(self, name: Name):
         for i in self.data:
            if i == name:
                return self.data[i]
    
    def delete(self, name: Name):
        try:
            self.data.pop(name)
        except:
            KeyError   

    def save_record(self):
        with open(PATH_TO_SAVE, "wb") as fh:
            pickle.dump(self, fh)
    
    def __repr__(self):
        print ("Adress book:")
        for record in self.data.values():
            print(record)
        return 'end'
        
    def load_from_file(self):
        with open(PATH_TO_SAVE, "rb") as fh:
            data = pickle.load(fh)
            return data
    
    def find_anything(self, ch):
        find_list = list()
        for i in self.data:
            if ch in i:
                find_list.append(self.data[i])

        for i, j in self.data.items():
            for p in j.phones:
                if ch in p.value:
                    find_list.append(j)
        return find_list

def main():
    book = AddressBook()
    check_file = os.path.exists(PATH_TO_SAVE)
    if check_file:
        book = book.load_from_file()

    # Створення запису для John
    john_record = Record("John", "", '30 May 2020')
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    #john_record.days_to_birthday()
    print(john_record)
    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane99")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    print(book)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    res = book.find_anything("987")
    print(f' find {res}')
    john.edit_phone("1234567890", "1112223333")

    # Пошук конкретного телефону у записі John
    #found_phone = john.find_phone("5555555555")
    #print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    jane_record2 = Record("Jane2")
    jane_record2.add_phone("9876543210")
    book.add_record(jane_record2)
 
    #john_record.save_record()
    book.save_record()
    
if __name__ == '__main__':
    main()