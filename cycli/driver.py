from datetime import datetime
from cycli.table import pretty_table
from py2neo import Graph, Unauthorized, remote
from py2neo.packages.httpstream import SocketError, http


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


def sort_dict_by_key(d, key):
  return sorted(d, key=lambda k: k[key])


class Neo4j:
  labels = None
  relationship_types = None
  property_keys = None
  constraints = None
  indexes = None

  parameters = {}

  def __init__(self, host, port, username=None, password=None, ssl=False, timeout=None, bolt=None):
    if timeout is not None:
      http.socket_timeout = timeout

    host_port = "{host}:{port}".format(host=host, port=port)
    uri = "{scheme}://{host_port}/db/data/".format(scheme="https" if ssl else "http", host_port=host_port)

    self.graph = Graph(uri, user=username, password=password, bolt=bolt, secure=ssl)

    try:
      self.neo4j_version = self.graph.dbms.kernel_version
    except Unauthorized:
      raise AuthError(uri)
    except SocketError:
      raise ConnectionError(uri)

  def cypher(self, statement):
    error = False
    headers = []
    rows = []

    start = datetime.now()
    tx = self.graph.begin()

    try:
      result = tx.run(statement, self.parameters)
      headers = list(result.keys())
      rows = [[x[header] for header in headers] for x in result]
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

  def get_labels(self):
    if not self.labels:
      self.labels = sorted(self.graph.node_labels)
    return self.labels

  def get_relationship_types(self):
    if not self.relationship_types:
      self.relationship_types = sorted(self.graph.relationship_types)
    return self.relationship_types

  def get_property_keys(self):
    if not self.property_keys:
      self.property_keys = sorted(remote(self.graph).resolve("propertykeys").get().content)
    return self.property_keys

  def get_constraints(self):
    if not self.constraints:
      data = remote(self.graph).resolve("schema/constraint").get().content
      self.constraints = sort_dict_by_key(data, "label")
    return self.constraints

  def get_indexes(self):
    if not self.indexes:
      data = remote(self.graph).resolve("schema/index").get().content
      self.indexes = sort_dict_by_key(data, "label")
    return self.indexes

  def update_parameters(self, key, value):
    self.parameters[key] = value

  def refresh(self):
    self.labels = None
    self.relationship_types = None
    self.property_keys = None
    self.indexes = None
    self.constraints = None
    self.get_labels()
    self.get_relationship_types()
    self.get_property_keys()
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
