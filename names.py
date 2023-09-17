import re
import os
import sys
SPECIAL_REGEX = r'\`|\~|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\+|\=|\[|\{|\]|\}|\||\\|\'|\<|\,|\.|\>|\?|\/|\""|\;|\:|\s'

## Function for validating names. Only accepts the name if there are no special chars in it.
def enterName(isFile=False):
    while True:
        name = str(input())
        notValid = re.search(SPECIAL_REGEX, name)
        if notValid:
            print("Your name has special chars in it.")
            print("Please try again.")
        else:
            break

## delete system32
    if isFile:
        compare_names = [f.startswith(name) for f in os.listdir(".")]
        if any(compare_names):
            print(f"There is already a similar file that starts with these chars in the directory.")
            print("Aborting for safety reasons...")
            sys.exit()
        else:
            print(f"Creating file {name}.sql in {os.getcwd()}")
            with open(name + ".sql", 'w') as t, open('topBase.sql', 'r') as top_base:
                for line in top_base:
                    t.write(line)
                t.write("\n")
    return name

def bottomBase(name):
    with open(name + ".sql", 'a') as t, open('bottomBase.sql', 'r') as bottom_base:
        for line in bottom_base:
            t.write(line)
        t.write("\n")

