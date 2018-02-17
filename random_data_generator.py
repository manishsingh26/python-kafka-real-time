
import pandas as pd


class SalesDataGenerator(object):

    def __init__(self, app_config):
        self.app_config = app_config
        self.lead_data_path = app_config["lead_data"]["file"]
        self.employ_data = pd.read_csv("/home/msingh/Documents/PycharmProjects/kafka/data/Employ_df.csv")

    def lead_generator(self, row):

        lead_state = row["lead_state"]
        employ_designation = row["employ_designation"]

        filter_employ_data = self.employ_data[(self.employ_data["employ_territory_state"] == lead_state) &\
                                              (self.employ_data["employ_designation"] == employ_designation)]
        employ_assign_id = ((filter_employ_data.sample(1))["employ_id"]).values[0]
        row["employ_id"] = employ_assign_id
        return row
