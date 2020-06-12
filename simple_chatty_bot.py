def greet(bot_name: str, bot_year_created: int):
    print(f"Hello! My name is {bot_name}.\nI was created in {bot_year_created}.")


def remind_name():
    user_name = input("Please, remind me your name.\n> ")
    print(f"What a great name you have, {user_name}!")


def guess_age():
    print("Let me guess your age.\nEnter remainders of dividing your age by 3, 5 and 7.")
    remainder3, remainder5, remainder7 = int(input("> ")), int(input("> ")), int(input("> "))

    user_age = (remainder3 * 70 + remainder5 * 21 + remainder7 * 15) % 105
    print(f"Your age is {user_age}; that's a good time to start programming!")


def count():
    print("Now I will prove to you that I can count to any number you want.")
    count_number = int(input())
    for i in range(count_number + 1):
        print(f"{i} !")


def test():
    print("""Let's test your programming knowledge.
Why do we use methods?
1. To repeat a statement multiple times.
2. To decompose a program into several small subroutines.
3. To determine the execution time of a program.
4. To interrupt the execution of a program.""")
    correct_answer = 2
    user_answer = int(input("> "))
    while user_answer != correct_answer:
        print("Please, try again.")
        user_answer = int(input("> "))
    print("Completed, have a nice day!")


def send_bye_msg():
    print("Congratulations, have a nice day!")


if __name__ == "__main__":
    greet("Aid", 2020)
    remind_name()
    guess_age()
    count()
    test()
    send_bye_msg()
