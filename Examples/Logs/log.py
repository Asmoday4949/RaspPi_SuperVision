import logging

# https://realpython.com/python-logging/

if __name__ == "__main__":
    logging.basicConfig(filename='debug.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    logging.warning('This is a warning message')
    logging.error('This is an error message')
    logging.critical('This is a critical message')
