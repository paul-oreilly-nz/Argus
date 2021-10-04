"""
    Faker generates fake records of data and submits those records to Kafta
"""

from argus.common.Common import CommonAppFramework, LogLevel
from argus.common.data import schema
from argus.common.KafkaConnection import KafkaConnection

import sys
import random
from datetime import datetime
from time import sleep


class Faker(CommonAppFramework):
    def __init__(self):
        """
        Establishes a connection to Kafka (based on environmental vars)
        Chooses a random number from a list to represent the number of CPU's 
        for the fake system.
        """
        super().__init__()
        self.kafka = KafkaConnection(self)
        self.set_limits(cpu_count=random.choice([2, 4, 6, 8, 12, 16, 24, 32, 48, 64]))
        self.schema = schema.full_colander_set()

    def run(self):
        """
        This will generate 60 'heartbeat' objects and submit those to Kafta 
        with a second between each.
        """
        self.kafka.start_producer()
        # run for a minute, then terminate
        for i in range(60):
            self.log("Generating a fake record to send to Kafka")
            self.kafka.send(
                data=self.fake_heartbeat_data(), deserializer_name="heartbeat"
            )
            sys.stdout.flush()
            sleep(1)

    def fake_CPU_Load_data(self):
        """
        Generates a sequence of load values (as percentages), one for each fake CPU.
        Returns schema verified cpu load data.
        """
        result = []
        for i in range(self.cpu_count):
            result.append(random.randint(0, 1000) * 1.0 / 10)
        return self.schema["cpu_load"].serialize(result)

    def fake_CPU_Times_data(self):
        """
        Generates a fake set of timing data 
        (each between 0 and 1000 with two decimals), 
        for each of the system time stats.
        Returns schema verified cpu time data.
        """
        terms = [
            "user",
            "nice",
            "system",
            "idle",
            "iowait",
            "irq",
            "softirq",
            "steal",
            "guest",
            "guest_nice",
        ]
        result = {}
        for item in terms:
            result[item] = random.randrange(0, 100000) * 1.0 / 100
        return self.schema["cpu_times"].serialize(result)

    def fake_CPUs_data(self):
        """
        Combines both CPU load and CPU time data, 
        returning these as a schema verified object.
        """
        result = {
            "load": self.fake_CPU_Load_data(),
            "times": self.fake_CPU_Times_data(),
        }
        return self.schema["cpus"].serialize(result)

    def fake_heartbeat_data(self):
        """
        Adds a timestamp to a CPU data set (load, times). 
        Returns a heartbeat schema verified object.
        """
        result = {"timestamp": datetime.now(), "cpus": self.fake_CPUs_data()}
        return self.schema["heartbeat"].serialize(result)
