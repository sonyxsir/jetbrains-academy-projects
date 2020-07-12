from collections import deque


vars_ = {}


def infix_to_postfix(string: str):
    ops = {"+": 0, "-": 0, "*": 1, "/": 1, "^": 2, "(": -1, ")": -1}

    if string == "":
        return None

    while string.count("--") != 0:
        string = string.replace("--", "+")
    while string.count("++") != 0:
        string = string.replace("++", "+")
    string = string.replace("+-", "-")

    string = string.replace("+", " + ")
    string = string.replace("-", " - ")
    string = string.replace("*", " * ")
    string = string.replace("/", " / ")
    string = string.replace("^", " ^ ")
    string = string.replace("(", " ( ")
    string = string.replace(")", " ) ")

    infix = string.split()
    # number neighbourhood error
    for i in range(len(infix) - 1):
        if infix[i] not in ops.keys() and infix[i + 1] not in ops.keys():
            return "Invalid expression"

    stack = deque()
    postfix = []

    for item in infix:
        if item in vars_:
            item = vars_[item]
        try:
            postfix.append(int(item))
        except ValueError:
            try:
                if (item not in ops.keys()) and (item not in "()"):
                    return "Unknown variable"
                else:
                    if len(stack) == 0 or item == "(":
                        stack.append(item)
                    elif item == ")":
                        top = stack.pop()
                        while top != "(":
                            postfix.append(top)
                            top = stack.pop()
                    else:
                        top = stack.pop()
                        if top == "(" or ops[item] > ops[top]:
                            stack.append(top)
                            stack.append(item)
                        else:
                            while top != "(" and ops[item] <= ops[top]:
                                postfix.append(top)
                                if len(stack) == 0:
                                    break
                                else:
                                    top = stack.pop()
                            else:
                                stack.append(top)
                            stack.append(item)
            except (KeyError, IndexError):
                return "Invalid expression"
        # print(item, stack)
    while len(stack) != 0:
        postfix.append(stack.pop())
    if "(" in postfix:
        return "Invalid expression"

    return postfix


def operate(second, first, operand):
    if operand == "+":
        return first + second
    elif operand == "-":
        return first - second
    elif operand == "*":
        return first * second
    elif operand == "/":
        return int(first / second)
    elif operand == "^":
        return first ** second


def evaluate_postfix(postfix: list):
    if not postfix:
        return None
    if postfix in ("Invalid expression", "Unknown variable"):
        return postfix
    ops = ["+", "-", "*", "/", "^"]
    stack = deque()

    try:
        for item in postfix:
            if item not in ops:
                stack.append(item)
            else:
                result = operate(stack.pop(), stack.pop(), item)
                stack.append(result)
    except IndexError:
        return "Invalid expression"
    return stack.pop()


def calculate_vars(string: str):
    for key in vars_.keys():
        string = string.replace(key, vars_[key])
    return string


def assign_var(variable: str, value: str):
    variable = variable.strip()
    if not variable.isalpha():
        return "Invalid identifier"
    assignment = evaluate_postfix(infix_to_postfix(value))
    if assignment in ("Invalid expression", "Unknown variable"):
        return "Invalid assignment"
    vars_[variable] = str(assignment)


def main():
    user_input = input()
    while user_input != "/exit":
        if user_input.startswith("/"):
            if user_input == "/help":
                print("The program performs +, -, *, / and ^. () and variables are supported.")
            else:
                print("Unknown command")
        else:
            result = None
            if "=" in user_input:
                assignment = user_input.split("=")
                try:
                    result = assign_var(*assignment)
                except TypeError:
                    print("Invalid assignment")
            else:
                infix = calculate_vars(user_input)
                result = evaluate_postfix(infix_to_postfix(infix))
            if result is not None:
                print(result)
        user_input = input()
    print("Bye!")


if __name__ == "__main__":
    main()
