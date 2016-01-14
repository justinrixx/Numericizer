#!/usr/bin/python

""" numericizer.py: Numericizes a csv file

    Numericizing is a word I made up that means
    that any non-numerical data will be made
    numerical by this program. I wrote this program
    to standardize csv data sets to prepare them
    for use in machine learning algorithms."""

import sys
import numpy as np


def main(argv):
    # Get the source and destination files

    if len(argv) == 3:
        srcfile = argv[1]
        dstfile = argv[2]
    else:
        srcfile = input("Source Filename: ")
        dstfile = input("Destination Filename: ")

    # read the file into a multidimensional array of strings
    csv = np.genfromtxt(srcfile, delimiter=',', dtype=str)

    columns = csv[0]
    non_numeric_columns = []
    # look for non-numeric columns we need clarification for
    for i, attribute in enumerate(columns):
        non_numeric_columns.append(i)

    sets = []
    # create an empty set for each non-numeric column
    for column in non_numeric_columns:
        sets.append(set())

    # now get all the possible values for the columns in the sets
    for instance in csv:
        for i, column in enumerate(non_numeric_columns):
            sets[i].add(instance[column])

    # next get user clarification
    for i, column in enumerate(non_numeric_columns):

        is_non_numeric = False

        for value in sets[i]:
            if not is_number(value):
                is_non_numeric = True

        if is_non_numeric:
            print("Is there a natural order to these values?")

            for value in sets[i]:
                print(value)

            choice = input("[y/n]")

            change = {}

            # get the user's choice
            if choice.upper() == "Y":
                for value in sets[i]:
                    number = input("Enter a number corresponding to " + value + " ")
                    change[value] = number

            # data with no natural order become negative (-1, -2, -3 ...)
            else:
                for j, value in enumerate(sets[i]):
                    change[value] = -j - 1

            # propagate the request
            for instance in csv:
                for key, value in change.items():
                    if instance[column] == key:
                        instance[column] = value

    # what column is the target in?
    i_target = input("Which column contains the target values (0 indexed please)." +
                     "If the target is in the last column, just press ENTER: ")

    if i_target != "":
        # move the target column to the rightmost position
        # this is a fancy trick I borrowed from stackoverflow
        # http://stackoverflow.com/questions/20265229/rearrange-columns-of-numpy-2d-array
        i_target = int(i_target)
        length = len(csv[0])
        new_positions = np.arange(length)
        for i in range(length):
            if i == length - 1:
                new_positions[i] = i_target
            elif i == i_target:
                new_positions[i] = length - 1
            elif i > i_target:
                new_positions[i] -= 1
                # else do nothing

        csv = csv[:, new_positions]

    # save the file
    np.savetxt(dstfile, csv, delimiter=',', fmt='%s')

    print("Done")


def is_number(s):
    """Determines if a string represents a number
    :param s: The string to check

    Tries to cast the string to a float. If an exception
    is raised, returns false. If not, returns true
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


# This is here to ensure main is only called when
#   this file is run, not just loaded
if __name__ == "__main__":
    main(sys.argv)
