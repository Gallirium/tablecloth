import re
import sys
import random
import names
import datetime
SUPPORTED_TYPES = set(['varchar', 'int', 'decimal', 'date'])

## Function for validating types according to SQL restrictions.
## This does NOT validate the values that are inserted into the table.
def validateType():
    while True:
        dt = str(input())
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

                return ["varchar", str(size)]
            
            elif dt.lower() == 'int':
                return ["int"]

            elif dt.lower() == 'decimal':
                print("Enter the precision value.")
                while True:
                    try:
                        precision = int(input())
                        if precision <= 0 or precision > 38:
                            print("The number you entered is either too large for decimal precision (>38), or negative. Or a zero.")
                            print("Enter a different value.")
                        else:
                            print("")
                            break
                    except ValueError:
                        print("Could not interpret input as a numeric value. Please try again.")
                
                print("Enter the scale value (digits after the decimal point).")
                while True:
                    try:
                        scale = int(input())
                        if scale <= 0 or scale > precision:
                            print("The number you entered is either negative or greater than your precision. Or a zero.")
                            print("Enter a different value.")
                        else:
                            print("")
                            break
                    except ValueError:
                        print("Could not interpret input as a numeric value. Please try again.")
            
                return ["decimal", str(precision), str(scale)]
            
            elif dt.lower() == 'date':
                return ["date"]

def genTable(file, table, columns):
    col_data = {}
    print("Please enter the names and data types. Supported types are as follows: VARCHAR, INT, DECIMAL, DATE")
    for i in range(columns):
        print(f"Name of column {i+1}:")
        while True:
            name = names.enterName()
            if name in col_data.keys():
                print("This column already exists in the table. Please enter a different name.")
            else:
                print("")
                break

        print("Enter data type:")
        col_data[name] = validateType()

    try:
        with open(file + ".sql", 'a') as t:
            ##FIX: not the name of the file, but the name of the table!!
            t.write(f"DROP TABLE IF EXISTS `{file}`;\n")
            t.write("/*!40101 SET @saved_cs_client   = @@character_set_client */;\n")
            t.write("/*!40101 SET character_set_client = utf8 */;\n")
            t.write(f"CREATE TABLE `{table}` (" + "\n")
            
            for col, dtype in list(col_data.items())[:-1]:
                if len(dtype) == 1:
                    t.write(f"`{col}` {dtype[0]}," + "\n")
                else:
                    t.write(f"`{col}` {dtype[0] + '(' + ','.join(dtype[1:]) + ')'}," + "\n")
            
            col, dtype = list(col_data.items())[-1]
            if len(dtype) == 1:
                t.write(f"`{col}` {dtype[0]}" + "\n")
            else:
                t.write(f"`{col}` {dtype[0] + '(' + ','.join(dtype[1:]) + ')'}" + "\n")
            t.write(") ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;" + "\n")
            t.write("/*!40101 SET character_set_client = @saved_cs_client */;\n\n\n")
    except FileNotFoundError:
        print("Unexpected error: file not found. Aborting.")
        sys.exit()
    print(col_data)
    return col_data
    

def fillTable(file, table, columns):
    row_data = {}
    
    ## This actually attempts to validate the data.
    def checkTypes(dtype):
        while True:
            inputList = input().split()

            if dtype[0] == 'varchar':
                l = int(dtype[1])
                for el in inputList:
                    if len(el) > l:
                        print("At least one of your strings is longer than what you specified. Try again.")
                        break
                else:
                    inputList = ["'" + el + "'" for el in inputList]
                    break

            if dtype[0] == 'int':
                INT_MIN = -2**32/2
                INT_MAX = 2**32/2-1
                for el in inputList:
                    try:
                        el = int(el)
                        if el > INT_MAX or el < INT_MIN:
                            print("The integer is too large. Why do you need these numbers for a test database? Try again.")
                            break
                    except ValueError:
                        print("That's not an integer. Try again.")
                        break
                else: break

            if dtype[0] == 'decimal':
                for num in inputList:
                    try:
                        m = repr(float(num)).split('.')
                        if len(m) == 1:
                            pr = map(len, m)
                            sc = 0
                        else:
                            pr, sc = map(len, m)
                        if m[0][0] == '-':
                            pr -= 1
                        if pr + sc > int(dtype[1]) or sc > int(dtype[2]):
                            print("The number you entered won't work: out of range. Try again.")
                            break
                    except ValueError:
                        print("One of the numbers you entered is wrong.")
                        break
                else: break

            if dtype[0] == 'date':
                for dat in inputList:
                    try:
                        datetime.date.fromisoformat(dat)
                    except ValueError:
                        print("The date you entered appears to be wrong. Try again.")
                        break
                else:
                    inputList = ["'" + el + "'" for el in inputList]
                    break
        
        return inputList

    print(f"Enter a reasonable number or rows in {table}:")
    while True:
        try:
            ROWS = int(input())
            if ROWS <= 0:
                print("The number is negative. I swear, what is it with you?")
            elif ROWS > 50:
                print("That's more than enough.")
                print("Enter a different value.")
            else:
                print("")
                break
        except ValueError:
            print("Could not interpret as numeric value. Please try again.")

    for key in columns.keys():
        print(f"Please enter the values for {key} (type {columns[key][0]}), separated by spaces:")
        row_data[key] = checkTypes(columns[key])
    print(row_data)

    ##Write the damn data to the file!!
    with open(file + '.sql', 'a') as t:
        t.write(f"LOCK TABLES `{table}` WRITE;\n")
        t.write(f"/*40000 ALTER TABLE `{table}` DISABLE KEYS */;\n")
        t.write(f"INSERT INTO `{table}` VALUES\n")

        l = list(row_data.keys())
        for _ in range(ROWS-1):
            t.write("(")
            for i in range(len(l[:-1])):
                t.write(random.choice(row_data[l[i]]))
                t.write(",")
            t.write(random.choice(row_data[l[-1]]))
            t.write("),\n")
        
        t.write("(")
        for i in range(len(l[:-1])):
            t.write(random.choice(row_data[l[i]]))
            t.write(",")
        t.write(random.choice(row_data[l[-1]]))
        t.write(");\n")


        t.write(f"/*40000 ALTER TABLE `{table}` ENABLE KEYS */;\n")
        t.write("UNLOCK TABLES;\n\n\n")

    ## After the dict has been filled with the values and validated, we can fill the actual table data with random values
    ## add the bottom base and call it a day. We can worry about the primary and foreign keys later. I hope I can ALTER TABLE later.
        


## Maybe a function to append a bottom base as well?
