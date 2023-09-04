import re
import os
import sys
SPECIAL_REGEX = r'\`|\~|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\+|\=|\[|\{|\]|\}|\||\\|\'|\<|\,|\.|\>|\?|\/|\""|\;|\:|\s'
SUPPORTED_TYPES = set(['varchar', 'int', 'decimal', 'date'])

## Function for validating names. Only accepts the name if there are no special chars in it.
def enterName(isFile=False):
    while True:
        name = str(input())
        notValid = re.search(SPECIAL_REGEX, name)
        if notValid:
            print("Please try again.")
        else:
            break

## delete system32
    if isFile:
        compare_names = [f.startswith(name) for f in os.listdir(".")]
        if any(compare_names):
            print(f"There is already a similar file that starts with these chars in the directory.")
            print("Aborting for safety...")
            sys.exit()
        else:
            print(f"Creating file {name}.txt in {os.getcwd()}")
            open(name + ".txt",'a').close()

    return name

## Function for validating types according to SQL restrictions.
## This does NOT validate the values that are inserted into the table.
def validate_type():
    dt = str(input())
    while True:
        if dt.lower() not in SUPPORTED_TYPES:
            print("This is not supported. Please enter a valid type.")
        else:
            if dt.lower() == 'varchar':
                print("Print a number in range from 0 to 255.")
                while True:
                    try:
                        size = int(input())
                        if size <= 0:
                            print("The size you entered is negative. Or zero. Either way, why?.")
                        elif size > 255: 
                            print("That's too many. Go stand in the corner.")
                        else:
                            print("")
                            break
                    except ValueError:
                        print("Could not interpret input as a numeric value. Please try again.")

                return ["varchar", f"({size})"]
            
            elif dt.lower() == 'int':
                return ["int",""]

            elif dt.lower() == 'decimal':
                print("Enter the precision value.")
                while True:
                    try:
                        precision = int(input())
                        if precision < 0 or precision > 38:
                            print("The number you entered is either too large for decimal precision (>38), or negative.")
                            print("Enter a different value.")
                        else:
                            print("")
                            break
                    except ValueError:
                        print("Could not interpret input as a numeric value. Please try again.")
                
                print("Enter the scale value (digits after the decimal point)")
                while True:
                    try:
                        scale = int(input())
                        if scale < 0 or scale > precision:
                            print("The number you entered is either negative or greater than your precision.")
                            print("Enter a different value.")
                        else:
                            print("")
                            break
                    except ValueError:
                        print("Could not interpret input as a numeric value. Please try again.")
            
                return ["decimal",f"({precision},{scale})"]
            
            elif dt.lower() == 'date':
                return ["date",""]


def genTable(file, table, columns):
    col_data = {}
    print("Please enter the names and data types. Supported types are as follows: VARCHAR, INT, DECIMAL, DATE")
    for i in range(columns):
        print(f"Name of column {i+1}:")
        while True:
            name = enterName()
            if name in col_data.keys():
                print("This column already exists in the table. Please enter a different name.")
            else:
                print("")
                break

        print("Enter data type:")
        col_data[name] = validate_type()

    try:
        with open(file + ".txt", 'w') as t:
            t.write(f"CREATE TABLE {table} (" + "\n")
            for col, dtype in col_data.items():
                t.write(f"{col} {''.join(dtype)}" + "\n")
            t.write(")" + "\n")
    except FileNotFoundError:
        print("Unexpected error: file not found. Aborting.")
        sys.exit()

    ##Now for the values themselves
    print("")
    col_values = {}
    for key in col_data:
        print("Type: {key}")
        print(f"Enter the values for column {col_data[key]} separated by spaces, commas, or semicolons: ")
        print("Make sure there aren't too many possible values,")
        if col_data[key][0] == 'varchar':
            strs = re.split("; |, ", str(input()))
        elif col_data[key][0] == 'int':
            print('Range?')
            ##TODO
        elif col_data[key][0] == 'decimal':
            print("Range and increments?")
            ##TODO
        elif col_data[key][0] == 'date':
            print("Enter a valid date delimited by hyphens")
            ##TODO
            
    ##ALSO do something about primary and foreign keys???



def main():

    print("Enter filename:")
    filename = enterName(True)
    print("Enter table name:")
    tablename = enterName()
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

    genTable(filename, tablename, COLS)

    ##fillTable()

main()
