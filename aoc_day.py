import argparse
import importlib
import os
import re
import subprocess
import sys
import time


def UninitializedError(day):
    print(f"The specified Advent of Code Day ({day}) has not been initialized")
    exit(2)


class _FileInterface:

    PROJECT_FILES = {
        "input": "^(?P<filename>input)\.(?P<extension>txt)$",
        "readme": "^(?P<filename>README)\.(?P<extension>md)$",
        "run": (
            "^(?P<filename>part|puzzle|[0-5]{1,3})"
            "_?"
            "(?P<number>[0-9]+)?"
            "\."
            "(?P<extension>py)$"
        ),
        "solution": "^(?P<filename>solution)_?(?P<number>[0-9]+)?\.(?P<extension>txt)$",
        "test": "^(?P<filename>test)_?(?P<number>[0-9]+)?\.(?P<extension>txt)$",
    }

    @staticmethod
    def Attach(day_obj, filename):
        path = os.path.join(day_obj.path, filename)
        if os.path.isdir(path):
            raise ValueError(
                f"Unable to attach a file interface to a directory: {path}"
            )

        match = None
        for day_filetype in _FileInterface.PROJECT_FILES:
            match = re.match(
                _FileInterface.PROJECT_FILES[day_filetype], filename.strip()
            )
            if match:
                break

        if not match:
            raise ValueError(
                f"Unable to match provided path to a project filetype: {path}"
            )

        obj = _FileInterface(day_filetype, day_obj.path, path)
        if day_filetype in ["input", "readme"]:
            setattr(day_obj, f"{day_filetype}_", obj)
        else:
            index = int(match.group("number")) if match.group("number") else 0
            getattr(day_obj, f"{day_filetype}_")[index] = obj

    def __init__(self, day_filetype, basedir, filepath):
        self.dir = basedir
        self.path = filepath
        self.type_ = day_filetype

        self.data = None
        self.lines = []
        if os.path.exists(filepath):
            self._read()

    def __call__(self, *args, **kwargs):
        if self.type_ in ["input", "test"]:
            return iter(self.lines)
        elif self.type_ == "readme":
            print(self.data)
            return
        elif self.type_ == "run":
            return self._run(*args, **kwargs)
        elif self.type_ == "solution":
            self._write(*args, **kwargs)

    def __iter__(self):
        return iter(self.lines)

    def __getitem__(self, index):
        return self.lines[index]

    def __len__(self):
        return len(self.lines)

    def __str__(self):
        return self.data.strip()

    def _read(self):
        with open(self.path, "r") as openfile:
            self.data = openfile.read()
        self.lines = self.data.split("\n")

    def _run(self, data, **kwargs):
        spec = importlib.util.spec_from_file_location("run", self.path)
        module = importlib.util.module_from_spec(spec)

        sys.path.append(self.dir)
        spec.loader.exec_module(module)
        sys.path.pop()

        for attr in kwargs:
            setattr(module, attr, kwargs[attr])

        return module.solve_puzzle(data)

    def _write(self, data):
        if data:
            if not isinstance(data, str):
                data = str(data)

            with open(self.path, "w") as openfile:
                openfile.write(data)
                if data[-1] != "\n":
                    openfile.write("\n")


class _AttachFile:

    PROJECT_FILES = {
        "input": "^(?P<filename>input)\.(?P<extension>txt)$",
        "readme": "^(?P<filename>README)\.(?P<extension>md)$",
        "run": (
            "^(?P<filename>part|puzzle|[0-5]{1,3})"
            "_?"
            "(?P<number>[0-9]+)?"
            "\."
            "(?P<extension>py)$"
        ),
        "solution": "^(?P<filename>solution)_?(?P<number>[0-9]+)?\.(?P<extension>txt)$",
        "test": "^(?P<filename>test)_?(?P<number>[0-9]+)?\.(?P<extension>txt)$",
    }

    def __init__(self, obj, filename):
        self.path = os.path.join(obj.path, filename)
        if os.path.isdir(self.path):
            raise ValueError(self.path)

        match = None
        for filetype in self.PROJECT_FILES:
            match = re.match(self.PROJECT_FILES[filetype], filename.strip())
            if match:
                fn = getattr(obj, f"_set_{filetype}")
                fn(self, match)
                break

        if not match:
            raise ValueError(self.path)

    @property
    def data(self):
        with open(self.path, "r") as openfile:
            data = openfile.read().strip()
        return data


class InputData:
    def __init__(self, data):
        self.data = data
        self.path = data.path
        self.tokens = data.data.split("\n")

    def __iter__(self):
        return iter(self.tokens)

    def __str__(self):
        return self.data.data

    @property
    def lines(self):
        return len(self.tokens)


class RunSolution:
    def __init__(self, data):
        self.path = data.path
        self.spec = importlib.util.spec_from_file_location("run", self.path)
        self.module = importlib.util.module_from_spec(self.spec)

    def __call__(self, day):
        self.module.input_data = day.input_
        self.module.test_data = day.test_

        sys.path.append(day.path)
        self.spec.loader.exec_module(self.module)
        sys.path.pop()

        return self.module.solve_puzzle(day.input_)


class Solution:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return self.data.data

    def __call__(self, value):
        with open(self.data.path, "w") as openfile:
            openfile.write(value + "\n")


class Day(int):

    SUFFIX_MAP = {
        1: "st",
        2: "nd",
        3: "rd",
        None: "th",
    }

    def __new__(cls, aoc_dir, day_str):
        obj = super().__new__(cls, int(day_str))
        obj.day = int(day_str)

        obj.path = os.path.join(aoc_dir, day_str)
        if not os.path.exists(obj.path):
            obj._init_state()

        obj.year = int(os.path.basename(aoc_dir)[-4:])

        try:
            obj.suffix = obj.SUFFIX_MAP[int(day_str[-1])]
        except KeyError:
            obj.suffix = obj.SUFFIX_MAP[None]

        obj._check_state()
        return obj

    def __str__(self):
        return f"December {self.day: >2}{self.suffix}, {self.year}: {self.stars}"

    def _check_state(self):
        self.input_ = None
        self.readme_ = dict()
        self.run_ = dict()
        self.solution_ = dict()
        self.test_ = dict()

        for filename in os.listdir(self.path):
            try:
                # _AttachFile(self, filename)
                _FileInterface.Attach(self, filename)
            except ValueError as error:
                # print(error)
                pass

        # print(self, dir(self))
        # raise NotImplementedError()

    def _init_state(self):
        os.makedirs(self.path)
        for part in ["1", "2"]:
            path = os.path.join(self.path, f"part{part}.py")
            with open(path, "w") as openfile:
                openfile.write(
                    "#!/usr/bin/env python3\n"
                    "\n"
                    "def solve_puzzle(input_data):\n"
                    "   pass\n"
                    "\n"
                )
                os.chmod(path, 0o755)

    @property
    def stars(self):
        return "*" * len(self.solution_)

    def _run(self, part, data):
        solution = self.run_[part](data)

        if part == 0:
            filename = "solution.txt"
        else:
            filename = f"solution{part}.txt"

        # _AttachFile(self, filename)
        _FileInterface.Attach(self, filename)
        start = time.time()
        self.solution_[part](solution)
        end = time.time()
        print("=" * 40)
        print(f" Day {self.day}, Part {part} - Puzzle Input")
        print("-" * 40)
        print(f" Solution: {solution}")
        print(f"  Runtime: {end - start:8.6f}s")

    def _test(self, part, test):
        if test == 0:
            for index in sorted(self.test_):
                start = time.time()
                solution = self.run_[part](self.test_[index])
                end = time.time()
                print("=" * 40)
                print(f" Day {self.day}, Part {part} - Test Input {index}")
                print("-" * 40)
                print(f" Solution: {solution}")
                print(f"  Runtime: {end - start:8.6f}s")
        else:
            start = time.time()
            solution = self.run_[part](self.test_[test])
            end = time.time()
            print("=" * 40)
            print(f" Day {self.day}, Part {part} - Test Input")
            print("-" * 40)
            print(f" Solution: {solution}")
            print(f"  Runtime: {end - start:8.6f}s")

    def Run(self, part=0):
        if part == 0:
            if 0 in self.run_:
                self._run(0, self.input_)
            else:
                self._run(1, self.input_)
                self._run(2, self.input_)
        else:
            self._run(part, self.input_)

    def Test(self, part=0, test=0):
        if part == 0:
            if 0 in self.run_:
                self._test(0, test)
            else:
                self._test(1, test)
                self._test(2, test)
        else:
            self._test(part, test)

    def View(self):
        print("=" * 60)
        print(self)
        print("=" * 60)
        if self.input_:
            print("{0: >14} | {1}".format("Puzzle Input", self.input_.path))
            print("-" * 60)
        if self.test_:
            for key in sorted(self.test_):
                print("{0: >14} | {1}".format(f"Test Data {key}", self.test_[key].path))
            print("-" * 60)
        if self.solution_:
            for key in sorted(self.solution_):
                print("{0: >14} | {1}".format(f"Solution P{key}", self.solution_[key]))
            print("-" * 60)


class Days:
    def __init__(self, aoc_dir):
        self.days = list()
        self.path = aoc_dir
        for filename in sorted(os.listdir(self.path)):
            try:
                self.days.append(Day(aoc_dir, filename))
            except ValueError as error:
                pass

    def __str__(self):
        return "\n".join([str(day) for day in self.days])

    def __getitem__(self, item):
        if item >= len(self.days):
            raise KeyError(item)
        return self.days[item]

    def New(self, day=0):
        if day == 0:
            day = len(self.days) + 1

        self.days.append(Day(self.path, str(day)))
        print("Initialized", self.days[-1])

    def Run(self, day=0, part=0):
        if day == -1:
            self[-1].Run(part)
        elif day == 0:
            for day in self.days:
                day.Run(part)
        else:
            try:
                self[day - 1].Run(part)
            except KeyError:
                UninitializedError(day)

    def Test(self, day=0, part=0, test=0):
        if day == -1:
            self[-1].Test(part, test)
        elif day == 0:
            for day in self.days:
                day.Test(part, test)
        else:
            try:
                self[day - 1].Test(part, test)
            except KeyError:
                UninitializedError(day)

    def View(self, day=0):
        if day == 0:
            self[-1].View()
        else:
            try:
                self[day - 1].View()
            except KeyError:
                UninitializedError(day)
