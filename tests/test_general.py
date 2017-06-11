from __future__ import unicode_literals
from cycli.main import split_queries_on_semicolons


def _file_to_list(file):
  return [x.strip() for x in file.split('\n') if x.strip()]


def test_file():
  file = '''
  MATCH (n) RETURN n;
  MATCH (n) SET n.name = 'Nicole';
  '''

  assert split_queries_on_semicolons(file) == _file_to_list(file)


def test_file_with_semicolon_in_quote_1():
  file = '''
  MATCH (n) SET n.name = 'Nicole; White';
  MATCH (n) RETURN n;
  MATCH (n) RETURN n;
  '''

  assert split_queries_on_semicolons(file) == _file_to_list(file)


def test_file_with_semicolon_in_quote_2():
  file = '''
  MATCH (n) RETURN n;
  MATCH (n) SET n.name = 'Nicole; White';
  MATCH (n) RETURN n;
  '''

  assert split_queries_on_semicolons(file) == _file_to_list(file)


def test_file_with_semicolon_in_quote_3():
  file = '''
  MATCH (n) RETURN n;
  MATCH (n) RETURN n;
  MATCH (n) SET n.name = 'Nicole; White';
  '''

  assert split_queries_on_semicolons(file) == _file_to_list(file)