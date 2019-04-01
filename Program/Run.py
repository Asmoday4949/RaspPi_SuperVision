from Web.Server import *
from Config import *
import sys
import time
import getpass
import re

DEFAULT_PORT = 465
MIN_PORT = 0
MAX_PORT = 65535

MIN_THRESHOLD = 0
MAX_THRESHOLD = 255

USER_CONFIG_FILENAME = "user_config.json"
DETECTION_CONFIG_FILENAME = "detection_config.json"
APP_CONFIG_FILENAME = "app_config.json"

COMMANDS_LIST = ["ru", "rd", "ra", "em"]

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

def help():
    print("""
            --- HELP ----------------------------------------------
            Run.py      - Launch normally the app
            Run.py ru   - Reconfig the user info
            Run.py rd   - Reconfig the detection info
            Run.py ra   - Reconfig all
        """)

def parse_command():
    user_reconfig = detection_reconfig = False
    if len(sys.argv) > 1:
        command = sys.argv[1]
        user_reconfig = command == "ru" or command == "ra"
        detection_reconfig = command == "rd" or command == "ra"
    return user_reconfig, detection_reconfig

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
            --- USER CONFIGURATION ----------------------------------
            Please complete the settings :
            """)
    email = ask_email();
    password = ask_password();
    address = ask_server_address();
    port = ask_server_port();

    data = dict()
    data["email"] = email
    data["password"] = password
    data["address"] = address
    data["port"] = port
    return Config(USER_CONFIG_FILENAME, data)

def ask_min_threshold():
    min = -1
    while min < MIN_THRESHOLD or min > MAX_THRESHOLD:
        min = input("Min threshold (0-255) : ")
        try:
            min = int(min)
        except:
            print("Only integers are allowed !")
            min = -1
    return min

def ask_max_threshold():
    max = -1
    while max < MIN_THRESHOLD or max > MAX_THRESHOLD:
        max = input("Max threshold (0-255) : ")
        try:
            max = int(max)
        except:
            print("Only integers are allowed !")
            max = -1
    return max

def ask_blur():
    blur = 0
    while blur % 2 == 0:
        blur = input("Blur (odd) : ")
        try:
            blur = int(blur)
        except:
            print("Only integers are allowed !")
            blur = -1
    return blur

def ask_detection_config():
    print("""
            --- DETECTION CONFIGURATION -----------------------------
            Please complete the settings :
            """)
    min_threshold = ask_min_threshold()
    max_threshold = ask_max_threshold()
    blur = ask_blur()

    data = dict()
    data["min_threshold"] = min_threshold
    data["max_threshold"] = max_threshold
    data["blur"] = blur
    return Config(DETECTION_CONFIG_FILENAME, data)

def load_user_config(user_config_name, reconfig=False):
    config = Config(user_config_name)
    if not config.exist() or reconfig:
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
    return config

def load_detection_config(detection_config_name, reconfig=False):
    config = Config(detection_config_name)
    if not config.exist() or reconfig:
        print("""
            Config. file : not found !
            """)
        config = ask_detection_config()
        config.save()
    else:
        print("""
            Config. file : found !
            """)
        config.load()
    return config

def load_app_config(app_config_name):
    config = Config(app_config_name)
    
    data = dict()
    data["auto_mail_activation"] = False
    data["timeout"] = 10
    config.set_data(data)

    return config

if __name__ == "__main__":
    print_title()
    
    user_reconfig, detection_reconfig = parse_command()
    user_config = load_user_config(USER_CONFIG_FILENAME, user_reconfig)
    detection_config = load_detection_config(DETECTION_CONFIG_FILENAME, detection_reconfig)
    app_config = load_app_config(APP_CONFIG_FILENAME)

    launch_server(user_config, detection_config, app_config)
