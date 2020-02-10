import json
import csv
import requests
import sys

# returns a list of attributes.
def parseRow0(row):
    rowStr = ",".join(row)
    index = 0 ;
    prev = None
    row_list = []
    while index < len(rowStr):
        char = rowStr[index]
        if char == "'" and prev == None:
            prev = index;
        elif char == "'" and rowStr[index - 1] != "\\":
            row_list.append(rowStr[prev+1:index])
            prev = None
        elif char == "N":
            if rowStr[index: index + 4] == "NULL":
                row_list.append("NULL")
                index += 4
                continue
        index += 1
    return row_list

# adds the attributes to object list with appropriate column name
def addRowToTableObjectList(values, columns, obj):
    if len(values) != len(columns):
        print(str(values) + "\n")
        print(str(columns) + "\n")
        print("values and columns do not match length\n")
        return
    insertObject = {}
    for index in range(len(values)):
        insertObject[columns[index]] = values[index]
    obj.append(insertObject)

def transform_attribute_into_list(attribute):
    attribute = attribute.lower()
    attributes = attribute.split(" ")
    return [''.join(char for char in string if char.isalnum()) for string in attributes]


def add_attributes_to_inverted_index(attributes, columns, table, primary_key, inverted_index):
    if len(attributes) != len(columns):
        print(str(attributes) + "\n")
        print(str(columns) + "\n")
        print("attributes and columns do not match length\n")
        return
    
    primary_key_value = None

    for index in range(len(attributes)):
        column = columns[index]
        attribute = attributes[index]
        if column == primary_key:
            primary_key_value = attribute

    for index in range(len(attributes)):
        column = columns[index]
        attribute = attributes[index]
        modified_attribute_list = transform_attribute_into_list(attribute)
        table_locations = None
        for modified_attribute in modified_attribute_list:
            # empty strings
            if modified_attribute == '':
                break;
            if modified_attribute in inverted_index:
                table_locations = inverted_index[modified_attribute]
            else:
                table_locations = []
            location_in_table = {"TABLE": table, "COLUMN": column, "PRIMARY": primary_key, "PRIMARY_VALUE":primary_key_value}
            table_locations.append(location_in_table)
            inverted_index[modified_attribute] = table_locations


def load_country(inverted_index):
    csvfile = open('country.csv', 'r',  encoding="latin1")
    firebaseURL = "https://inf551-experimental.firebaseio.com/country.json"
    tablename = "country"
    primary_key = "Code"
  
    readCSV = csv.reader(csvfile, delimiter=',')
    columns = None
    tableObjectList = []
    for index, row in enumerate(readCSV):
        if index > 0:
            attributes = parseRow0(row)
            add_attributes_to_inverted_index(attributes, columns, tablename, primary_key, inverted_index) 
            addRowToTableObjectList(attributes, columns, tableObjectList)

        else:
            rowStr = ",".join(row)
            newrow = rowStr.split(", ")
            columns = [''.join(e for e in string if e.isalnum()) for string in newrow]
    
    x = requests.put(firebaseURL, data=json.dumps(tableObjectList))
    csvfile.close()

def load_city(inverted_index):
    csvfile = open('city.csv', 'r',  encoding="latin1")
    firebaseURL = "https://inf551-experimental.firebaseio.com/city.json"
    tablename = "city"
    primary_key = "ID"
  
    readCSV = csv.reader(csvfile, delimiter=',')
    columns = None
    tableObjectList = []
    for index, row in enumerate(readCSV):
        if index > 0:
            attributes = parseRow0(row)
            add_attributes_to_inverted_index(attributes, columns, tablename, primary_key, inverted_index) 
            addRowToTableObjectList(attributes, columns, tableObjectList)

        else:
            rowStr = ",".join(row)
            newrow = rowStr.split(", ")
            columns = [''.join(e for e in string if e.isalnum()) for string in newrow]
    
    x = requests.put(firebaseURL, data=json.dumps(tableObjectList))
    csvfile.close()

def load_countrylanguage(inverted_index):
    csvfile = open('countrylanguage.csv', 'r',  encoding="latin1")
    firebaseURL = "https://inf551-experimental.firebaseio.com/countrylanguage.json"
    tablename = "countrylanguage"
    primary_key = "Language"
  
    readCSV = csv.reader(csvfile, delimiter=',')
    columns = None
    tableObjectList = []
    for index, row in enumerate(readCSV):
        if index > 0:
            attributes = parseRow0(row)
            add_attributes_to_inverted_index(attributes, columns, tablename, primary_key, inverted_index) 
            addRowToTableObjectList(attributes, columns, tableObjectList)

        else:
            rowStr = ",".join(row)
            newrow = rowStr.split(", ")
            columns = [''.join(e for e in string if e.isalnum()) for string in newrow]
    
    x = requests.put(firebaseURL, data=json.dumps(tableObjectList))
    csvfile.close()

def upload_inverted_index(inverted_index):
    firebaseURL = "https://inf551-experimental.firebaseio.com/index.json"
    x = requests.put(firebaseURL, data=json.dumps(inverted_index))


def load_databases(args):
    inverted_index = {}
    for arg in args:
        if arg == "city.csv":
            load_city(inverted_index)
            print("Loading city")
        elif arg == "country.csv":
            load_country(inverted_index)
            print("loading country")
        elif arg == "countrylanguage.csv":
            load_countrylanguage(inverted_index)
            print("loading country language")
    upload_inverted_index(inverted_index)
        

if __name__ == "__main__":
    load_databases(sys.argv)

###################################################################### extras



def load_country2():
    csvfile = open('country.csv', 'r',  encoding="utf8")
    txt = open('country_out.txt', 'w',  encoding="utf8")
    firebaseURL = "https://inf551-experimental.firebaseio.com/country.json"
  
    readCSV = csv.reader(csvfile, delimiter=',')
    columns = None
    tableObjectList = []
    for index, row in enumerate(readCSV):
        if index > 0:
            attributes = parseRow(row)
            txt.write(str(attributes) + "\n")
            addRowToTableObjectList(attributes, columns, tableObjectList)
        else:
            rowStr = ",".join(row)
            newrow = rowStr.split(", ")
            columns = [''.join(e for e in string if e.isalnum()) for string in newrow]
    #x = requests.put(firebaseURL, data=json.dumps(tableObjectList))
    txt.close()
    csvfile.close()

# replaces values with appropriate values.
def replaceVal(value):
    if value == ', NULL, ':
        return 'NULL'
    return value.replace('\\"', "\\'")

# returns a list of attributes.
def parseRow(row):
    rowStr = ",".join(row)
    rowStr = rowStr[1:-1]
    # value will be replaced back in replaceVal
    rowStr = rowStr.replace("\\'", '\\"')
    newrow = rowStr.split("'")
    return [replaceVal(value) for value in newrow if (value != ', ')]
