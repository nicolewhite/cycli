try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

from json import loads
from datetime import datetime

from cycli.table import pretty_table


class AuthError(Exception):
    pass


class ConnectionError(Exception):
    pass


def duration_in_ms(start, end):
    return int(round((end - start).total_seconds() * 1000))


def walk(profile):
    steps = []
    steps.append(profile)

    for child in profile.children:
        for n in walk(child):
            steps.append(n)

    return steps


class Neo4j:

    Client = None

    relationship_types = None
    labels = None
    constraints = None
    indexes = None

    parameters = {}

    def __init__(self, host, port, username=None, password=None, ssl=False, timeout=None):
        self.client = self.Client(host, port, username, password, ssl, timeout)
        self.root = "http://{host}:{port}/".format(host=host, port=port)

    def cypher(self, query):
        return self.client.cypher(query, self.parameters)

    def request_endpoint(self, endpoint):
        data = loads(urlopen(self.root + endpoint).read().decode("utf8"))

        if type(data) is list:
            return sorted(data)

        return data

    def get_labels(self):
        if not self.labels:
            self.labels = self.request_endpoint("db/data/labels")
        return self.labels

    def get_relationship_types(self):
        if not self.relationship_types:
            self.relationship_types = self.request_endpoint("db/data/relationship/types")
        return self.relationship_types

    def get_constraints(self):
        if not self.constraints:
            self.constraints = self.request_endpoint("db/data/schema/constraints")
        return self.constraints

    def get_indexes(self):
        if not self.indexes:
            self.indexes = self.request_endpoint("db/data/schema/indexes")
        return self.indexes

    def get_property_keys(self):
        return self.request_endpoint("db/data/propertykeys")

    def update_parameters(self, key, value):
        self.parameters[key] = value

    def refresh(self):
        self.labels = None
        self.relationship_types = None
        self.indexes = None
        self.constraints = None
        self.get_labels()
        self.get_relationship_types()
        self.get_indexes()
        self.get_constraints()

    def print_labels(self):
        headers = ["Labels"]
        rows = [[x] for x in self.get_labels()]

        print(pretty_table(headers, rows))

    def print_relationship_types(self):
        headers = ["Relationship Types"]
        rows = [[x] for x in self.get_relationship_types()]

        print(pretty_table(headers, rows))

    def print_constraints(self):
        headers = ["Constraints"]
        constraints = self.get_constraints()
        rows = [[x] for x in self.format_constraints_indexes(constraints)]

        print(pretty_table(headers, rows))

    def print_indexes(self):
        headers = ["Indexes"]
        indexes = self.get_indexes()
        rows = [[x] for x in self.format_constraints_indexes(indexes)]

        print(pretty_table(headers, rows))

    def format_constraints_indexes(self, values):
        return [":{}({})".format(value["label"], ",".join(value["property_keys"])) for value in values]

    def print_schema(self):
        headers = ["Labels", "Relationship Types", "Constraints", "Indexes"]

        columns = [self.get_labels()[:]]
        columns.append(self.get_relationship_types()[:])
        columns.append(self.format_constraints_indexes(self.get_constraints()[:]))
        columns.append(self.format_constraints_indexes(self.get_indexes()[:]))

        max_length = len(max(columns, key=len))
        [x.extend([""] * (max_length - len(x))) for x in columns]
        rows = [[x[i] for x in columns] for i in range(max_length)]

        print(pretty_table(headers, rows))

    def print_profile(self, profile):
        planner = profile.arguments["planner"]
        version = profile.arguments["version"]
        runtime = profile.arguments["runtime"]

        print("")
        print("Planner: {}".format(planner))
        print("Version: {}".format(version))
        print("Runtime: {}".format(runtime))
        print("")

        headers = ["Operator", "Estimated Rows", "Rows", "DB Hits", "Variables"]
        rows = []

        for n in reversed(walk(profile)):
            operator = n.operator_type
            estimated_rows = int(n.arguments["EstimatedRows"])
            rows_ = n.arguments["Rows"]
            db_hits = n.arguments["DbHits"]
            variables = n.identifiers

            rows.append([operator, estimated_rows, rows_, db_hits, variables])

        print(pretty_table(headers, rows))

try:
    from neo4j.v1 import GraphDatabase

    class BoltClient(object):

        def __init__(self, host, port, username=None, password=None, ssl=False, timeout=None):
            bolt_uri = "bolt://{host}".format(host=host, port=port)

            if username and password:
                # todo: set auth header
                pass

            driver = GraphDatabase.driver(bolt_uri)
            self.session = driver.session()

        def cypher(self, statement, parameters):
            error = False
            profile = None
            headers = []
            rows = []

            start = datetime.now()
            tx = self.session.begin_transaction()

            try:
                cursor = tx.run(statement, parameters)
                rows = [list(row.values()) for row in cursor.stream()]
                headers = cursor.keys()
                tx.commit()
                profile = cursor.summary.profile
            except KeyboardInterrupt:
                tx.rollback()
                error = ""
            except Exception as e:
                error = e

            end = datetime.now()

            return {
                "headers": headers,
                "rows": rows,
                "duration": duration_in_ms(start, end),
                "error": error,
                "profile": profile
            }

    Neo4j.Client = BoltClient

except ImportError:
    from py2neo import Graph, authenticate, Unauthorized
    from py2neo.packages.httpstream import SocketError, http

    class Py2neoClient(object):

        def __init__(self, host, port, username=None, password=None, ssl=False, timeout=None):
            if timeout is not None:
                http.socket_timeout = timeout

            host_port = "{host}:{port}".format(host=host, port=port)
            uri = "{scheme}://{host_port}/db/data/".format(scheme="https" if ssl else "http", host_port=host_port)

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
            headers = []
            rows = []

            start = datetime.now()
            tx = self.graph.cypher.begin()

            try:
                tx.append(statement, parameters)
                results = tx.process()
                results = results[0]
                headers = results.columns
                rows = [[x[header] for header in headers] for x in results]
                tx.commit()
            except KeyboardInterrupt:
                tx.rollback()
                error = ""
            except Exception as e:
                error = e

            end = datetime.now()

            return {
                "headers": headers,
                "rows": rows,
                "duration": duration_in_ms(start, end),
                "error": error
            }

    Neo4j.Client = Py2neoClient