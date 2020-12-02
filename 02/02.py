#!/usr/bin/env python3

import re


class Password(str):
    def __new__(cls, input_str):
        input_str = input_str.strip()

        if len(input_str) == 0:
            raise ValueError("Empty string is not a valid Password")

        match = re.match(
            (
                "^"
                "(?P<min>[0-9]{1,3})"
                "-"
                "(?P<max>[0-9]{1,3})"
                " *"
                "(?P<letter>[a-zA-Z]{1})"
                ":"
                " *"
                "(?P<value>[\w]*)"
                "$"
            ),
            input_str,
        )

        if not match:
            raise ValueError(f"Password format could not be decoded: {input_str}")

        obj = super().__new__(cls, "***")

        obj.is_valid_ = None
        obj.letter_ = match["letter"]
        obj.letter_max_ = int(match["max"])
        obj.letter_min_ = int(match["min"])
        obj.value_ = match["value"]

        return obj

    def _is_valid(self):
        letter1 = self.value_[self.letter_min_ - 1]
        letter2 = self.value_[self.letter_max_ - 1]

        if (letter1 + letter2).count(self.letter_) == 1:
            return True
        else:
            return False

    def _is_valid_old(self):
        count = self.value_.count(self.letter_)
        if count >= self.letter_min_ and count <= self.letter_max_:
            return True
        else:
            return False

    @property
    def IsValid(self):
        if self.is_valid_ is None:
            self.is_valid_ = self._is_valid()
        return self.is_valid_


with open("input.txt", "r") as openfile:
    data = openfile.read()

pwords = [Password(line) for line in data.split("\n") if len(line) > 0]
print(len([pword for pword in pwords if pword.IsValid]))
