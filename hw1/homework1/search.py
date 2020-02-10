import json
import csv
import requests
import sys

# keyword is a string
# results_str is a str
# results is a dictionary[keyword] -> sorted primary keys by table
def parse_and_add_to_results(keyword, results_str, results):
    table_dict = {}
    if keyword in results:
        table_dict = results[keyword]

    # list_of_results is a list of occurances in all tables.
    list_of_results = json.loads(results_str) 
    for result_dict in list_of_results:
        table = result_dict["TABLE"]
        primary_key = result_dict["PRIMARY"]
        primary_value = result_dict["PRIMARY_VALUE"]
        
        primary_key_list = []
        if primary_key in table_dict:
            primary_key_list = table_dict[primary_key]
        primary_key_list.append(primary_value)

        table_dict[primary_key] = primary_key_list

    results[keyword] = table_dict

def sort_and_remove_duplicates_in_list(primary_key_list):
    sorted_by_frequency = sorted(primary_key_list,key=primary_key_list.count,reverse=True)

    seen = set()
    seen_add = seen.add
    removed_duplicates =  [x for x in sorted_by_frequency if not (x in seen or seen_add(x))]
    print(removed_duplicates)
    return removed_duplicates

# sorts the primary keys in the different tables and also removes duplicates.
def sort_and_remove_duplicates_in_results(results):
    for key in results:
        table_dict = results[key]
        for primary_key in table_dict:
            primary_key_list = table_dict[primary_key]
            primary_key_list = sort_and_remove_duplicates_in_list(primary_key_list)
            table_dict[primary_key] = primary_key_list

def search_for_keyword(keyword, results):
    firebaseURL = "https://inf551-experimental.firebaseio.com/index/" + str(keyword) + ".json"
    response = requests.get(firebaseURL)

    if response.text == "null":
        return
    parse_and_add_to_results(keyword, response.text, results)
    sort_and_remove_duplicates_in_results(results)
    #print(results)



def search_databases(args):
    results = {}
    for arg in args[1:]:
        search_for_keyword(arg, results)

if __name__ == "__main__":
    search_databases(sys.argv)
