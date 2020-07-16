from random import choice


def set_state(state: list):

    for i in range(len(state)):
        if state[i] == "_":
            state[i] = " "

    state_printable = ""
    state_printable += "---------\n"
    state_printable += f"| {state[0]} {state[1]} {state[2]} |\n"
    state_printable += f"| {state[3]} {state[4]} {state[5]} |\n"
    state_printable += f"| {state[6]} {state[7]} {state[8]} |\n"
    state_printable += "---------"
    return state_printable


def is_winner(player: str, state: list):

    win_states = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                  [0, 3, 6], [1, 4, 7], [2, 5, 8],
                  [0, 4, 8], [2, 4, 6]]

    for win in win_states:
        if state[win[0]] == player and state[win[1]] == player and state[win[2]] == player:
            return True
    return False


def check_state(state: list):
    x_wins, o_wins = is_winner("X", state), is_winner("O", state)
    if not x_wins and not o_wins:
        if state.count(" ") > 0:
            return "Game not finished"
        else:
            return "Draw"
    else:
        if x_wins:
            return "X wins"
        else:
            return "O wins"


def move_user(player: str, state: list):

    corr = {(1, 1): 6, (2, 1): 7, (3, 1): 8,
            (1, 2): 3, (2, 2): 4, (3, 2): 5,
            (1, 3): 0, (2, 3): 1, (3, 3): 2
            }
    try:
        throw = tuple(map(int, input("Enter the coordinates: > ").split(" ")))

        if len(throw) != 2:
            print("You should enter two numbers!")
            return move_user(player, state)
        else:
            for coord in throw:
                if coord not in (1, 2, 3):
                    print("Coordinates should be from 1 to 3!")
                    return move_user(player, state)
            if state[corr[throw]] != " ":
                print("This cell is occupied! Choose another one!")
                return move_user(player, state)
        state[corr[throw]] = player
    except ValueError:
        print("You should enter numbers!")
        return move_user(player, state)


def move_easy(player: str, state: list):
    print('Making move level "easy"')
    free_cells = [i for i in range(len(state)) if state[i] == " "]
    state[choice(free_cells)] = player


def move_medium(player: str, state: list):
    print('Making move level "medium"')
    free_cells = [i for i in range(len(state)) if state[i] == " "]
    opponent = "O" if player == "X" else "X"
    for cell in free_cells:
        state[cell] = player
        if check_state(state) == f"{player} wins":
            break
        else:
            state[cell] = " "
    else:
        for cell in free_cells:
            state[cell] = opponent
            if check_state(state) == f"{opponent} wins":
                state[cell] = player
                break
            else:
                state[cell] = " "
        else:
            state[choice(free_cells)] = player


def move_hard(player: str, state: list):
    print('Making move level "hard"')
    state[minimax(player, state)[0]] = player


def minimax(player: str, state: list):
    free_cells = [i for i in range(len(state)) if state[i] == " "]
    ai_player = "X" if player == "X" else "O"
    opponent = "O" if ai_player == "X" else "X"

    best = [-1, -100] if player == ai_player else [-1, 100]

    if len(free_cells) == 0:
        if check_state(state) == f"{ai_player} wins":
            score = 10
        elif check_state(state) == f"{opponent} wins":
            score = -10
        else:
            score = 0
        return [-1, score]

    for cell in free_cells:
        state[cell] = player
        if player == ai_player:
            score = minimax(opponent, state)
        else:
            score = minimax(ai_player, state)
        score[0] = cell
        state[cell] = " "

        if player == ai_player:
            if score[1] > best[1]:
                best = score
        else:
            if score[1] < best[1]:
                best = score

    return best


def make_throw(player: str, player_type: str, state: list):
    if player_type == "easy":
        move_easy(player, state)
    elif player_type == "medium":
        move_medium(player, state)
    elif player_type == "hard":
        move_hard(player, state)
    else:
        move_user(player, state)


def play(players: dict):
    # current_state = list("_________")
    current_state = list("_________")
    print(set_state(current_state))

    current_player = "X"

    while check_state(current_state) not in ("X wins", "O wins", "Draw"):
        make_throw(current_player, players[current_player], current_state)
        print(set_state(current_state))
        current_player = "O" if current_player == "X" else "X"

    print(check_state(current_state))


def main():
    players = {"X": "", "O": ""}
    command = [""]
    while command[0] != "exit":
        command = input("Input command: > ").split()
        if command:
            if command[0] == "start":
                try:
                    players["X"] = command[1] if command[1] in ("user", "easy", "medium", "hard") else ""
                    players["O"] = command[2] if command[2] in ("user", "easy", "medium", "hard") else ""
                    if players["X"] == "" or players["O"] == "":
                        print("Bad parameters!")
                    else:
                        play(players)
                except IndexError:
                    print("Bad parameters!")
            elif command[0] == "exit":
                pass
            else:
                print("Bad parameters!")
        else:
            command = [""]
            print("Bad parameters!")


if __name__ == "__main__":
    main()
