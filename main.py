
import json

from multiprocessing import Process
from kafka_consumer import consumer_main
from kafka_producer import producer_main


if __name__ == "__main__":

    app_config = json.load(open("app_config.json"))

    producer_process = Process(target=producer_main(app_config))
    producer_process.start()
    consumer_process = Process(target=consumer_main(app_config))
    consumer_process.start()

