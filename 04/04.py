#!/usr/bin/env python3

import re
import string

class Passport:

    FIELDS = {
        "byr": "Birth Year",
        "iyr": "Issue Year",
        "eyr": "Expiration Year",
        "hgt": "Height",
        "hcl": "Hair Color",
        "ecl": "Eye Color",
        "cid": "Country ID",
        "pid": "Passpord Color",
    }
    OPTIONAL_FIELDS = ["cid"]

    def __init__(self, data):
        self.data = dict()
        fields = data.split()

        for field in fields:
            key, value = field.split(":", 1)

            if hasattr(self, key):
                getattr(self, key)(value)
            else:
                self.data[key] = value

    def __getitem__(self, item):
        return self.data[item]

    def __repr__(self):
        return ", ".join([f"({key}: {self.data[key]})" for key in self.FIELDS if key in self.data])
        #return " ".join([f"{key}: {self.data[key]}" for key in self.data])

    def IsValid(self, strict=True):
        check_fields = [field for field in self.FIELDS if field not in self.OPTIONAL_FIELDS]

        if strict:
            check = [(self.data[f"{field}_valid"] if field in self.data else False) for field in check_fields]
        else:
            check = [(field in self.data) for field in check_fields]

        if check.count(True) >= len(check_fields):
            return True
        else:
            return False

    def byr(self, value):
        year = self.data["byr"] = int(value)

        if len(value) != 4:
            self.data["byr_valid"] = False
        else:
            if year < 1920 or year > 2002:
                self.data["byr_valid"] = False
            else:
                self.data["byr_valid"] = True

    def eyr(self, value):
        year = self.data["eyr"] = int(value)

        if len(value) != 4:
            self.data["eyr_valid"] = False
        else:
            if year < 2020 or year > 2030:
                self.data["eyr_valid"] = False
            else:
                self.data["eyr_valid"] = True

    def iyr(self, value):
        year = self.data["iyr"] = int(value)

        if len(value) != 4:
            self.data["iyr_valid"] = False
        else:
            if year < 2010 or year > 2020:
                self.data["iyr_valid"] = False
            else:
                self.data["iyr_valid"] = True

    def hgt(self, value):
        match = re.match("^(?P<value>[0-9]*)(?P<unit>.*)$", value)
        value = self.data["hgt"] = int(match["value"])
        unit = self.data["hgt_unit"] = match["unit"]

        if unit == "in":
            if value < 59 or value > 76:
                self.data["hgt_valid"] = False
            else:
                self.data["hgt_valid"] = True

        elif unit == "cm":
            if value < 150 or value > 193:
                self.data["hgt_valid"] = False
            else:
                self.data["hgt_valid"] = True

        else:
            self.data["hgt_valid"] = False

    def hcl(self, value):
        hex_str = value.strip("#")
        self.data["hcl"] = hex_str

        if value[0] != "#" or len(hex_str) != 6:
            self.data["hcl_valid"] = False
        else:
            self.data["hcl_valid"] = True

            for char in hex_str:
                if not char in string.hexdigits:
                    self.data["hcl_valid"] = False
                    break

    def ecl(self, value):
        self.data["ecl"] = value
        if value in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            self.data["ecl_valid"] = True
        else:
            self.data["ecl_valid"] = False

    def pid(self, value):
        self.data["pid"] = value

        if len(value) != 9:
            self.data["pid_valid"] = False
        else:
            self.data["pid_valid"] = False
            try:
                int(value)
                self.data["pid_valid"] = True

            except Exception as error:
                raise


with open("input.txt", "r") as openfile:
    data = openfile.read()

passport_strs = []
passport_str = ""

for line in data.split("\n"):
    if line == "":
        passport_strs.append(passport_str)
        passport_str = ""
        continue
    passport_str += " " + line

passports = [Passport(passport_str) for passport_str in passport_strs]
valid = [passport.IsValid() for passport in passports]
print(valid.count(True))

