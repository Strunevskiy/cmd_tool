import logging.config
import os

from project.src.cmd import BasePrompt
from project.src.base.entity import User


def main():
    logging.config.fileConfig('./config/logging.ini')

    user = User("Oleg", "Struneusk'i", "manager")
    prompt = BasePrompt.get_prompt(user)
    prompt.prompt = '> '
    prompt.cmdloop(user.get_position())


def fullname():
    os.system('clear')
    print("Welcome")
    choice = input(">  ")
    exec_menu(choice)
    return


def position():
    os.system('clear')
    choice = input(">  ")
    exec_menu(choice)
    return


def exec_menu(choice):
    os.system('clear')

    ch = choice.lower()
    if ch == '':
        actions['fullname']()
    else:
        try:
            actions[ch]()
        except KeyError:
            print("Invalid selection, please try again.")
            actions['fullname']()
    return

actions = {'fullname': fullname, 'position': position}

if __name__ == "__main__": main()
