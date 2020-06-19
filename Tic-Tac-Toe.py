def set_state(state: list):
    # generate cells_state from user input
    # state.extend(list(input("Enter cells: > ")))

    # generate empty field by default
    for _ in range(9):
        state.extend("_")


def get_state(state: list):

    # replace _'s for spaces to display the field properly
    for _ in range(len(state)):
        if state[_] == "_":
            state[_] = " "

    # prepare the field for displaying
    current_state = ""
    current_state += "---------\n"
    current_state += f"| {state[0]} {state[1]} {state[2]} |\n"
    current_state += f"| {state[3]} {state[4]} {state[5]} |\n"
    current_state += f"| {state[6]} {state[7]} {state[8]} |\n"
    current_state += "---------"
    return current_state


def count_field(field: str, state: list):

    # count number of cells containing field (X, O or empty)
    count = 0
    for item in state:
        if field == item:
            count += 1
    return count


def check_win(field: str, state: list):

    # all the eight win states
    win_states = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                  [0, 3, 6], [1, 4, 7], [2, 5, 8],
                  [0, 4, 8], [2, 4, 6]]

    # checking if field (X or O) is in win state
    for win in win_states:
        if state[win[0]] == field and state[win[1]] == field and state[win[2]] == field:
            return True
    return False


def check_state(state: list):
    has_empty = True if count_field(" ", state) > 0 else False
    check_win_x = check_win("X", state)
    check_win_o = check_win("O", state)

    # if the field has 2 more X than O and vice versa or some of them is already in win state
    if abs(count_field("X", state) - count_field("O", state)) > 1 or (check_win_x and check_win_o):
        return "Impossible"
    elif has_empty and (not check_win_x and not check_win_o):
        return "Game not finished"
    elif not has_empty and (not check_win_x and not check_win_o):
        return "Draw"
    elif check_win_x:
        return "X wins"
    elif check_win_o:
        return "O wins"


def get_throw():
    throw = list(input("Enter the coordinates: > ").split())
    throw_coords = []
    for _ in throw:
        if not _.isdigit():
            return "You should enter numbers!"
        elif _ not in ("1", "2", "3"):
            return "Coordinates should be from 1 to 3!"
        else:

            # throw is successful, collect coordinates
            throw_coords.append(int(_))

    # turn into tuple for using in dictionary as a key
    throw = tuple(throw_coords)
    return throw


def make_throw(player: str, throw, state: list):

    # dictionary to relate coordinates with a certain cell
    correspondence = {(1, 1): 6, (2, 1): 7, (3, 1): 8,
                      (1, 2): 3, (2, 2): 4, (3, 2): 5,
                      (1, 3): 0, (2, 3): 1, (3, 3): 2
                      }

    # if error in throw print it and make player try again
    if type(throw) == str:
        print(throw)
        make_throw(player, get_throw(), cells_state)
    else:
        # check if the cell is occupied and if yes make player try again
        if state[correspondence[throw]] != " ":
            print("This cell is occupied! Choose another one!")
            make_throw(player, get_throw(), cells_state)
        # make a throw
        else:
            state[correspondence[throw]] = player


if __name__ == "__main__":

    # create the field and display it
    cells_state = []
    set_state(cells_state)
    print(get_state(cells_state))

    # not necessary if the field is empty but useful in general case
    if check_state(cells_state) == "Impossible":
        pass
    else:
        # choose current player (X by default but may be O in general case)
        current_player = "O" if count_field("X", cells_state) > count_field("O", cells_state) else "X"
        while check_state(cells_state) == "Game not finished":
            make_throw(current_player, get_throw(), cells_state)
            current_player = "O" if current_player == "X" else "X"
            print(get_state(cells_state))

    print(check_state(cells_state))
