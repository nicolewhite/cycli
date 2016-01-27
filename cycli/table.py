def pretty_table(headers, rows):
    """
    :param headers: A list, the column names.
    :param rows: A list of lists, the row data.
    """

    rows = [[stringify(s) for s in row] for row in rows]

    if not all([len(headers) == len(row) for row in rows]):
        return "Incorrect number of rows."

    columns = [[headers[i]] + [row[i] for row in rows] for i in range(len(headers))]
    widths = [len(max(l, key=len)) for l in columns]

    top = [x.ljust(widths[i]) for i, x in enumerate(headers)]
    separator = ["-" * widths[i] for i in range(len(headers))]
    rest = [[x.ljust(widths[i]) for i, x in enumerate(item)] for item in rows]

    top = " | ".join(top)
    separator = "-+-".join(separator)
    rest = [" | ".join(r) for r in rest]

    top += "\n"
    separator += "\n"
    rest = "\n".join(rest)

    return top + separator + rest + "\n"

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
