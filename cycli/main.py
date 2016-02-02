from __future__ import unicode_literals, print_function

import sys
import re
import os
import csv
from datetime import datetime

import click
from prompt_toolkit import Application, CommandLineInterface, AbortAction
from prompt_toolkit.buffer import AcceptAction
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import create_prompt_layout, create_eventloop
from prompt_toolkit.styles import PygmentsStyle
from pygments.token import Token

from cycli import __version__
from cycli.lexer import CypherLexer
from cycli.style import CypherStyle
from cycli.completer import CypherCompleter
from cycli.buffer import CypherBuffer
from cycli.binder import CypherBinder
from cycli.driver import Neo4j, AuthError, ConnectionError
from cycli.table import pretty_table
from cycli.cypher import Cypher


def get_tokens(x):
        return [(Token.Prompt, "> ")]


class Cycli:

    def __init__(self, host, port, username, password, logfile, filename, ssl, read_only, timeout):
        self.logfile = logfile
        self.filename = filename
        self.read_only = read_only
        self.neo4j = Neo4j(host, port, username, password, ssl, timeout)
        self.cypher = Cypher()

    def write_to_logfile(self, query, response):
        headers = response["headers"]
        rows = response["rows"]
        duration = response["duration"]
        error = response["error"]

        self.logfile.write("> {}\n".format(query))
        self.logfile.write("{}\n".format(pretty_table(headers, rows)))

        if error is False:
            self.logfile.write("{} ms\n\n".format(duration))

    @staticmethod
    def write_to_csvfile(headers, rows):
        filename = "cycli {}.csv".format(datetime.now().strftime("%Y-%m-%d at %I.%M.%S %p"))

        with open(filename, "wt") as csvfile:
            csvwriter = csv.writer(csvfile, quotechar=str('"'), quoting=csv.QUOTE_NONNUMERIC, delimiter=str(","))
            csvwriter.writerow(headers)

            for row in rows:
                csvwriter.writerow(row)

        csvfile.close()

    def run(self):
        labels = self.neo4j.get_labels()
        relationship_types = self.neo4j.get_relationship_types()
        properties = self.neo4j.get_property_keys()

        if self.filename:
            queries = self.filename.read()
            queries = queries.split(";")[:-1]

            for query in queries:
                query += ";"
                query = query.strip()

                print("> " + query)
                self.handle_query(query)
                print()

            return

        click.secho(" ______     __  __     ______     __         __    ", fg="red")
        click.secho("/\  ___\   /\ \_\ \   /\  ___\   /\ \       /\ \   ", fg="yellow")
        click.secho("\ \ \____  \ \____ \  \ \ \____  \ \ \____  \ \ \  ", fg="green")
        click.secho(" \ \_____\  \/\_____\  \ \_____\  \ \_____\  \ \_\ ", fg="blue")
        click.secho("  \/_____/   \/_____/   \/_____/   \/_____/   \/_/ ", fg="magenta")

        msg = "\nUsing Bolt." if type(self.neo4j.client).__name__ == "BoltClient" else ""

        print(msg)
        print("Version: {}".format(__version__))
        print("Bug reports: https://github.com/nicolewhite/cycli/issues\n")

        completer = CypherCompleter(labels, relationship_types, properties)

        layout = create_prompt_layout(
            lexer=CypherLexer,
            get_prompt_tokens=get_tokens,
            reserve_space_for_menu=8,
        )

        buff = CypherBuffer(
            accept_action=AcceptAction.RETURN_DOCUMENT,
            history=FileHistory(filename=os.path.expanduser('~/.cycli_history')),
            completer=completer,
            complete_while_typing=True,
        )

        application = Application(
            style=PygmentsStyle(CypherStyle),
            buffer=buff,
            layout=layout,
            on_exit=AbortAction.RAISE_EXCEPTION,
            key_bindings_registry=CypherBinder.registry
        )

        cli = CommandLineInterface(application=application, eventloop=create_eventloop())

        try:
            while True:
                document = cli.run()
                query = document.text
                self.handle_query(query)

        except:
            print("Goodbye!")

    def handle_query(self, query):
        run_n = re.match('run-([0-9]+) (.*)', query, re.DOTALL)
        save_csv = query.startswith("save-csv ")

        if self.cypher.is_a_write_query(query) and self.read_only:
            print("Query aborted. You are in read-only mode.")

        elif query in ["quit", "exit"]:
            raise Exception

        elif query == "help":
            print_help()

        elif query == "refresh":
            self.neo4j.refresh()

        elif query == "schema":
            self.neo4j.print_schema()

        elif query == "schema-indexes":
            self.neo4j.print_indexes()

        elif query == "schema-constraints":
            self.neo4j.print_constraints()

        elif query == "schema-labels":
            self.neo4j.print_labels()

        elif query == "schema-rels":
            self.neo4j.print_relationship_types()

        elif query.startswith("env"):
            if query == "env":
                for key, value in self.neo4j.parameters.items():
                    print("{0}={1}".format(key, value))
            else:
                key = query[3:]
                key = key.strip("'\"[]")
                value = self.neo4j.parameters.get(key)

                if value is not None:
                    print(value)

        elif query.startswith("export "):
            if "=" not in query:
                print("Set parameters with export key=value.")
            else:
                params = query.replace("export ", "").strip()
                key, value = params.split("=", 1)
                key = key.strip()
                value = value.strip()

                try:
                    value = eval(value)
                    self.neo4j.update_parameters(key, value)
                except Exception as e:
                    print(e)

        else:
            count = int(run_n.group(1)) if run_n else 1
            query = run_n.group(2) if run_n else query
            query = query[len("save-csv "):] if save_csv else query

            if count <= 0 or not query:
                raise Exception

            total_duration = 0
            index = 0

            while index < count:
                response = self.neo4j.cypher(query)

                headers = response["headers"]
                rows = response["rows"]
                duration = response["duration"]
                error = response["error"]
                profile = response.get("profile")

                if error is False:
                    print(pretty_table(headers, rows))

                    ms = "Run {}: {} ms\n".format(index + 1, duration) if run_n else "{} ms".format(duration)
                    print(ms)

                    if profile:
                        self.neo4j.print_profile(profile)

                    if save_csv:
                        self.write_to_csvfile(headers, rows)
                else:
                    print(error)

                if self.logfile:
                    self.write_to_logfile(query, response)

                total_duration += duration
                index += 1

            if run_n and error is False:
                print("Total duration: {} ms".format(total_duration))


def print_help():
    headers = ["Keyword", "Description"]

    rows = [
        ["quit", "Exit cycli."],
        ["exit", "Exit cycli."],
        ["help", "Display this text."],
        ["refresh", "Refresh schema cache."],
        ["run-n", "Run a Cypher query n times."],
        ["export", "Set a parameter with export key=value."],
        ["save-csv", "Save the query results to a CSV file."],
        ["schema", "Display indexes, constraints, labels, and relationship types."],
        ["schema-indexes", "Display indexes."],
        ["schema-constraints", "Display constraints."],
        ["schema-labels", "Display labels."],
        ["schema-rels", "Display relationship types."],
        ["CTRL-D", "Exit cycli if the input is blank."],
        ["CTRL-C", "Abort and rollback the currently-running query."]
    ]

    print(pretty_table(headers, rows))


@click.command()
@click.option("-v", "--version", is_flag=True, help="Show cycli version and exit.")
@click.option("-h", "--host", default="localhost", help="The host address of Neo4j.")
@click.option("-P", "--port", default="7474", help="The port number on which Neo4j is listening.")
@click.option("-u", "--username", help="Username for Neo4j authentication.")
@click.option("-p", "--password", help="Password for Neo4j authentication.")
@click.option("-t", "--timeout", help="Set a global socket timeout for queries.", type=click.INT)
@click.option('-l', '--logfile', type=click.File(mode="a", encoding="utf-8"), help="Log every query and its results to a file.")
@click.option("-f", "--filename", type=click.File(mode="rb"), help="Execute semicolon-separated Cypher queries from a file.")
@click.option("-s", "--ssl", is_flag=True, help="Use the HTTPS protocol.")
@click.option("-r", "--read-only", is_flag=True, help="Do not allow any write queries.")
def run(host, port, username, version, timeout, password, logfile, filename, ssl, read_only):
    if version:
        print("cycli {}".format(__version__))
        sys.exit(0)

    if username and not password:
        password = click.prompt("Password", hide_input=True, show_default=False, type=str)

    try:
        cycli = Cycli(host, port, username, password, logfile, filename, ssl, read_only, timeout)

    except AuthError:
        print("Unauthorized. See cycli --help for authorization instructions.")

    except ConnectionError:
        print("Connection refused. Is Neo4j turned on?")

    else:
        cycli.run()


if __name__ == '__main__':
    run()
