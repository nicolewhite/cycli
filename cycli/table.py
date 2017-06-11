def pretty_table(headers, rows):
  """
  :param headers: A list, the column names.
  :param rows: A list of lists, the row data.
  """

  if not all([len(headers) == len(row) for row in rows]):
    return "Incorrect number of rows."

  rows = [[stringify(s) for s in row] for row in rows]
  headers = [stringify(s) for s in headers]

  widths = col_widths(headers, rows)

  top = [x.ljust(widths[i]) for i, x in enumerate(headers)]
  separator = ["-" * widths[i] for i in range(len(headers))]

  rest = []

  for item in rows:
    row = []
    for i, x in enumerate(item):
      if isnumeric(x):
        row.append(x.rjust(widths[i]))
      else:
        row.append(x.ljust(widths[i]))

    rest.append(row)

  top = " | ".join(top)
  separator = "-+-".join(separator)
  rest = [" | ".join(r) for r in rest]

  top += "\n"
  separator += "\n"
  rest = "\n".join(rest)

  return top + separator + rest + "\n"

def col_widths(headers, rows):
  l = [headers] + rows
  transpose = [list(x) for x in zip(*l)]
  return [len(max(x, key=len)) for x in transpose]

def isnumeric(s):
  for c in s:
    if not c.isdigit() and c != ".":
      return False

  return s.count(".") < 2

def stringify(s):
  if s is None:
      return ""

  try:
    unicode
  except NameError:
    return str(s)
  else:
    if isinstance(s, unicode):
      return s.encode("utf8")

  return str(s)
