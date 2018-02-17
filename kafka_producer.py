
import msgpack, json, csv, time
from kafka import KafkaProducer
from kafka.errors import KafkaError


from random_data_generator import SalesDataGenerator
app_config = json.load(open("app_config.json"))


def producer_main(app_config):

    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

    data_generator_obj = SalesDataGenerator(app_config)
    lead_data_path = app_config["lead_data"]["file"]
    reader = csv.DictReader(open(lead_data_path))

    for row in reader:

        try:
            final_data = data_generator_obj.lead_generator(row)
            producer.send('sales_database', json.dumps(final_data).encode('utf-8'))
            time.sleep(1)
            producer.flush()

        except IOError:
            print("Print data is not in right format")


if __name__ == "__main__":
    app_config = json.load(open("app_config.json"))
    producer_main(app_config)
