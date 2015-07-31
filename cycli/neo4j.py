from py2neo import Graph

graph = Graph()

reltypes = list(graph.relationship_types)
labels = list(graph.node_labels)

props = []

for label in labels:
    query = "MATCH (n:{}) RETURN n LIMIT 1;".format(label)
    n = graph.cypher.execute_one(query)

    if not n:
        continue

    props.extend(n.properties.keys())

props = list(set(props))

words = reltypes + labels + props