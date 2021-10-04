#!/usr/bin/env python3

"""
    Argus Terminal Monitor 0.1
    Monitor a single set of data from one provider in a console.

    Usage:
      terminal-monitor.py  <provider_id> [--run_once]
      terminal-monitor.py  --help | -h
      terminal-monitor.py  --version

    Options:
      -h --help     Show this screen
      --verison     Show version
      --run_once    Don't refresh the display - run once and terminate
"""

from docopt import docopt

import json
from time import sleep
import os, sys
from pprint import pprint


class TerminalMonitor:
    def __init__(self, args):
        """
        Sets up to connect to Postgres and initialises default values
        """
        from argus.common.PostgresConnection import PostgresConnection
        self.log_buffer = []
        self.postgres = PostgresConnection(self)
        self.latest = {}
        self.args = args
        # below nifty funciton sourced from
        #  https://www.delftstack.com/howto/python/python-clear-console/
        self.clear_cmd = lambda: os.system(
            "cls" if os.name in ("nt", "dos") else "clear"
        )
        pprint(self.args)
        self.target = self.args.get("<provider_id>")

    def log(self, message, level):
        """
        Logging function also provided for (and used by) the PostgresConnection object
        """
        self.log_buffer.append(message)

    def run(self, exception_passthrough=False):
        """
        Connects to postgres, and then depending on if 'run_once' is set or not,
        will generate and loop over a display until terminated.
        """
        # establish the postgres connection
        self.postgres.connect()
        # just show one screen if 'run-once' is set
        if self.args["--run_once"]:
            fetch_latest_data()
            update_display()
            exit(0)
        # loop until a keyboard interrupt
        try:
            while True:
                self.fetch_latest_data()
                self.update_display()
        except KeyboardInterrupt:
            print("Press Ctl-C to terminate")
            pass

    def fetch_latest_data(self, exception_passthrough=False):
        """
        Queries Postgres for the last heartbeat record from a given producer_id
        (set by self.target)
        'exception_passthrough' will pass any exceptions generated up the chain
        """
        try:
            cursor = self.postgres.db_connection.cursor()
            cursor.execute(
                "SELECT * FROM heartbeat "
                "WHERE producer_id='{}' "
                "ORDER BY id DESC "
                "LIMIT 1;".format(self.target)
            )
            self.latest = cursor.fetchall()[0]
        except Exception as e:
            self.log("Error encountered while fetching data {}".format(str(e)))
            if exception_passthrough:
                raise e

    def update_display(self):
        """
        Clears the terminal and displays formatted data taken from the last
        entry for the given provider_id
        """
        self.clear_cmd()
        print("Argus Terminal Monitor - {}\n\n".format(self.target))
        data = self.latest[2].get("data", {}).get("data", {})
        meta = self.latest[2].get("meta", {})
        cpu_times = ""
        for k, v in data.get("cpus", {}).get("times", {}).items():
            cpu_times += f"  {k:<12} {v}\n"
        print(
            "Timestamp: {timestamp}\n"
            "Offset:    {offset}\n\n"
            "CPU Usage: {CPU_Load}%\n"
            "Time Data:\n{CPU_Times}".format(
                timestamp=meta.get("timestamp"),
                offset=meta.get("kafka_offset"),
                CPU_Load="%, ".join(data.get("cpus", {}).get("load", [])),
                CPU_Times=cpu_times,
            )
        )


if __name__ == "__main__":
    print("Starting Terminal Monitor")
    sys.path.append("/app")
    args = docopt(__doc__, version="Argus Terminal Monitor 0.1")
    monitor = TerminalMonitor(args)
    monitor.run()
