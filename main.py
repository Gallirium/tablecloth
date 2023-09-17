import re
import os
import sys
import names
import gentable

def main():

    print("Enter filename:")
    filename = names.enterName(True)
    print("Enter table name:")
    tablename = names.enterName()
    print("Please enter a reasonable number of columns.")

    ## We don't want to generate large tables.
    while True:
        try:
            COLS = int(input())
            if COLS <= 0:
                print("The number you entered is negative. What do you expect me to do?")
            elif COLS > 10: 
                print("That's too many. There should be ten or less columns.")
            else:
                print("")
                break
        except ValueError:
            print("Could not interpret input as a numeric value. Please try again.")

    columns = gentable.genTable(filename, tablename, COLS)
    gentable.fillTable(filename, tablename, columns)
    names.bottomBase(filename)

main()
