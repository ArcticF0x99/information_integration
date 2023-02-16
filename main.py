from strsimpy.normalized_levenshtein import NormalizedLevenshtein
from strsimpy.jaro_winkler import JaroWinkler
from strsimpy.jaccard import Jaccard
import numpy as np

mediated_schema = ['name', 'publisher', 'genre', 'language', 'platform',
          'price', 'sales count', 'release date']

source1 = ['appid', 'name', 'developer', 'publisher', 'score_rank',
           'owners', 'average_forever', 'average_2weeks', 'median_forever',
           'median_2weeks', 'ccu', 'price', 'initialprice', 'discount', 'tags', 'languages', 'genre']


source2full = ['aliases', 'api_detail_url', 'characters', 'concepts', 'date_added', 'date_last_updated', 'deck',
               'description', 'developers', 'expected_release_day', 'expected_release_month', 'expected_release_quarter',
               'expected_release_year', 'first_appearance_characters', 'first_appearance_concepts', 'first_appearance_locations',
               'first_appearance_objects', 'first_appearance_people', 'franchises', 'genres', 'guid', 'id', 'image', 'images',
               'image_tags', 'killed_characters', 'locations', 'name', 'number_of_user_reviews', 'objects', 'original_release_date',
               'people', 'platforms', 'publishers', 'releases', 'dlcs', 'reviews', 'similar_games', 'site_detail_url', 'themes', 'videos']

source2short = ['developers', 'franchises', 'genres', 'name', 'original_release_date', 'platforms', 'publishers', 'releases', 'themes']


normalized_levensthein = NormalizedLevenshtein()
jaro_winkler = JaroWinkler()
# k shingle -> set of k words
jaccard = Jaccard(3)

def get_similarities(schema, data_source):
    similarity_pairs = []

    for schema_field in schema:
        field = {
            'schema_field': schema_field,
            'matching_pairs': []
        }

        for source_field in data_source:
            matching_pair = {
                'source_field': source_field,
                'similarities': []
            }

            similarity_jaro = jaro_winkler.similarity(schema_field, source_field)
            similarity_jaccard = jaccard.similarity(schema_field, source_field)
            similarity_lev = normalized_levensthein.similarity(schema_field, source_field)

            matching_pair['similarities'] = [similarity_jaro, similarity_jaccard, similarity_lev]
            field['matching_pairs'].append(matching_pair)

        similarity_pairs.append(field)

    return similarity_pairs


def get_best_matchings(similarity_pairs, combination_strat='max', threshold=0.7):
    matchings = []

    for sim_pair in similarity_pairs:
        highest_sim_value = 0
        best_match_field = ''
        sim_value_indices = None
        sim_method = 'average'

        for matching_pair in sim_pair['matching_pairs']:
            sim_value = None

            if combination_strat == 'max':
                sim_value = max(matching_pair['similarities'])
            elif combination_strat == 'min':
                sim_value = min(matching_pair['similarities'])
            elif combination_strat == 'avg':
                sim_value = sum(matching_pair['similarities']) / len(matching_pair['similarities'])

            if sim_value > highest_sim_value:
                highest_sim_value = sim_value
                best_match_field = matching_pair['source_field']

                if combination_strat != 'avg':
                    sim_value_indices = np.where(np.array(matching_pair['similarities']) == sim_value)[0]

        if highest_sim_value < threshold:
            highest_sim_value = 0
            best_match_field = ''
            sim_method = ''
        else:
            if sim_value_indices is not None:
                sim_method = ''

                for index in sim_value_indices:
                    if index == 0:
                        sim_method += ', jaro_winkler'
                    elif index == 1:
                        sim_method += ', jaccard'
                    elif index == 2:
                        sim_method += ', normalized_levensthein'

                sim_method = sim_method.removeprefix(', ')

        matchings.append({
            'schema_field': sim_pair['schema_field'],
            'source_field': best_match_field,
            'sim_value': highest_sim_value,
            'sim_method': sim_method
        })

    return matchings


def print_matchings(matchings, combination_strat, threshold):
    print('combination_strategy: ' + str(combination_strat) + ' | threshold: ' + str(threshold))

    for match in matchings:
        print('schema_field: ' + str(match['schema_field']) + ' | source_field: ' + str(match['source_field']) +
              ' | sim_value: ' + str(match['sim_value']) + ' | sim_method: ' + str(match['sim_method']))

    print('\n')


def schema_matching(schema, data_source, combination_strat='max', threshold=0.7, should_print_matchings=False):
    similarity_pairs = get_similarities(schema, data_source)
    matchings = get_best_matchings(similarity_pairs, combination_strat, threshold)

    if should_print_matchings:
        print_matchings(matchings, combination_strat, threshold)

    return matchings

def schema_matching_multiple_data_sources(schema, data_sources, combination_strategy='max', threshold=0.7, should_print_matchings=False):
    best_matchings = []

    for source in data_sources:
        matchings = schema_matching(schema, source, combination_strategy, threshold)

        if len(best_matchings) == 0:
            best_matchings = matchings
        else:
            for i in range(0, len(best_matchings)):
                if matchings[i]['sim_value'] > best_matchings[i]['sim_value']:
                    best_matchings[i] = matchings[i]

        if should_print_matchings:
            print_matchings(matchings, combination_strategy, threshold)

    return best_matchings


if __name__ == '__main__':
  # schema_matching(mediated_schema, source1)
  # schema_matching(mediated_schema, source2short)
  schema_matching_multiple_data_sources(mediated_schema, [source1, source2short], 'max', 0.7, True)





