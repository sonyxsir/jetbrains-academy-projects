from random import randint
import sqlite3


class Card:
    def __init__(self):
        self.__iin = "400000"

        rand_account_number = str(randint(0, 999999999))
        diff = 9 - len(rand_account_number)
        self.__account_number = diff * "0" + rand_account_number

        self.__checksum = self.get_chechsum()

        rand_pin = str(randint(0, 9999))
        diff = 4 - len(rand_pin)
        self.__pin = diff * "0" + rand_pin

        self.__balance = 0

    def get_chechsum(self):
        card_number = self.__iin + self.__account_number

        luhn_list = list(map(int, card_number))
        luhn_list = [luhn_list[_] * 2 if _ % 2 == 0 else luhn_list[_] for _ in range(len(luhn_list))]
        luhn_list = [_ - 9 if _ > 9 else _ for _ in luhn_list]
        return str(10 - sum(luhn_list) % 10 if sum(luhn_list) % 10 != 0 else 0)

    def get_full_number(self):
        self.__checksum = self.get_chechsum()
        return self.__iin + self.__account_number + self.__checksum

    def get_pin(self):
        return self.__pin

    def get_balance(self):
        return self.__balance

    def set_account_number(self, full_number):
        self.__account_number = full_number[6:15]
        self.__iin = full_number[:6]

    def set_pin(self, number):
        self.__pin = number

    def set_balance(self, number):
        self.__balance = number


def get_choice():
    return input(">")


def read_card(card_sql):
    card = Card()
    card.set_account_number(card_sql[1])
    card.set_pin(card_sql[2])
    card.set_balance(card_sql[3])
    return card


def update_card(card):
    card_sql = (card.get_pin(), card.get_balance())
    cursor.execute(f"UPDATE card SET (pin, balance) = (?, ?) WHERE number = {card.get_full_number()}", card_sql)
    connector.commit()


def log_in():
    print("\nEnter your card number:")
    card_number = input(">")
    print("Enter your PIN:")
    pin = input(">")
    cursor.execute(f"SELECT * FROM card WHERE number = {card_number}")
    card_sql = cursor.fetchone()
    if card_sql:
        if pin == card_sql[2]:
            card = read_card(card_sql)
            return card
    return None


def perform_operation(user_choice: str):
    if user_choice == "1":
        card = Card()
        card_sql = (card.get_full_number(), card.get_pin())
        cursor.execute("INSERT INTO card (number, pin) VALUES (?, ?)", card_sql)
        connector.commit()
        print(f"\nYour card has been created\nYour card number:\n{card.get_full_number()}\n{card.get_pin()}\n")

    elif user_choice == "2":
        card = log_in()
        if card:
            print("\nYou have successfully logged in!\n")
            perform_operations_logged_in(card)
        else:
            print("\nWrong card number or PIN!\n")

    elif user_choice == "0":
        print("\nBye!")

    else:
        print("\nWrong choice! in main\n")


def perform_operations_logged_in(card: Card):
    global choice
    print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
    user_choice = get_choice()
    if user_choice == "1":
        print(f"\nBalance: {card.get_balance()}\n")
        perform_operations_logged_in(card)

    elif user_choice == "2":
        print("\nEnter income:")
        income = int(input(">"))
        card.set_balance(card.get_balance() + income)
        update_card(card)
        print("Income was added!\n")
        perform_operations_logged_in(card)

    elif user_choice == "3":
        print("\nTransfer\nEnter card number:")
        tr_card_number = input(">")
        tr_card = Card()
        tr_card.set_account_number(tr_card_number)
        cursor.execute(f"SELECT * FROM card WHERE number = {tr_card_number}")
        tr_card_sql = cursor.fetchone()
        if tr_card_number == card.get_full_number():
            print("You can't transfer money to the same account!\n")
            perform_operations_logged_in(card)
        elif tr_card_number != tr_card.get_full_number():
            print("Probably you made mistake in the card number. Please try again!\n")
            perform_operations_logged_in(card)
        elif not tr_card_sql:
            print("Such a card does not exist.\n")
            perform_operations_logged_in(card)
        else:
            print("Enter how much money you want to transfer:")
            transfer = int(input(">"))
            if transfer > card.get_balance():
                print("Not enough money!\n")
                perform_operations_logged_in(card)
            else:
                card.set_balance(card.get_balance() - transfer)
                tr_card.set_balance(tr_card.get_balance() + transfer)
                tr_card.set_pin(tr_card_sql[2])
                update_card(card)
                update_card(tr_card)
                print("Success!\n")
                perform_operations_logged_in(card)

    elif user_choice == "4":
        cursor.execute(f"DELETE FROM card WHERE number = {card.get_full_number()}")
        connector.commit()
        print("\nThe account has been closed!\n")

    elif user_choice == "5":
        print("\nYou have successfully logged out!\n")

    elif user_choice == "0":
        choice = "0"
        perform_operation(choice)

    else:
        print("\nWrong choice! logged\n")
        perform_operations_logged_in(card)


if __name__ == "__main__":
    connector = sqlite3.connect("card.s3db")
    cursor = connector.cursor()
    try:
        cursor.execute("""CREATE TABLE card (
                            id INTEGER PRIMARY KEY,
                            number TEXT,
                            pin TEXT,
                            balance INTEGER DEFAULT 0
                     );""")
        connector.commit()
    except sqlite3.OperationalError:
        pass

    choice = ""
    while choice != "0":
        print("1. Create an account\n2. Log into account\n0. Exit")
        choice = get_choice()
        perform_operation(choice)
