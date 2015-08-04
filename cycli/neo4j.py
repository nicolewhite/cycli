import requests
from py2neo import Graph, authenticate


class Neo4j:

    def __init__(self, host, port, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        self.host_port = "{host}:{port}".format(host=host, port=port)
        self.url = "http://{host_port}/db/data/".format(host_port=self.host_port)

    def connection(self):
        if self.username and self.password:
            authenticate(self.host_port, self.username, self.password)

        graph = Graph(self.url)
        return graph

    def cypher(self, query):
        try:
            results = self.connection().cypher.execute(query)
        except Exception as e:
            results = e

        return results

    def labels(self):
        return sorted(list(self.connection().node_labels))

    def relationship_types(self):
        return sorted(list(self.connection().relationship_types))

    def properties(self):
        url = self.url + "propertykeys"
        r = requests.get(url, auth=(self.username, self.password))
        props = r.json()
        return sorted(props)