import requests
from py2neo import Graph, authenticate
from datetime import datetime


class Neo4j:

    def __init__(self, host, port, username=None, password=None, ssl=False):
        self.username = username
        self.password = password

        self.protocol = "https://" if ssl else "http://"
        self.host_port = "{host}:{port}".format(host=host, port=port)
        self.url = "{protocol}{host_port}/db/data/".format(protocol=self.protocol, host_port=self.host_port)

    def connect(self):
        if self.username and self.password:
            authenticate(self.host_port, self.username, self.password)

        graph = Graph(self.url)
        self.graph = graph

    def cypher(self, query):
        start = datetime.now()
        tx = self.graph.cypher.begin()

        try:
            tx.append(query)
            results = tx.process()
            tx.commit()
        except Exception as e:
            results = e
        except KeyboardInterrupt:
            tx.rollback()
            results = ""

        end = datetime.now()
        duration = int(round((end - start).total_seconds() * 1000))

        return results, duration

    def labels(self):
        return sorted(list(self.graph.node_labels))

    def relationship_types(self):
        return sorted(list(self.graph.relationship_types))

    def properties(self):
        url = self.url + "propertykeys"
        r = requests.get(url, auth=(self.username, self.password))
        props = r.json()
        return sorted(props)
