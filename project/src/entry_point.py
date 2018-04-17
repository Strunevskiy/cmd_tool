import logging.config
import sys
from argparse import ArgumentParser

from project.src.base.entity import User, POSITION
from project.src.cli import BasePrompt


def convert_app_args(src_args: []):
    args = {}
    for arg in src_args:
        if "=" in arg:
            key, value = arg.split("=")
            args[key] = value
    return args


def validate_required_args(args: map, required_args: set):
    provided_args = args.keys()
    left_required_args = required_args - provided_args
    if len(left_required_args) != 0:
        print("Mandatory args were not specified or were specified incorrectly: {}".format(left_required_args))
        exit()


def validate_mode(args, mode_types):
    #    if mode not in mode_types:
    #        print("-mode was specified incorrectly. There are two possible types {}".format(mode_types))
    #        exit()
    pass


def validate_position(args, position_types):
    #    if position not in position_types:
    #       print("-position was specified incorrectly. There are two possible types {}".format(position_types))
    #        exit()
    pass


def main():
    logging.config.fileConfig('./config/logging.ini')

    app_args = sys.argv
    required_args = {"-first_name", "-last_name", "-position", "-mode"}
    mode_types = ["command_line", "interactive"]
    position_types = [POSITION.MANAGER, POSITION.SALESMAN]

    args = convert_app_args(app_args)

    validate_required_args(args, required_args)
    validate_mode(args, mode_types)
    validate_position(args, position_types)

    prompt = BasePrompt.get_prompt(User(args.get("-first_name"), args.get("-last_name"), args.get("-position")))
    mode = args.get("-mode")
    if mode == mode_types[0]:
        prompt.onecmd(args.get("-command"))
    elif mode == mode_types[1]:
        prompt.cmdloop()


if __name__ == "__main__": main()
