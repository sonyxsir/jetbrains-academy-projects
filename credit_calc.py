import argparse
import math


def calculate_credit(credit_params: dict, arguments_parsed):
    credit_params["type"] = None
    for key, value in vars(arguments_parsed).items():
        if value:
            credit_params[key] = value

    if (credit_params["type"] != "diff" and credit_params["type"] != "annuity") or (not has_interest(credit_params)) \
            or (len(credit_params) < 4) or has_negative(credit_params):
        return throw_error_msg()
    else:
        if credit_params["type"] == "diff":
            if has_payment(credit_params):
                return throw_error_msg()
            else:
                return calc_diff(credit_params)
        if credit_params["type"] == "annuity":
            try:
                credit_params["payment"]
            except KeyError:
                return calc_payment(credit_params)
            try:
                credit_params["principal"]
            except KeyError:
                return calc_pricipal(credit_params)
            try:
                credit_params["periods"]
            except KeyError:
                return calc_periods(credit_params)


def has_interest(dictionary: dict):
    state = True
    try:
        dictionary["interest"]
    except KeyError:
        state = False
    return state


def has_negative(dictionary: dict):
    state = False
    for key in dictionary.keys():
        try:
            if dictionary[key] < 0:
                state = True
        except TypeError:
            pass
    return state


def has_payment(dictionary: dict):
    state = True
    try:
        dictionary["payment"]
    except KeyError:
        state = False
    return state


def throw_error_msg():
    return "Incorrect parameters"


def calc_diff(dictionary: dict):
    response = ""
    p, i, n, m = dictionary["principal"], dictionary["interest"] / 1200, dictionary["periods"], 1
    overpayment = - p

    for m in range(1, n + 1):
        d = math.ceil(p / n + i * (p - p * (m - 1) / n))
        overpayment += d
        response += f"Month {m}: paid out {d}\n"
    response += f"\nOverpayment = {math.ceil(overpayment)}"

    return response


def calc_payment(dictionary: dict):
    p, i, n = dictionary["principal"], dictionary["interest"] / 1200, dictionary["periods"]
    a = math.ceil(p * (i * math.pow(1 + i, n) / (math.pow(1 + i, n) - 1)))
    overpayment = math.ceil(a * n - p)

    return f"Your annuity payment = {a}!\nOverpayment = {overpayment}"


def calc_pricipal(dictionary: dict):
    a, i, n = dictionary["payment"], dictionary["interest"] / 1200, dictionary["periods"]
    p = math.floor(a / (i * math.pow(1 + i, n) / (math.pow(1 + i, n) - 1)))
    overpayment = math.ceil(a * n - p)

    return f"Your credit principal = {p}!\nOverpayment = {overpayment}"


def calc_periods(dictionary: dict):
    p, i, a = dictionary["principal"], dictionary["interest"] / 1200, dictionary["payment"]
    n = math.ceil(math.log(a / (a - i * p), 1 + i))
    n_years, n_months = n // 12, n % 12
    if n_years > 0:
        n_years_formatted = f"{n_years} years"
        if n_years == 1:
            n_years_formatted = n_years_formatted.replace("years", "year")
    else:
        n_years_formatted = ""
    if n_months > 0:
        n_months_formatted = f"{n_months} months"
        if n_months == 1:
            n_months_formatted = n_months_formatted.replace("months", "month")
    else:
        n_months_formatted = ""
    and_string = " and " if n_months_formatted and n_years_formatted else ""
    overpayment = math.ceil(a * n - p)

    return "You need {0}{1}{2} to repay this credit!\nOverpayment = {3}".format(
        n_years_formatted, and_string, n_months_formatted, overpayment)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str)
    parser.add_argument("--payment", type=float)
    parser.add_argument("--principal", type=float)
    parser.add_argument("--periods", type=int)
    parser.add_argument("--interest", type=float)
    args = parser.parse_args()

    params = {}

    print(calculate_credit(params, args))
