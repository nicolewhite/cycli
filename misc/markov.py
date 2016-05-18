from cycli.cypher import Cypher
from misc.graphgist import get_all_queries
import re

cypher = Cypher()

queries = get_all_queries()

# Each Cypher word is a state in the Markov model. We're also adding a "" state; this means there are no previous words
# (we're at the beginning of the query).
cypher_words = [""] + cypher.words()

# Store the model in a dictionary of dictionaries.
markov = {i: {j:0.0 for j in cypher_words} for i in cypher_words}

for query in queries:
    # Find the indices of Cypher functions and keywords separately. This results in a list of tuples for each word and its
    # index, e.g. [('MATCH', 0), ('WHERE', 13), ('RETURN', 29)].

    function_indices = []

    for word in cypher.FUNCTIONS:
        idx = [m.start() for m in re.finditer(" " + word + "\s+\(", query, re.IGNORECASE)]

        for i in idx:
            function_indices.append((word, i))

    # Find the keywords. Make sure they're surrounded by spaces so that we don't grab words within words.
    keyword_indices = []

    for word in cypher.KEYWORDS:
        idx = [m.start() for m in re.finditer(" " + word + " ", query, re.IGNORECASE)]

        for i in idx:
            keyword_indices.append((word, i))

    # Combine the indexes of the functions and keywords.
    indices = function_indices + keyword_indices

    # Sort the words by the order of their indexes, i.e. the order in which they were found in the query.
    indices.sort(key=lambda tup: tup[1])

    # Drop the indexes so that we just have a list of words ordered by their position in the query.
    indices = [x[0] for x in indices]

    # Append the empty string state to the beginning; this state means there are no previous keywords.
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

    if denominator == 0:
        # Absorbing state.
        markov[key] = {i: 1.0 if i == key else 0.0 for i in value.keys()}
    else:
        markov[key] = {i:j / denominator for i, j in value.items()}

# Convert dictionaries to list of tuples so that they can be stored in order.
for word in markov.keys():
    ordered = sorted(markov[word].items(), key=lambda x:x[1], reverse=True)
    markov[word] = ordered

# Write the Markov model to a file.
with open("markov.txt", "w") as file:
    file.write(repr(markov))
