from cycli.cypher import FUNCS, KEYWORDS, cypher_words
from misc.graphgist import get_all_queries
import json

queries = get_all_queries()

# Each Cypher word is a state in the Markov model. We're also adding a "" state; this means there are no previous words
# (we're at the beginning of the query).
cypher_words = [""] + cypher_words

# Store the model in a dictionary of dictionaries.
markov = {i: {j:0 for j in cypher_words} for i in cypher_words}

for query in queries:
    # Find the functions. This will miss cases where people put a space between the function and the open
    # parenthesis, e.g. LENGTH ([1,2,3]), but oh well.
    # This results in a tuple for each word and its index, e.g. ("RETURN", 5).
    function_indices = [(word, query.find(" " + word + "(")) for word in FUNCS]

    # Find the keywords. Make sure they're surrounded by spaces so that we don't grab words within words.
    keyword_indices = [(word, query.find(" " + word + " ")) for word in KEYWORDS]

    # Combine the indexes of the functions and keywords.
    indices = function_indices + keyword_indices

    # Only keep words that were found. If a word wasn't found, its index will be -1.
    indices = [x for x in indices if x[1] > -1]

    # Sort the words by the order of their indexes, i.e. the order in which they were found in the query.
    indices.sort(key=lambda tup: tup[1])

    # Drop the indexes so that we just have a list of words ordered by their position in the query.
    indices = [x[0] for x in indices]

    # Append an empty string to the beginning; this state means there are no previous keywords.
    indices = [""] + indices

    for i in range(len(indices) - 1):
        keyword = indices[i]
        next_keyword = indices[i + 1]

        # Build the Markov model. Given that the previous keyword is keyword[i], find the probability that the next keyword is
        # keyword[j].
        markov[keyword][next_keyword] += 1

# Divide each value in a row by the sum of all the values in the row to convert to a probability.
for key, value in markov.items():
    denominator = sum(value.values())

    if denominator > 0:
        markov[key] = {i:j / denominator for i, j in value.items()}

# Write the Markov model to a json file.
with open("markov.json", "w") as file:
    json.dump(markov, file)
