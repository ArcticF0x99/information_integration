from strsimpy import NormalizedLevenshtein, Jaccard
import numpy as np
from typing import List, Tuple


def function(name, developer):
    print("Hello")


if __name__ == '__main__':
    normalized_levenshtein = NormalizedLevenshtein()
    jaccard = Jaccard(2)
    # print(normalized_levenshtein.distance('Name', 'Name'))
    print(1 - jaccard.distance('Name', 'Name'))





from strsimpy.normalized_levenshtein import NormalizedLevenshtein

nl = NormalizedLevenshtein()

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

max_distance_pairs = {}

for key, value in schema.items():
    for source in source1:
        max_distance = 0
        max_distance_pair = ("", "")
        for val in value:
            distance = nl.distance(source, val)
            transformed_distance = 1 - distance
            if transformed_distance > max_distance:
                max_distance = transformed_distance
                max_distance_pair = (source, val)
        max_distance_pairs[source] = (max_distance, max_distance_pair)

for key, value in max_distance_pairs.items():
    print(f"The highest transformed distance for {key} is {value[0]} for the pair {value[1]}")




