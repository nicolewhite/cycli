import requests
from py2neo import Graph

graph = Graph()

reltypes = list(graph.relationship_types)
labels = list(graph.node_labels)

r = requests.get("http://localhost:7474/db/data/propertykeys")
props = r.json()

neo4j_words = reltypes + labels + props