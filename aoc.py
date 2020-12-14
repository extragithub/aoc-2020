#!/usr/bin/env python3

import argparse
import os
import sys

from aoc_day import Days

AOC_DIR = os.path.dirname(os.path.abspath(__file__))


def cmd_list(args):
    """ list information about Advent of Code Days """
    print(Days(AOC_DIR))


cmd_list.spec = []


def cmd_new(args):
    """ initialize an Advent of Code Day """
    Days(AOC_DIR).New(args.day)


cmd_new.spec = [
    {
        "name": ["-d", "--day"],
        "help": "day to initialize: default is 0 to auto-select",
        "type": int,
        "default": 0,
    }
]


def cmd_run(args):
    """ run puzzle solutions for one or more Advent of Code Days """
    Days(AOC_DIR).Run(args.day, args.part)


cmd_run.spec = [
    {
        "name": ["-d", "--day"],
        "help": "day to run solution(s) for: default is -1 for latest",
        "type": int,
        "default": -1,
    },
    {
        "name": ["-p", "--part"],
        "help": "part of day to run solution(s) for: default is 0 for both",
        "type": int,
        "default": 0,
    },
]


def cmd_test(args):
    """ run one or more puzzle part tests for one or more Advent of Code Days """
    Days(AOC_DIR).Test(args.day, args.part, args.test)


cmd_test.spec = [
    {
        "name": ["-d", "--day"],
        "help": "day to run test(s) for: default is -1 for latest",
        "type": int,
        "default": -1,
    },
    {
        "name": ["-p", "--part"],
        "help": "part of day to run test(s) for: default is 0 for both",
        "type": int,
        "default": 0,
    },
    {
        "name": ["-t", "--test"],
        "help": "test info to use: default is 0 for all",
        "type": int,
        "default": 0,
    },
]


def cmd_view(args):
    """ view detailed information about Advent of Code Days """
    Days(AOC_DIR).View(args.day)


cmd_view.spec = [
    {
        "name": ["-d", "--day"],
        "help": "day to view information about: default is -1 for latest",
        "type": int,
        "default": -1,
    }
]


class SubParsersAction(argparse._SubParsersAction):
    """ set subcommand value on the argparse namespace """

    def __call__(self, parser, namespace, values, option_string):
        namespace.command = values[0]
        return super().__call__(parser, namespace, values, option_string)


parser = argparse.ArgumentParser("Advent of Code command-line tool")
parser.subparsers = parser.add_subparsers(
    title="Command", action=SubParsersAction, required=True
)


def attach_command_spec(name, parser):
    cmd_fn = globals()[f"cmd_{name}"]
    cmd_parser = parser.add_parser(name, help=cmd_fn.__doc__)

    for arg in cmd_fn.spec:
        name = arg.pop("name")
        cmd_parser.add_argument(*name, **arg)
        arg["name"] = name


attach_command_spec("list", parser.subparsers)
attach_command_spec("new", parser.subparsers)
attach_command_spec("run", parser.subparsers)
attach_command_spec("test", parser.subparsers)
attach_command_spec("view", parser.subparsers)


def main():
    if len(sys.argv) < 2:
        parser.print_help()
        exit(1)

    args = parser.parse_args(sys.argv[1:])
    fn_name = f"cmd_{args.command}"
    globals()[fn_name](args)


if __name__ == "__main__":
    main()
