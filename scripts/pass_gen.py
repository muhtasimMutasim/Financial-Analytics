from lib2to3.pygram import Symbols
import os
import random
import string
import sys
import base64
import hmac
import hashlib
import argparse





parser = argparse.ArgumentParser()
parser.add_argument('-l','--len', type=int, help='Required for length of password.', required=True)
args = parser.parse_args()

symbols = "!@$" * 5
characters = list(string.ascii_letters + string.digits + symbols)


def pass_gen(length: int = 12):
    """ Generate Password. """
    password = [ random.choice(characters) for i in range(0, length)]
    random.shuffle(password)
    return "".join(password)


def main():
    if not args.len:
        raise argparse.ArgumentError()
    length = args.len
    password = pass_gen(length=length)
    print(f"\n\n\t{password}\n\n\n\n")
    



if __name__ == "__main__":
    main()