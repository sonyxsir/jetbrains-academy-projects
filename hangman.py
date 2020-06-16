import random


def menu():
    print('Type "play" to play the game, "exit" to quit:')
    choice = ""
    while choice not in ("play", "exit"):
        choice = input()
    if choice == "play":
        play()
        menu()


def play():
    words_list = ("python", "java", "kotlin", "javascript")
    correct_answer = random.choice(words_list)
    word_list = ["-" for _ in range(len(correct_answer))]
    word_set, user_set, user_takes_set, count = set(correct_answer), set(), set(), 8

    while count > 0:
        print()
        print("".join(word_list))
        print("Input a letter: > ")
        letter = input()
        if letter in user_takes_set:
            print("You already typed this letter")
        elif len(letter) != 1:
            print("You should input a single letter")
        elif not letter.islower():
            print("It is not an ASCII lowercase letter")
        elif letter not in word_set:
            print("No such letter in the word")
            user_takes_set.add(letter)
            count -= 1
        else:
            for j in range(len(correct_answer)):
                if letter == correct_answer[j]:
                    word_list[j] = letter
            user_set.add(letter)
            user_takes_set.add(letter)
        if word_set == user_set:
            break

    if count == 0:
        print("You are hanged!\n")
    else:
        print(f"\n{correct_answer}\nYou guessed the word!\nYou survived!\n")


if __name__ == "__main__":
    print("H A N G M A N")
    menu()
