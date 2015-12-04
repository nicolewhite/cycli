from py2neo import Graph, authenticate, Unauthorized
from py2neo.packages.httpstream import SocketError, http
from datetime import datetime
from cycli.table import pretty_print_table


class AuthError(Exception):
    pass


class ConnectionError(Exception):
    pass


class Py2neoClient(object):

    def __init__(self, host, port, username=None, password=None, ssl=False, timeout=None):
        if timeout:
            http.socket_timeout = timeout

        host_port = "{host}:{port}".format(host=host, port=port)
        uri = "{scheme}://{host_port}/db/data/".format(scheme="https" if ssl else "http",
                                                       host_port=host_port)
        if username and password:
            authenticate(host_port, username, password)
        self.graph = Graph(uri)
        try:
            self.neo4j_version = self.graph.neo4j_version
        except Unauthorized:
            raise AuthError(uri)
        except SocketError:
            raise ConnectionError(uri)

    def cypher(self, statement, parameters):
        error = False
        start = datetime.now()
        tx = self.graph.cypher.begin()

        try:
            tx.append(statement, parameters)
            results = tx.process()
            tx.commit()
        except KeyboardInterrupt:
            tx.rollback()
            results = ""
            error = True
        except Exception as e:
            results = e
            error = True

        end = datetime.now()
        duration = int(round((end - start).total_seconds() * 1000))

        return {"results": results, "duration": duration, "error": error}

    def labels(self):
        return sorted(self.graph.resource.resolve("labels").get().content)

    def relationship_types(self):
        return sorted(self.graph.resource.resolve("relationship/types").get().content)

    def constraints(self):
        return sorted(self.graph.resource.resolve("schema/constraint").get().content)

    def indexes(self):
        return sorted(self.graph.resource.resolve("schema/index").get().content)

    def property_keys(self):
        return sorted(self.graph.resource.resolve("propertykeys").get().content)


class Neo4j:

    Client = Py2neoClient

    __relationship_types = None
    __labels = None
    __constraints = None
    __indexes = None

    parameters = {}

    def __init__(self, host, port, username=None, password=None, ssl=False, timeout=None):
        self.__client = self.Client(host, port, username, password, ssl, timeout)

    def cypher(self, query):
        return self.__client.cypher(query, self.parameters)

    def labels(self):
        if not self.__labels:
            self.__labels = self.__client.labels()
        return self.__labels

    def relationship_types(self):
        if not self.__relationship_types:
            self.__labels = self.__client.relationship_types()
        return self.__relationship_types

    def constraints(self):
        if not self.__constraints:
            self.__constraints = self.__client.constraints()
        return self.__constraints

    def indexes(self):
        if not self.__indexes:
            self.__indexes = self.__client.indexes()
        return self.__indexes

    def update_parameters(self, key, value):
        self.parameters[key] = value

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
        return self.__client.property_keys()
