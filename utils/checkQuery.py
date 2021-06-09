from os import stat
import re


class checkQuery:
    @staticmethod
    def check_valid(email):
        regex = "^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$"
        # pass the regular expression
        # and the string in search() method
        if re.search(regex, email):
            print("Valid Email")

        else:
            print("Invalid Email")
