import sys
import os
import requests as r
from bs4 import BeautifulSoup
from collections import deque
from colorama import init


strings_parsed = []


def is_valid_url(url: str):
    if "." in url:
        return True
    return False


def create_dir():
    try:
        dir_name = sys.argv[1]
    except IndexError:
        dir_name = "temp"
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        pass
    return dir_name


def cache_url(dir_name: str, url: str, cache: str):
    full_path = dir_name + "/" + url[:url.rindex(".")] + ".txt"
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(cache)


def get_parsed(parent):
    tags = ["p", "h1", "h2", "h3", "h4", "h5", "h6",
            "a", "ul", "ol", "li", "span"]
    children = parent.find_all(True, recursive=False)
    if len(children) == 0:
        if parent.name in tags:
            if parent.name == "a":
                strings_parsed.append('\033[34m' + parent.text.strip() + '\033[39m')
            else:
                strings_parsed.append(parent.text.strip())
    else:
        for child in children:
            get_parsed(child)
    return strings_parsed


def read_url(url: str):
    if not url.startswith("https://"):
        full_url = "https://" + url
    else:
        full_url = url

    soup = BeautifulSoup(r.get(full_url).content, "html.parser").find("body")

    return "\n".join(get_parsed(soup))


def read_cached_url(dir_name: str, url: str):
    full_path = dir_name + "/" + url + ".txt"
    with open(full_path, "r") as f:
        cache = f.read()
    return cache


def main():
    global strings_parsed

    init()
    dir_name = create_dir()
    stack = deque()
    user_input, current_page = "", ""
    while user_input != "exit":
        user_input = input("> ")
        if is_valid_url(user_input):
            stack.append(current_page)
            strings_parsed = []
            response = read_url(user_input)
            cache_url(dir_name, user_input.replace("https://", ""), response)
            print(response)
            current_page = response
        else:
            if user_input == "exit":
                pass
            elif user_input == "back":
                try:
                    current_page = stack.pop()
                    if current_page:
                        print(current_page)
                except IndexError:
                    pass
            else:
                try:
                    stack.append(current_page)
                    print(read_cached_url(dir_name, user_input))
                    current_page = read_cached_url(dir_name, user_input)
                except FileNotFoundError:
                    print("Error: Incorrect URL")


if __name__ == "__main__":
    main()
