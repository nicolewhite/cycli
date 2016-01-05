import pytest


@pytest.fixture
def cypher():
    from cycli.cypher import Cypher
    return Cypher()


def test_delete(cypher):
    query = "MATCH n DELETE n"
    assert cypher.is_a_write_query(query)


def test_merge(cypher):
    query = "MERGE n RETURN n"
    assert cypher.is_a_write_query(query)


def test_remove(cypher):
    query = "MATCH n REMOVE n:Label"
    assert cypher.is_a_write_query(query)


def test_set(cypher):
    query = "MATCH n SET n.name = 'Hello'"
    assert cypher.is_a_write_query(query)


def test_drop(cypher):
    query = "DROP CONSTRAINT ON"
    assert cypher.is_a_write_query(query)


def test_create(cypher):
    query = "CREATE n"
    assert cypher.is_a_write_query(query)


def test_identifier(cypher):
    query = "MATCH (asset:Something) RETURN asset"
    assert cypher.is_a_write_query(query) is False


def test_node_label(cypher):
    query = "MATCH (a:Asset) RETURN a"
    assert cypher.is_a_write_query(query) is False


def test_rel_type(cypher):
    query = "MATCH (p:Person)-[:DELETE]->(m:Movie) RETURN p, m"
    assert cypher.is_a_write_query(query) is False


def test_double_quotes(cypher):
    query = 'MATCH n WHERE n.name = " DELETE ME " RETURN n'
    assert cypher.is_a_write_query(query) is False


def test_single_quotes(cypher):
    query = "MATCH n WHERE n.name = ' DELETE SET REMOVE ' RETURN n"
    assert cypher.is_a_write_query(query) is False


def test_back_ticks(cypher):
    query = "MATCH n WHERE n.`delete set match remove` = 'Tom' RETURN n"
    assert cypher.is_a_write_query(query) is False
