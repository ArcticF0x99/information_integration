from strsimpy import NormalizedLevenshtein, Jaccard
from Levenshtein import distance
from jellyfish import jaro_winkler
from nltk.metrics import jaccard_distance



def function(name, developer):
    print("Hello")


if __name__ == '__main__':
    normalized_levenshtein = NormalizedLevenshtein()
    jaccard = Jaccard(2)
    # print(normalized_levenshtein.distance('Name', 'Name'))
    print(1 - jaccard.distance('Name', 'Name'))



#list of strings (ordered, items can be accessed by index)
source1 = ["appid", "name", "developer", "publisher", "score_rank",
           "owners", "average_forever", "average_2weeks", "median_forever",
           "median_2weeks", "ccu", "price", "initialprice", "discount", "tags", "languages", "genre"]

#dictionary with key as string, and value as lists of string, values can be accessed by using the keys
schema = {
    "game": ["Name", "Publisher", "Genre", "Language"],
    "platform_release": ["Platform", "Price", "Date", "Sales Count"],
    "platform": ["Name", "Release Date"]
}


#looping through the values of the schema dictionary
#each value find the closest match in source1 using Levenshtein distance
#then add that match to a new dictionary "mapped_schema"
def map_schemas(source1, schema):
    mapped_schema = {}
    #iterate through each key-value pair of the schema dictionary
    #items() is a method that returns a list of key-value pairs (tuples) from the schema dictionary
    for table_name, fields in schema.items():
        mapped_fields = []
        for field in fields:
            closest_match = min(source1, key=lambda x: distance(x.lower(), field.lower()))
            mapped_fields.append(closest_match)
        mapped_schema[table_name] = mapped_fields
    return mapped_schema
def map_schemas(source1, schema):
    mapped_schema = {}
    for table_name, fields in schema.items():
        mapped_fields = []
        for field in fields:
            #replace min with max function for Jaro Winkler
            closest_match = max(source1, key=lambda x: jaro_winkler(x.lower(), field.lower()))
            mapped_fields.append(closest_match)
        mapped_schema[table_name] = mapped_fields
    return mapped_schema

def map_schemas(source1, schema):
    mapped_schema = {}
    for table_name, fields in schema.items():
        mapped_fields = []
        for field in fields:
            closest_match = max(source1, key=lambda x: jaccard_distance(set(x.lower()), set(field.lower())))
            mapped_fields.append(closest_match)
        mapped_schema[table_name] = mapped_fields
    return mapped_schema

result=map_schemas(source1, schema)
print("Jaro Winkler :" )
print(result)
print("")

result=map_schemas(source1, schema)
#new dictionary with the same keys as the schema dictionary
#values are the closest match from source1 for each value in the schema dictionary
print("Normalized Levenshtein :" )
print(result)
print("")

result=map_schemas(source1, schema)
print("Jaccard distance :" )
print(result)



