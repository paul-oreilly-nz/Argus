from argus.common.Common import CommonAppFramework, LogLevel
from argus.common.data import schema
from argus.common.KafkaConnection import KafkaConnection
from argus.common.PostgresConnection import PostgresConnection
import json
from time import sleep
import sys


class Caterpillar(CommonAppFramework):
    def __init__(self):
        super().__init__()
        # we need a kafta connection, and schema objects
        self.kafka = KafkaConnection(self)
        self.schema = schema.full_colander_set()
        self.postgres = PostgresConnection(self)

    def run(self):
        # start the sevices we will need
        self.kafka.start_consumer()
        self.postgres.connect()
        # check we have the tables in place
        self._check_postgres()
        # poll and process for results
        for i in range(45):
            results = self.kafka.fetch()
            self.log("Caterpillar finds {} result(s)".format(len(results)))
            results = self.conform_data(results)
            self.commit_to_db(results)
            sys.stdout.flush()
            sleep(1)

    def _check_postgres(self):
        cursor = self.postgres.db_connection.cursor()
        cursor.execute("SELECT current_database()")
        database = cursor.fetchone()[0]
        cursor.execute(
            "SELECT EXISTS(SELECT * FROM information_schema.tables "
            "WHERE table_name='heartbeat');"
        )
        if not cursor.fetchone()[0]:
            # then we need to make the table for the data to go into...
            self.log("Postgres database did not have heartbeat database. Creating..")
            cursor.execute(
                "CREATE TABLE heartbeat ("
                "id serial NOT NULL PRIMARY KEY, "
                "producer_id VARCHAR(200),"
                "info json NOT NULL);"
            )
            self.postgres.db_connection.commit()
            cursor.execute(
                "CREATE INDEX producer_index ON heartbeat (" " producer_id );"
            )
            self.postgres.db_connection.commit()
        else:
            self.log("Heatbeat database table is ready for use")
        cursor.close()

    def conform_data(self, data_list):
        results = []
        for item in data_list:
            value = json.loads(item.value.decode())
            deserializer = value.get("deserializer")
            conformed_value = {}
            result = {}
            # check if we have a deserializer defined, and if it actually exists
            if deserializer is None:
                self.log(
                    "Unable to decode package, deserializer not defined",
                    LogLevel.WARNING,
                )
                continue
            if not deserializer in self.schema:
                self.log(
                    "Unale to decode package, deserializer {} not found".format(
                        deserializer
                    ),
                    LogLevel.WARNING,
                )
                continue
            if not "data" in value:
                self.log(
                    "Unable to decode {}, data value not found".format(deserializer),
                    LogLevel.WARNING,
                )
            # can we deserialize successfully?
            try:
                conformed_value = self.schema[deserializer].deserialize(value["data"])
            except Exception as e:
                self.log(
                    "Error while decoding {} package - {}".format(deserializer, str(e))
                )
                continue
            # if we have valid data, add some other useful fields
            result["meta"] = {
                "timestamp": item.timestamp,
                "timestamp_type": item.timestamp_type,
                "kafka_offset": item.offset,
                "kafta_id": value["id"],
                "data_type": deserializer,
            }
            result["raw"] = value
            result["conformed"] = conformed_value
            results.append(result)
            self.log(
                "{} decoded from {} with timestamp {} and offset {}".format(
                    deserializer, value["id"], item.timestamp, item.offset
                )
            )
        return results

    def commit_to_db(self, data_list):
        cursor = self.postgres.db_connection.cursor()
        for item in data_list:
            # We can combine some of the data here, and make a new json string
            as_json = json.dumps({"data": item["raw"], "meta": item["meta"]})
            # which we then insert into the database
            cursor.execute(
                "INSERT INTO heartbeat (producer_id, info) "
                " VALUES( '{}', '{}');".format(item["meta"]["kafta_id"], as_json)
            )
            self.postgres.db_connection.commit()
        self.log("{} item(s) added to the postgres database".format(len(data_list)))
