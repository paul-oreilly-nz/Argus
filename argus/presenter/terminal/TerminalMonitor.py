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


class TerminalMonitor():
    def __init__(self, args):
        from argus.common.PostgresConnection import PostgresConnection 
        self.log_buffer = []
        self.postgres = PostgresConnection(self)
        self.latest = {}
        self.args = args
        # below nifty funciton sourced from 
        #  https://www.delftstack.com/howto/python/python-clear-console/
        self.clear_cmd = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        pprint(self.args)
        self.target = self.args.get('<provider_id>')

    def log(self, message, level):
        self.log_buffer.append( message )
    
    def run(self):
        # establish the postgres connection
        self.postgres.connect()
        # just show one screen if 'run-once' is set
        if self.args['--run_once']:
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

    def fetch_latest_data(self):
        try:
            cursor = self.postgres.db_connection.cursor()
            cursor.execute( "SELECT * FROM heartbeat " \
                "WHERE producer_id='{}' " \
                "ORDER BY id DESC " \
                "LIMIT 1;".format( self.target))
            self.latest = cursor.fetchall()[0]
        except Exception as e:
            self.log("Error encountered while fetching data {}".format(str(e)))
    
    def update_display(self):
        self.clear_cmd()
        print("Argus Terminal Monitor - {}\n\n".format(self.target))
        data = self.latest[2].get('data',{}).get('data',{})
        meta = self.latest[2].get('meta',{})
        cpu_times = ""
        for k,v in data.get('cpus',{}).get('times',{}).items():
            cpu_times += (f'  {k:<12} {v}\n')
        print("Timestamp: {timestamp}\n" \
               "Offset:    {offset}\n\n" \
               "CPU Usage: {CPU_Load}%\n" \
               "Time Data:\n{CPU_Times}".format(
                    timestamp = meta.get('timestamp'),
                    offset = meta.get('kafka_offset'),
                    CPU_Load = "%, ".join(data.get('cpus',{}).get('load',[])),
                    CPU_Times = cpu_times
                    ))



if __name__ == "__main__":
    print("Starting Terminal Monitor")
    sys.path.append( '/app' )
    args = docopt(__doc__, version="Argus Terminal Monitor 0.1")
    monitor = TerminalMonitor( args )
    monitor.run()
