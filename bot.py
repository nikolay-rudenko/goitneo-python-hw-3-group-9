from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self.validate():
            raise ValueError("Invalid phone number")

    def validate(self):
        return len(self.value) == 10 and self.value.isdigit()


class Birthday(Field):
    def __init__(self, date_string):
        super().__init__(date_string)
        if not self.validate():
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY")

    def validate(self):
        try:
            datetime.strptime(self.value, "%d.%m.%Y")
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                break

    def find_phone(self, phone_number):
        return next((phone for phone in self.phones if phone.value == phone_number), None)

    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

    def days_to_birthday(self):
        if not self.birthday:
            return None

        today = datetime.date.today()
        birthday_date = datetime.date(today.year, self.birthday.month, self.birthday.day)

        if birthday_date < today:  # День народження вже пройшов цього року
            birthday_date = birthday_date.replace(year=today.year + 1)

        return (birthday_date - today).days


    def __str__(self):
        return (f"Contact name: {self.name.value}, "
                f"phones: {'; '.join(p.value for p in self.phones)}, "
                f"birthday: {self.birthday}" if self.birthday else "")


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]


def add_birthday_handler(args):
    if len(args) != 3:
        return "Invalid command usage: add_birthday <name> <birthday>"
    name, birthday = args[1:]
    contact = book.find(name)
    if contact:
        contact.add_birthday(birthday)
        return f"Birthday added for {name}"
    else:
        return f"Contact {name} not found"

def show_birthday_handler(args):
    if len(args) != 2:
        return "Invalid command usage: show_birthday <name>"
    name = args[1]
    contact = book.find(name)
    if contact and contact.birthday:
        return f"Birthday for {name}: {contact.birthday}"
    else:
        return f"Contact {name} does not have a birthday or not found"

def show_birthdays_next_week_handler(args):
    today = datetime.date.today()
    next_week = today + datetime.timedelta(days=7)
    birthdays = []
    for contact in book.values():
        if contact.birthday:
            birthday_date = datetime.date(contact.birthday.year, contact.birthday.month, contact.birthday.day)
            if birthday_date >= today and birthday_date <= next_week:
                birthdays.append(contact)
    return (f"Upcoming birthdays within the next week:\n")

