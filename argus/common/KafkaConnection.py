"""
    The Kafka connection class uses environment variables for both direct values, and
    for the location of files that hold secrets (compatible with kubernetes environments
    and secrets managers). The values and purposes used are:

        KAFKA_HOST                  The URI of the Kafka host to connect to
        KAFKA_PORT                  Which port to connect to
        KAFKA_KEY_FILE_LOCATION     file location (inside a container at times) to load
                                        the access key from. File should contain only
                                        the access key, and no other information
        KAFKA_ACCESS_CERT_LOCATION  file location to load the Access Cert from
        KAFKA_CA_CERT_LOCAITON      file location to load the CA Cert from
"""


environment_variable_map = {
    "host": "KAFKA_HOST",
    "port": "KAFKA_PORT",
    "key_file": "KAFKA_KEY_FILE_LOCATION",
    "access_cert_file": "KAFKA_ACCESS_CERT_LOCATION",
    "ca_cert_file": "KAFKA_CA_CERT_LOCATION",
    "topic": "KAFKA_TOPIC",
    "id": "KAFKA_MY_ID",
    "group": "KAFKA_GROUP_ID",
    "timeout": "KAFKA_CLIENT_TIMEOUT",
}

environment_variable_defaults = {
    "topic": "default",
    "group": "default",
    "timeout": 1000,
}

import os
from argus.common.Common import LogLevel
from kafka import KafkaProducer, KafkaConsumer
import json


class KafkaConnection:
    def __init__(self, app):
        """
        Requires the application as an argument, in order that we can refer to the
        application log.
        """
        self.env = {}
        self.app = app
        self._parse_environment_variables(os.environ)
        self._verify_secrets_files()

    def _parse_environment_variables(self, env_map):
        """
        Check that we have the environment variables and details we need.
        Missing environment variables are noted and reported,
        and an exception is raised if key values are missing.
        """
        missing_env_vars = []
        for internal, external in environment_variable_map.items():
            self.env[internal] = env_map.get(external)
            if self.env[internal] is None:
                if internal in environment_variable_defaults:
                    self.env[internal] = environment_variable_defaults[internal]
                else:
                    missing_env_vars.append(external)
        if len(missing_env_vars) > 0:
            issue = (
                "A connection to Kafta cannot be formed, as the following "
                "environmental variables are missing: {}".format(
                    ", ".join(missing_env_vars)
                )
            )
            self.app.log(issue, log_level=LogLevel.CRITICAL)
            raise Exception(issue)

    def _verify_secrets_files(self):
        """
        For a list of variables (in 'self[]') that refer to file paths, load the
        contents of those files into variales of the same name, with '_file' stripped
        to create the new variable name.
        """
        file_path_variables = ["key_file", "access_cert_file", "ca_cert_file"]
        # loop over each of the above values to find the file and read the contents
        # into a new self assigned variable
        for key in file_path_variables:
            if key not in self.env.keys():
                raise Exception(
                    "Key {} not found in self for KaftaLink object".format(key)
                )
            path = self.env[key]
            if not os.path.isfile(path):
                raise FileNotFoundError(path)

    def start_producer(self):
        self.producer = KafkaProducer(
            bootstrap_servers="{}:{}".format(self.env["host"], self.env["port"]),
            security_protocol="SSL",
            ssl_cafile=self.env["ca_cert_file"],
            ssl_certfile=self.env["access_cert_file"],
            ssl_keyfile=self.env["key_file"],
            value_serializer=lambda v: json.dumps(v).encode("ascii"),
            key_serializer=lambda v: json.dumps(v).encode("ascii"),
            api_version=(2, 6, 0),
        )

    def start_consumer(self):
        self.consumer = KafkaConsumer(
            self.env["topic"],
            auto_offset_reset="earliest",
            bootstrap_servers="{}:{}".format(self.env["host"], self.env["port"]),
            client_id=self.env["id"],
            group_id=self.env["group"],
            security_protocol="SSL",
            ssl_cafile=self.env["ca_cert_file"],
            ssl_certfile=self.env["access_cert_file"],
            ssl_keyfile=self.env["key_file"],
            api_version=(2, 6, 0),
        )
        self.consumer_has_had_initial_call = False

    def send(self, deserializer_name, data):
        msg_data = {
            "id": self.env["id"],
            "deserializer": deserializer_name,
            "data": data,
        }
        key = {"key": self.env["id"]}
        self.producer.send(self.env["topic"], msg_data, key)
        self.producer.flush()

    def fetch(self):
        raw_msg = self.consumer.poll(timeout_ms=self.env["timeout"])
        result = []
        for topic_partition, msgs in raw_msg.items():
            for msg in msgs:
                result.append(msg)
        self.consumer.commit()
        if not self.consumer_has_had_initial_call:
            self.consumer_has_had_initial_call = True
            return self.fetch()
        return result
