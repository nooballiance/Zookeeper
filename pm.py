import getpass
from collections import OrderedDict
from peewee import *
from hashlib import sha256
from random import *
from playhouse.sqlcipher_ext import SqlCipherDatabase
import os


def login():
    countdown = 0
    while countdown < 3:
        try:
            p1 = getpass.getpass(
                "Enter master password, %s\n" % getpass.getuser())
            db.init('passwords.db', passphrase=p1)
            Service.create_table(fail_silently=True)
            break

        except DatabaseError:
            print("\nWrong password! Try again.\n")
            print(str(2 - countdown) + " chance(s) left!\n")

        countdown += 1
    if countdown == 3:
        print("Potential threat, Database deleted.")
        os.remove('./passwords.db')
        exit()


def get_hexdigest(salt, password):
    return sha256(salt + password).hexdigest()


SECRET_KEY = "s3cr3t"


def make_password(plaintext, service):
    salt = get_hexdigest(SECRET_KEY, service)[:20]
    hsh = get_hexdigest(salt, plaintext)
    return "".join((salt, hsh))


ALPHABET = "abcdefghijklmnopqrstuvwxyz"\
           "ABCDEFGHIJKLMNOPQRSTUVWXYZ"\
           "0123456789!@#$%^&*()-_"


def password(plaintext, service, length=10, alphabet=ALPHABET):
    raw_hexdigest = make_password(plaintext, service)

    num = int(raw_hexdigest, 16)

    num_chars = len(alphabet)
    chars = []
    while len(chars) < length:
        num, idx = divmod(num, num_chars)
        chars.append(alphabet[idx])

    return "".join(chars)


def generate(ktmp):
    tmp = ("".join(choice("ABCDEFGHIJKLMNOPQRST12345") for i in range(20)))
    return password(ktmp, tmp)


db = SqlCipherDatabase(None)


class Service(Model):
    name = CharField()
    savedpassword = CharField()

    class Meta:
        database = db


def add_entry():
    """Add entry"""
    serv = raw_input("\nService name\n\n")
    masterpass = raw_input("\nPassword\n\n")
    Service.create(name=serv, savedpassword=masterpass)
    print("\n\n Successful\n\n")


def edit_entry():
    """Edit entry"""
    print("\nu) update entry")
    print("\nd) delete entry")
    action = raw_input("\nChoice?\n\n")
    if action == "u":
        action2 = raw_input("\nEntry to update\n\n")
        temp = Service.get(Service.name == action2)
        action3 = raw_input("\nType updated name\n\n")
        temp.name = action3
        temp.save()
        print("\n\n Successful\n\n")
    elif action == "d":
        action2 = raw_input("\nEntry to delete\n\n")
        temp = Service.get(Service.name == action2)
        temp.delete_instance()
        print("\n\n Successful\n\n")


def update_password():
    """Update password, user-based/automated"""
    print("\nu) update password")
    print("\ng) generate new password")
    action = raw_input("\nChoice?\n\n")
    if action == "u":
        action2 = raw_input("\nEntry to update password of\n\n")
        temp = Service.get(Service.name == action2)
        action3 = raw_input("\nType updated paswword\n\n")
        temp.savedpassword = action3
        temp.save()
        print("\n\n Successful\n\n")
    elif action == "g":
        action2 = raw_input("\nEntry to update password of\n\n")
        temp = Service.get(Service.name == action2)
        action3 = generate(action2)
        print("\nGenerated password : {}".format(action3))
        temp.savedpassword = action3
        temp.save()
        print("\n\n Successful\n\n")


def view_entry():
    """View previous entries"""
    action = raw_input("\nPress w to print whole database else Enter\n\n")
    if action != "w":
        action2 = raw_input("\nEntry to view\n\n")
        temp = Service.get(Service.name == action2)
        print("\nNAME:", temp.name, "PASSWORD:", temp.savedpassword)
    elif action == "w":
        for i in Service.select():
            print("\nNAME:", i.name, "PASSWORD:", i.savedpassword)


def menu_loop():
    choice = None
    while choice != "q":
        print("\n\n\n")
        for key, value in menu.items():
            print("\n%s) %s" % (key, value.__doc__))
        choice = raw_input("\n==>Action: \n\nPress q to quit\n\n")
        if choice in menu:
            menu[choice]()


menu = OrderedDict([("a", add_entry), ("s", edit_entry),
                    ("p", update_password), ("v", view_entry)])


if __name__ == "__main__":

    login()
    menu_loop()
db.close()
