import re
import sys
import names
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
            t.write(f"DROP TABLE IF EXISTS `{file}`;\n")
            t.write("/*!40101 SET @saved_cs_client   = @@character_set_client */;\n")
            t.write("/*!40101 SET character_set_client = utf8 */;\n")
            t.write(f"CREATE TABLE {table} (" + "\n")
            for col, dtype in col_data.items():
                t.write(f"{col} {''.join(dtype)}" + "\n")
            t.write(") ENGINE=InnoDB CHARSET=latin1 COLLATE=latin1_swedish_ci;" + "\n")
            t.write("/*!40101 SET character_set_client = @saved_cs_client */;\n")
    except FileNotFoundError:
        print("Unexpected error: file not found. Aborting.")
        sys.exit()

    return col_data
    

def fillTable(file, table, columns):
    row_data = {}
         
    def checkType(dtype, inputList):
        #if dtype == 'varchar':
        #if dtype == 'int': inputList = [int(x) for x in inputList]
        #if dtype == 'decimal':
        #if dtype == 'date': 
        pass

        #return inputList

    print(f"Enter a reasonable number or rows in {table}")
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
        print("Please enter the values you would like to have:")
        inputList = input().split()
        row_data[key] = checkType(columns[key][0], inputList)

    ## After the dict has been filled with the values and validated, we can fill the actual table data with random values
    ## add the bottom base and call it a day. We can worry about the primary and foreign keys later. I hope I can ALTER TABLE later.
        


## Maybe a function to append a bottom base as well?
