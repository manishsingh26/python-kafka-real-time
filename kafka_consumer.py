import json
from datetime import datetime


from kafka import KafkaConsumer
from elasticsearch_connector import ElasticsearchConnection


def consumer_main(app_config):
    consumer = KafkaConsumer('sales_database', bootstrap_servers=['localhost:9092'])

    es_obj = ElasticsearchConnection(app_config)
    es_obj.elastic_connection()
    es = es_obj.es

    index = 1
    for message in consumer:

        if message.topic == "sales_database":

            try:
                doc = json.loads(message.value.decode('utf-8'))

                location_doc = dict()
                location_doc["lead_id"] = int(doc["lead_id"])
                location_doc["location"] = [float(doc["lead_long"]), float(doc["lead_lat"])]

                es.index(index="leaddata", doc_type="lead", id=index, body=doc)
                es.index(index="leaddatalocation", doc_type="leadlocation", id=index, body=location_doc)
                index += 1

            except Exception as e:
                print(e.message)
                print(e.args)


if __name__ == "__main__":
    app_config = json.load(open("app_config.json"))
    consumer_main(app_config)
