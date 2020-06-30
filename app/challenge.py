import os
import requests
import random
import time
import hashlib
import pandas as pd
import sqlite3 as db


class zinobe_challenge():
    def __init__(self):
        self.base_rapid_api_url = os.environ.get("RAPID_API")
        self.rapid_api_key = os.environ.get("RAPID_API_KEY")

    def request_info(self):
        region_base_url = self.base_rapid_api_url + "region/"

        headers = { 'x-rapidapi-key': self.rapid_api_key }
        regions = ["africa", "americas", "asia", "europe", "oceania"]
        labels = ["Region", "Country", "Language", "Time"]
        join_data = []
        
        ## Initial time
        ti = time.time()

        ## Iterate over regions
        for region in regions:

            ## Request for region iterator
            url = region_base_url + region
            response = requests.request("GET", url, headers=headers)
            json_response = response.json()
            index = random.randint(0, len(json_response)-1)
            country = json_response[index]
            country_name = country.get("name")
            langs = country.get("languages")
            langs_str = ",".join(langs)
            encoded_langs = hashlib.sha1(langs_str.encode()).hexdigest()
            print(response.elapsed.total_seconds())
            
            ## Construct the element to save
            join_data.append((
                region.capitalize(),
                country_name,
                encoded_langs,
                round(response.elapsed.total_seconds(), 3)
            ))

        ## Final time
        tf = time.time()

        df = pd.DataFrame.from_records(join_data, columns=labels)
        mean_time = round(df["Time"].mean(), 3)
        min_time = round(df["Time"].min(), 3)
        max_time = round(df["Time"].max(), 3)
        total_time = round(tf-ti, 3)
        metrics_data = {
            "mean_time": [mean_time],
            "max_time": [max_time],
            "min_time": [min_time],
            "total_time": [total_time]
        }
        metrics_df = pd.DataFrame.from_dict(metrics_data)

        conn = db.connect('test.db')
        df.to_sql('challenge', con=conn, if_exists='replace')
        df.to_json('data.json', orient='split')
        metrics_df.to_sql('metrics', con=conn, if_exists='replace')
        metrics_df.to_json('metrics.json', orient='split')

