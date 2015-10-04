from unittest import TestCase, main
from cycli.cypher import Cypher

cypher = Cypher()

class TestReadOnly(TestCase):
    def test_delete(self):
        query = "MATCH n DELETE n"
        self.assertTrue(cypher.is_a_write_query(query))

    def test_merge(self):
        query = "MERGE n RETURN n"
        self.assertTrue(cypher.is_a_write_query(query))

    def test_remove(self):
        query = "MATCH n REMOVE n:Label"
        self.assertTrue(cypher.is_a_write_query(query))

    def test_set(self):
        query = "MATCH n SET n.name = 'Hello'"
        self.assertTrue(cypher.is_a_write_query(query))

    def test_drop(self):
        query = "DROP CONSTRAINT ON"
        self.assertTrue(cypher.is_a_write_query(query))

    def test_create(self):
        query = "CREATE n"
        self.assertTrue(cypher.is_a_write_query(query))

    def test_identifier(self):
        query = "MATCH (asset:Something) RETURN asset"
        self.assertFalse(cypher.is_a_write_query(query))

    def test_node_label(self):
        query = "MATCH (a:Asset) RETURN a"
        self.assertFalse(cypher.is_a_write_query(query))

    def test_rel_type(self):
        query = "MATCH (p:Person)-[:DELETE]->(m:Movie) RETURN p, m"
        self.assertFalse(cypher.is_a_write_query(query))

    def test_double_quotes(self):
        query = 'MATCH n WHERE n.name = " DELETE ME " RETURN n'
        self.assertFalse(cypher.is_a_write_query(query))

    def test_single_quotes(self):
        query = "MATCH n WHERE n.name = ' DELETE SET REMOVE ' RETURN n"
        self.assertFalse(cypher.is_a_write_query(query))

    def test_back_ticks(self):
        query = "MATCH n WHERE n.`delete set match remove` = 'Tom' RETURN n"
        self.assertFalse(cypher.is_a_write_query(query))

if __name__ == "__main__":
  main()