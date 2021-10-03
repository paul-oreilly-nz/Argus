from argus.common.Common import CommonAppFramework, LogLevel
from argus.common.data import schema
from argus.common.KafkaConnection import KafkaConnection

import sys
import random
from datetime import datetime
from time import sleep


class Faker(CommonAppFramework):
    def __init__(self):
        super().__init__()
        # We need a kafta connection, which will init based on environmental variables
        self.kafka = KafkaConnection(self)
        self.set_limits(cpu_count=random.choice([2, 4, 6, 8, 12, 16, 24, 32, 48, 64]))
        self.schema = schema.full_colander_set()

    def run(self):
        self.kafka.start_producer()
        # run for a minute, then terminate
        for i in range(60):
            self.log("Generating a fake record to send to Kafka")
            self.kafka.send(
                data=self.fake_heartbeat_data(), deserializer_name="heartbeat"
            )
            sys.stdout.flush()
            sleep(1)

    def set_limits(self, cpu_count=4):
        self.cpu_count = cpu_count

    def fake_CPU_Load_data(self):
        result = []
        for i in range(self.cpu_count):
            result.append(random.randint(0, 1000) * 1.0 / 10)
        return self.schema["cpu_load"].serialize(result)

    def fake_CPU_Times_data(self):
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
        result = {
            "load": self.fake_CPU_Load_data(),
            "times": self.fake_CPU_Times_data(),
        }
        return self.schema["cpus"].serialize(result)

    def fake_heartbeat_data(self):
        result = {"timestamp": datetime.now(), "cpus": self.fake_CPUs_data()}
        return self.schema["heartbeat"].serialize(result)
