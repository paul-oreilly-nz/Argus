from argus.common.Common import CommonAppFramework, LogLevel
from argus.common.data import schema
from argus.common.KafkaConnection import KafkaConnection
import json


class Caterpillar( CommonAppFramework ):
    def __init__(self):
        super().__init__()
        # we need a kafta connection, and schema objects
        self.kafka = KafkaConnection( self )
        self.schema = schema.full_colander_set()
    
    def run(self):
        self.kafka.start_consumer()
        results=self.kafka.fetch()
        self.log("Caterpillar finds {} result(s)".format( len( results )))
        results = self.conform_data(results)
        self.commit_to_db(results)

    def conform_data(self, data_list):
        results = []
        for item in data_list:
            value = json.loads(item.value.decode())
            deserializer = value.get('deserializer')
            # check if we have a deserializer defined, and if it actually exists
            if deserializer is None:
                self.log("Unable to decode package, deserializer not defined", 
                        LogLevel.WARNING)
                continue
            if not deserializer in self.schema:
                self.log("Unale to decode package, deserializer {} not found".format(
                    deserializer), LogLevel.WARNING)
                continue
            if not 'data' in value:
                self.log("Unable to decode {}, data value not found".format(
                    deserializer), LogLevel.WARNING)
            # can we deserialize successfully?
            try:
                result = self.schema[ deserializer ].deserialize( value['data'] )
            except Exception as e:
                self.log("Error while decoding {} package - {}".format(
                    deserializer, str(e)))
                continue
            # if we have valid data, add some other useful fields
            result['kafka_timestamp'] = item.timestamp
            result['kafka_timestamp_type'] = item.timestamp_type
            result['kafka_offset'] = item.offset
            result['kafta_id'] = value['id']
            results.append(result)
            self.log('{} decoded from {} with timestamp {} and offset {}'.format(
                deserializer, value['id'], item.timestamp, item.offset ))
        return results

    def commit_to_db(self, data_list):
        from pprint import pprint
        pprint( data_list )




