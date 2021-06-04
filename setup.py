#!/usr/bin/env python3.9

import sys

from setuptools import setup
from Cython.Build import cythonize


def main():
    if not list_contains(list(sys.argv), ["build_ext", "--inplace"]):
        print("ERROR: Args must contain `build_ext` and `--inplace` in that order.")
        return 1

    setup(
        ext_modules=cythonize("fluids/simulator.pyx")
    )
    return 0


def list_contains(bigger_list, smaller_list):
    if len(bigger_list) < len(smaller_list):
        return False

    for i in range(len(bigger_list) - len(smaller_list) + 1):
        slice = bigger_list[i:i+len(smaller_list)]
        print(slice)
        if slice == smaller_list:
            return True
    else:
        return False


if __name__ == "__main__":
    exit(main())
