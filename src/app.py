#!/usr/bin/env python

import logging.config
from argparse import ArgumentParser

from src.base.entity import User
from src.cli import BasePrompt


def main():
    logging.config.fileConfig('./../config/logging.ini')
    # description a brief description of what the program does and how it works.
    parser = ArgumentParser(prog="coffee for me", description="coffee")
    parser.add_argument("first_name", metavar="first_name", help="user first name")
    parser.add_argument("last_name", metavar="last_name", help="user last name")
    parser.add_argument("position", metavar="role", choices=["salesman", "manager"], help="roles: %(choices)s")
    parser.add_argument("mode", metavar="mode", choices=["command_line", "interactive"], help="execution modes: %(choices)s")
    parser.add_argument("-c", "--command", nargs="*", help="Command to be executed. Please type help to see available commands", default="help")
    args = parser.parse_args()

    prompt = BasePrompt.get_prompt(User(args.first_name, args.last_name, args.position))
    command_line = " ".join(args.command)
    if args.mode == "command_line":
        prompt.onecmd(command_line)
    elif args.mode == "interactive":
        prompt.cmdloop(command_line)


if __name__ == "__main__": main()
