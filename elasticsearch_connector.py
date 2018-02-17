
import csv
import json
from elasticsearch import Elasticsearch


class ElasticsearchConnection(object):

    def __init__(self, app_config):
        self.app_config = app_config
        self.elastic_host = self.app_config['elastic_search']['host']
        self.elastic_port = int(self.app_config['elastic_search']['port'])
        self.es = ''
        self.elastic_index_status = self.app_config['elastic_search']['index']['create']['status']
        self.elastic_index_name = self.app_config['elastic_search']['index']['create']['index']
        self.elastic_index_type = self.app_config['elastic_search']['index']['create']['type']
        self.elastic_index_field_id = self.app_config['elastic_search']['index']['create']['field_id']

    def elastic_connection(self):
        self.es = Elasticsearch(hosts=[{'host': self.elastic_host, 'port': self.elastic_port}])

    def elastic_index(self):

        if self.elastic_index_status is False:
            return self.es
        else:
            elastic_request_body = self.app_config['elastic_search']['index']['create']['request_body']
            return self.es.indices.create(index=self.elastic_index_name, body=elastic_request_body)

    def elastic_csv_bulk_push(self):
        csv_file = self.app_config['elastic_search']['index']['create']['csv_file']
        csv_file_object = csv.reader(open(csv_file, 'r'))

        header = next(csv_file_object)
        header = [item.lower() for item in header]

        bulk_data = []
        for row in csv_file_object:

            data_dict = {}
            for i in range(len(row)):

                data_dict[header[i]] = row[i]
            op_dict = {"index": {
                        "_index": self.elastic_index_name,
                        "_type": self.elastic_index_type,
                        "_id": data_dict[self.elastic_index_field_id]
                            }
                        }
            bulk_data.append(op_dict)
            bulk_data.append(data_dict)
        self.es.bulk(index=self.elastic_index_name, body=bulk_data, refresh=True)


if __name__ == "__main__":

    app_config = json.load(open("/home/msingh/Documents/PycharmProjects/kafka/app_config.json"))
    obj = ElasticsearchConnection(app_config)
    obj.elastic_connection()
    obj.elastic_index()
    obj.elastic_csv_bulk_push()
