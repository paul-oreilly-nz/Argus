"""
    The PostgresConnection class connects based on one environmental variable,
      POSTGRES_URL
"""

import os
from argus.common.Common import LogLevel
import json
import psycopg2

class PostgresConnection():
    def __init__(self, app):
        self.env = {}
        self.app = app
        # check the url to connect with exists
        self.url = os.environ.get('POSTGRES_URL')
        if self.url is None:
            app.log("Missing environment variable for POSTGRES_URL." \
                    "No database connection possible.", LogLevel.WARNING)
    def connect(self):
        self.cursor = None
        try:
            self.db_connection = psycopg2.connect( self.url )
        except Exception as e:
            app.log("Exception encountered while connecting to Postgres: {}".format(
                str(e)), LogLevel.WARNING)
    
