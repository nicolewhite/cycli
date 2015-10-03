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
        error = False
        start = datetime.now()
        tx = self.graph.cypher.begin()

        try:
            tx.append(query)
            results = tx.process()
            tx.commit()
        except Exception as e:
            results = e
            error = True
        except KeyboardInterrupt:
            tx.rollback()
            results = ""
            error = True

        end = datetime.now()
        duration = int(round((end - start).total_seconds() * 1000))

        return {"results": results, "duration": duration, "error": error}

    def labels(self):
        if not self.__labels:
            labels_resource = Resource(self.graph.uri.string + "labels")
            self.__labels = sorted(list(frozenset(labels_resource.get().content)))

        return self.__labels

    def relationship_types(self):
        if not self.__relationship_types:
            relationship_types_resource = Resource(self.graph.uri.string + "relationship/types")
            self.__relationship_types = sorted(list(frozenset(relationship_types_resource.get().content)))

        return self.__relationship_types

    def constraints(self):
        if not self.__constraints:
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
        if not self.__indexes:
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
        rows = [[x] for x in self.format_constraints_indexes(constraints)]

        pretty_print_table(headers, rows)

    def print_indexes(self):
        headers = ["Indexes"]
        indexes = self.indexes()
        rows = [[x] for x in self.format_constraints_indexes(indexes)]

        pretty_print_table(headers, rows)

    def format_constraints_indexes(self, values):
        return [":{}({})".format(value["label"], ",".join(value["property_keys"])) for value in values]

    def print_schema(self):
        headers = ["Labels", "Relationship Types", "Constraints", "Indexes"]

        columns = [self.labels()[:]]
        columns.append(self.relationship_types()[:])
        columns.append(self.format_constraints_indexes(self.constraints()[:]))
        columns.append(self.format_constraints_indexes(self.indexes()[:]))

        max_length = len(max(columns, key=len))
        [x.extend([""] * (max_length - len(x))) for x in columns]
        rows = [[x[i] for x in columns] for i in range(max_length)]

        pretty_print_table(headers, rows)

    def properties(self):
        url = self.url + "propertykeys"
        r = requests.get(url, auth=(self.username, self.password))
        props = r.json()
        return sorted(props)