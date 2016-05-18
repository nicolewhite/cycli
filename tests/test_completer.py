from __future__ import unicode_literals
import pytest
from prompt_toolkit.completion import Completion
from prompt_toolkit.document import Document

@pytest.fixture
def completer():
    from cycli.completer import CypherCompleter
    return CypherCompleter(
        labels=["Movie", "Person", "Under_Score", "Spa Ce"],
        relationship_types=["ACTED_IN", "DIRECTED", "SPA CE"],
        properties=["name", "title", "under_score", "spa ce"]
    )

@pytest.fixture
def complete_event():
    from mock import Mock
    return Mock()

def get_completions(completer, complete_event, text):
    position = len(text)

    return list(completer.get_completions(
        Document(text=text, cursor_position=position),
        complete_event))

def test_empty_string_completion(completer, complete_event):
    text = ""
    result = get_completions(completer, complete_event, text)
    assert result == []

def test_label_completion(completer, complete_event):
    text = "MATCH (p:P"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="Person", start_position=-1)]

def test_label_completion_after_rel(completer, complete_event):
    text = "MATCH (p:Person)-[:ACTED_IN]->(m:M"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="Movie", start_position=-1)]

def test_label_completion_with_backticks(completer, complete_event):
    text = "MATCH (p:`P"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="Person", start_position=-1)]

def test_label_completion_with_underscores(completer, complete_event):
    text = "MATCH (u:Under_S"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="Under_Score", start_position=-7)]

def test_label_completion_with_backticks_and_spaces(completer, complete_event):
    text = "MATCH (s:`Spa C"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="Spa Ce", start_position=-5)]

def test_label_completion_with_backticks_and_underscores(completer, complete_event):
    text = "MATCH (u:`Under_S"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="Under_Score", start_position=-7)]

def test_rel_completion(completer, complete_event):
    text = "MATCH (p:Person)-[:A"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="ACTED_IN", start_position=-1)]

def test_rel_completion_with_backticks(completer, complete_event):
    text = "MATCH (p:Person)-[:`A"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="ACTED_IN", start_position=-1)]

def test_rel_completion_with_underscores(completer, complete_event):
    text = "MATCH (p:Person)-[:ACTED_I"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="ACTED_IN", start_position=-7)]

def test_rel_completion_with_backsticks_and_spaces(completer, complete_event):
    text = "MATCH (p:Person)-[`:SPA C"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="SPA CE", start_position=-5)]

def test_rel_completion_with_backticks_and_underscores(completer, complete_event):
    text = "MATCH (p:Person)-[:`ACTED_I"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="ACTED_IN", start_position=-7)]

def test_rel_completion_inside_function(completer, complete_event):
    text = "MATCH (p:Person) RETURN p.name, SIZE((p)-[:a"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="ACTED_IN", start_position=-1)]

def test_property_completion(completer, complete_event):
    text = "MATCH (p:Person) WHERE p.n"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="name", start_position=-1)]

def test_property_completion_with_backticks(completer, complete_event):
    text = "MATCH (p:Person) WHERE p.`n"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="name", start_position=-1)]

def test_property_completion_with_underscores(completer, complete_event):
    text = "MATCH (p:Person) WHERE p.under_s"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="under_score", start_position=-7)]

def test_property_completion_with_backticks_and_underscores(completer, complete_event):
    text = "MATCH (p:Person) WHERE p.`under_s"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="under_score", start_position=-7)]

def test_property_completion_with_backticks_and_spaces(completer, complete_event):
    text = "MATCH (p:Person) WHERE p.`spa c"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="spa ce", start_position=-5)]

def test_no_property_completion_in_float(completer, complete_event):
    text = "RETURN 5."
    result = get_completions(completer, complete_event, text)
    assert result == []

def test_no_property_completion_in_float_after_export(completer, complete_event):
    text = "export k=5."
    result = get_completions(completer, complete_event, text)
    assert result == []

def test_no_cypher_completions_after_non_alpha(completer, complete_event):
    text = "MATCH p WHERE p.name ="
    result = get_completions(completer, complete_event, text)
    assert result == []

def property_completion_in_identifier_with_number(completer, complete_event):
    text = "MATCH (p1:Person) WHERE p1."
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="name", start_position=0), Completion(text="title", start_position=0)]

def test_no_completions_while_inside_string(completer, complete_event):
    text = "MATCH (p:Person) WHERE p.name = 'Tom H"
    result = get_completions(completer, complete_event, text)
    assert result == []

def test_match_keyword_completion(completer, complete_event):
    text = "MAT"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="MATCH", start_position=-3)]

def test_nested_function_completion(completer, complete_event):
    text = "MATCH n RETURN length(col"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="collect", start_position=-3)]

def test_lower_camel_case_functions(completer, complete_event):
    text = "MATCH p = allS"
    result = get_completions(completer, complete_event, text)
    assert result == [Completion(text="allShortestPaths", start_position=-4)]

def test_markov_w_after_match(completer, complete_event):
    # Out of the words starting with W, WHERE is most commonly used after MATCH.
    text = "MATCH n W"
    result = get_completions(completer, complete_event, text)
    assert result[0] == Completion(text="WHERE", start_position=-1)

def test_markov_w_after_case(completer, complete_event):
    # Out of the words starting with W, WHEN is most commonly used after CASE.
    text = "MATCH n RETURN CASE W"
    result = get_completions(completer, complete_event, text)
    assert result[0] == Completion(text="WHEN", start_position=-1)

def test_markov_w_after_nothing(completer, complete_event):
    # Out of the words starting with W, WITH is most commonly the first word in a query.
    text = "W"
    result = get_completions(completer, complete_event, text)
    assert result[0] == Completion(text="WITH", start_position=-1)

def test_markov_m_after_nothing(completer, complete_event):
    # Out of the words starting with M, MATCH and MERGE are most commonly the first words in a query, in that order.
    text = "M"
    result = get_completions(completer, complete_event, text)
    assert result[0] == Completion(text="MATCH", start_position=-1)
    assert result[1] == Completion(text="MERGE", start_position=-1)

def test_markov_a_after_where(completer, complete_event):
    # Out of the words starting with A, AND is most commonly used after WHERE.
    text = "MATCH (p:Person) WHERE p.born > 1950 A"
    result = get_completions(completer, complete_event, text)
    assert result[0] == Completion(text="AND", start_position=-1)

def test_markov_a_after_return(completer, complete_event):
    # Out of the words starting with A, AS is most commonly used after RETURN.
    text = "MATCH (p:Person) RETURN p.name A"
    result = get_completions(completer, complete_event, text)
    assert result[0] == Completion(text="AS", start_position=-1)
