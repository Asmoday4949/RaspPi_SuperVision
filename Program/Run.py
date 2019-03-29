from Web.Server import *
from Config import *
import getpass
import re

DEFAULT_PORT = 465
MIN_PORT = 0
MAX_PORT = 65535

USER_CONFIG_FILENAME = "user_config.json"

def print_title():
    print(r"""
        __________ __________ .___    _________       .__         .__
        \______   \\______   \|   |  /   _____/___  __|__|  ______|__|  ____    ____
         |       _/ |     ___/|   |  \_____  \ \  \/ /|  | /  ___/|  | /  _ \  /    \
         |    |   \ |    |    |   |  /        \ \   / |  | \___ \ |  |(  <_> )|   |  \
         |____|_  / |____|    |___| /_______  /  \_/  |__|/____  >|__| \____/ |___|  /
                \/                          \/                 \/                  \/
        Author(s) : Malik Fleury        Date : 29.03.2019           Version : 1.0
        """)

def ask_email():
    not_valid = True
    while not_valid:
        email = input("Email : ")
        email = str(email)
        not_valid = not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    return email

def ask_password():
    password = "a"
    confirmation = "b"
    while password != confirmation:
        password = getpass.getpass("Password : ")
        confirmation = getpass.getpass("Confirmation : ")
        password = str(password)
        confirmation = str(confirmation)
    return password

def ask_server_address():
    address = input("SMTP server adress : ")
    return str(address)

def ask_server_port():
    port = -1
    while port < MIN_PORT or port > MAX_PORT:
        port = input("Port : ")
        try:
            port = int(port)
        except:
            print("Only integers are allowed !")
            port = -1
    return port

def ask_user_config():
    print("""
            --- CONFIGURATION WIZARD -------------------------------
            This is the first time that the application is launched.
            Please complete the settings :
            """)
    email = ask_email();
    password = ask_password();
    address = ask_server_address();
    port = ask_server_port();

    print("""
            --- RECAP ----------------------------------------------
            Email : {}
            Address : {}
            Port : {}
            """.format(email, address, port))

    data = dict()
    data["email"] = email
    data["password"] = password
    data["address"] = address
    data["port"] = port
    return Config(USER_CONFIG_FILENAME, data)

def ask_detection_config():
    None

def load_user_config(user_config_name):
    config = Config(user_config_name)
    if not config.exist():
        print("""
            Config. file : not found !
            """)
        config = ask_user_config()
        config.save()
    else:
        print("""
            Config. file : found !
            """)
        config.load()

def load_detection_config(detection_config_name):
    config = Config(detection_config_name)
    if not config.exist():
        print("""
            Config. file : not found !
            """)
        config = ask_user_config()
        config.save()
    else:
        print("""
            Config. file : found !
            """)
        config.load()

if __name__ == "__main__":
    print_title()
    load_user_config(USER_CONFIG_FILENAME)
    execute_server()
