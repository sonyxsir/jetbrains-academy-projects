from random import choice

player_name, player_rating, win_strategy = "", 0, {}


def get_name():
    print("Enter your name: ")
    return input()


def greet(player: str):
    print(f"Hello, {player}")


def get_start_rating(player: str):
    rating = {}
    with open("rating.txt", "r") as f:
        for line in f:
            current_player = line.split()
            rating[current_player[0]] = int(current_player[1])
    try:
        return rating[player]
    except KeyError:
        return 0


def get_current_rating():
    return f"Your rating: {player_rating}"


def get_options():
    options = input().split(",")
    return ["rock", "paper", "scissors"] if options == [""] else options


def set_options(options: list):
    global win_strategy

    # how many other options each one beats
    num_to_beat = len(options) // 2
    # copy this number of options form the left side to right
    options.extend(options[:num_to_beat])

    # for each option slice the list needed and fill the dictionary
    for i in range(1, (num_to_beat + 1) * 2):
        win_strategy[options[i - 1]] = options[i: i + num_to_beat]

    print("Okay, let's start")


def get_step():
    global player_rating
    user_option = input()
    comp_option = choice(list(win_strategy.keys()))

    if user_option == "!rating":
        return get_current_rating()
    if user_option == "!exit":
        return "Bye!"
    if user_option == comp_option:
        player_rating += 50
        return f"There is a draw ({comp_option})"
    elif comp_option in win_strategy[user_option]:
        return f"Sorry, but computer chose {comp_option}"
    else:
        player_rating += 100
        return f"Well done. Computer chose {comp_option} and failed"


def play(name: str):
    greet(name)
    set_options(get_options())
    step = ""
    while step != "Bye!":
        try:
            step = get_step()
            print(step)
        except KeyError:
            print("Invalid input")


if __name__ == "__main__":
    player_name = get_name()
    player_rating = get_start_rating(player_name)
    play(player_name)
