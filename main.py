from strsimpy.normalized_levenshtein import NormalizedLevenshtein
from strsimpy.jaro_winkler import JaroWinkler
from strsimpy.jaccard import Jaccard


source1 = ["appid", "name", "developer", "publisher", "score_rank",
           "owners", "average_forever", "average_2weeks", "median_forever",
           "median_2weeks", "ccu", "price", "initialprice", "discount", "tags", "languages", "genre"]


source2 = ["platform/hardware", "release_date", "developer", "publisher", "genre", "theme", "freanchise",
"features", "multiplayer_types", "franchises"]

schema = ["Name", "Publisher", "Genre", "Language", "Platform",
          "Price", "Date", "Sales Count", "Name", "Release Date"]

normalized_levensthein = NormalizedLevenshtein()
jaro_winkler = JaroWinkler()

def levenshtein_similarity(schema, data_source):
    best_matches = []
    best_scores = []
    for column in schema:
        max_similarity = 0
        closest_match = ''

        for schema_column in data_source:
            similarity_lev = normalized_levensthein.similarity(column, schema_column)
            similarity_jaro = jaro_winkler.similarity(column, schema_column)
            if similarity > max_similarity:
                max_similarity = similarity
                closest_match = schema_column

        best_matches.append(closest_match)
        best_scores.append(max_similarity)
    return best_matches, best_scores

def jaro_winkler_similarity(schema, data_source):
    max_similarity = 0
    closest_column = ''
    closest_match = ''
    for column in data_source:
        for schema_column in schema:
            similarity = jellyfish.jaro_winkler(column, schema_column)
            if similarity > max_similarity:
                max_similarity = similarity
                closest_column = schema_column
                closest_match = column
    return (closest_match, closest_column, similarity)

def jaccard_similarity(schema, data_source):
    max_similarity = 0
    closest_column = ''
    closest_match = ''
    for column in data_source:
        for schema_column in schema:
            similarity = len(set(column).intersection(schema_column)) / len(set(column).union(schema_column))
            if similarity > max_similarity:
                max_similarity = similarity
                closest_column = schema_column
                closest_match = column
    return (closest_match, closest_column, similarity)



def get_best_match(source1, schema, source2):
    levenshtein_best_match, schema_column1, levenshtein_score = levenshtein_similarity(source1, schema)
    jaro_winkler_best_match, schema_column2, jaro_winkler_score = jaro_winkler_similarity(source1, schema)
    jaccard_best_match, schema_column3, jaccard_score = jaccard_similarity(source1, schema)


    best_match = None
    best_score = 0
    if levenshtein_score > best_score:
        best_match = levenshtein_best_match
        best_score = levenshtein_score
    if jaro_winkler_score > levenshtein_score:
        best_match = jaro_winkler_best_match
        best_score = jaro_winkler_score
    if jaccard_score > jaccard_score:
        best_match = jaccard_best_match
        best_score = jaccard_score


    return best_match, best_score


if __name__ == '__main__':
  """result = get_best_match(source1, schema, source2)
  print(result)"""
  best_matches1, best_score1 = levenshtein_similarity(schema, source1)
  best_matches2, best_score2 = levenshtein_similarity(schema, source2)
  print("hello")





