import requests
from py2neo import Graph, authenticate, Resource
from datetime import datetime
from cycli.table import pretty_print_table


class Neo4j:

    __relationship_types = None
    __labels = None
    __constraints = None
    __indexes = None

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
        if self.__labels is None:
            # directly query from resource - as py2neo does caching of node_labels
            labels_resource = Resource(self.graph.uri.string + "labels")
            self.__labels = sorted(list(frozenset(labels_resource.get().content)))
        return self.__labels

    def relationship_types(self):
        if self.__relationship_types is None:
            # directly query from resource - as py2neo does caching of relationship_types
            relationship_types_resource = Resource(self.graph.uri.string + "relationship/types")
            self.__relationship_types = sorted(list(frozenset(relationship_types_resource.get().content)))
        return self.__relationship_types

    def constraints(self):
        if self.__constraints is None:
            constraints = []
            constraints_resource = Resource(self.graph.uri.string + "schema/constraint")
            constraints_content = list(constraints_resource.get().content)
            for i in constraints_content:
                constraint = dict(i)
                constraint["property_keys"] = list(constraint["property_keys"])
                constraints.append(constraint)

            self.__constraints = constraints
        return self.__constraints

    def indexes(self):
        if self.__indexes is None:
            indexes = []
            for label in self.labels():
                index_resource = Resource(self.graph.uri.string + "schema/index/" + label)
                indexes_content = list(index_resource.get().content)
                for i in indexes_content:
                    index = dict(i)
                    index["property_keys"] = list(index["property_keys"])
                    indexes.append(index)

            self.__indexes = indexes
        return self.__indexes

    # when schema changes - user can call refresh
    def refresh(self):
        self.__labels = None
        self.__relationship_types = None
        self.__indexes = None
        self.__constraints = None
        self.labels()
        self.relationship_types()
        self.indexes()
        self.constraints()

    def print_labels(self):
        headers = ["Labels"]
        rows = [[x] for x in self.labels()]

        pretty_print_table(headers, rows)

    def print_relationship_types(self):
        headers = ["Relationship Types"]
        rows = [[x] for x in self.relationship_types()]

        pretty_print_table(headers, rows)

    def print_constraints(self):
        headers = ["Constraints"]
        constraints = self.constraints()
        rows = [[":{}({})".format(value["label"], ",".join(value["property_keys"]))] for value in constraints]

        pretty_print_table(headers, rows)

    def print_indexes(self):
        headers = ["Indexes"]
        indexes = self.indexes()
        rows = [[":{}({})".format(value["label"], ",".join(value["property_keys"]))] for value in indexes]

        pretty_print_table(headers, rows)

    def print_schema(self):
        self.print_labels()
        self.print_relationship_types()
        self.print_indexes()
        self.print_constraints()

    def properties(self):
        url = self.url + "propertykeys"
        r = requests.get(url, auth=(self.username, self.password))
        props = r.json()
        return sorted(props)