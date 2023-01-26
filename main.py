from strsimpy import NormalizedLevenshtein, Jaccard

def function(name, developer):
    print("Hello")


if __name__ == '__main__':
    normalized_levenshtein = NormalizedLevenshtein()
    jaccard = Jaccard(2)
    # print(normalized_levenshtein.distance('Name', 'Name'))
    print(1 - jaccard.distance('Name', 'Name'))

