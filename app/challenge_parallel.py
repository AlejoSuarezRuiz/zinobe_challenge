import os
import requests
import random
import time
import hashlib
import pandas as pd
import sqlite3 as db

import multiprocessing
from joblib import Parallel, delayed


class zinobe_challenge_parallel():
    def __init__(self):
        self.base_rapid_api_url = os.environ.get("RAPID_API")
        self.rapid_api_key = os.environ.get("RAPID_API_KEY")

    def request_for_region(self, region, region_base_url, headers):
        ## Request for region parameter
        url = region_base_url + region
        response = requests.request("GET", url, headers=headers)
        json_response = response.json()
        index = random.randint(0, len(json_response)-1)
        country = json_response[index]
        country_name = country.get("name")
        langs = country.get("languages")
        langs_str = ",".join(langs)
        encoded_langs = hashlib.sha1(langs_str.encode()).hexdigest()
        
        ## Return tuple element 
        return((
            region.capitalize(),
            country_name,
            encoded_langs,
            round(response.elapsed.total_seconds(), 3)
        ))

    def request_info(self):      
        region_base_url = self.base_rapid_api_url + "region/"

        headers = { 'x-rapidapi-key': self.rapid_api_key }
        regions = ["africa", "americas", "asia", "europe", "oceania"]
        labels = ["Region", "Country", "Language", "Time"]
        join_data = []

        num_cores = multiprocessing.cpu_count()

        ## Initial time
        ti = time.time()

        processed_list = Parallel(n_jobs=num_cores)(
            delayed(self.request_for_region)(region, region_base_url, headers) for region in regions
        )

        ## Final time
        tf = time.time()

        df = pd.DataFrame.from_records(processed_list, columns=labels)
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

