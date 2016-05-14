# coding: utf8
"""
Re-runnable script that loads the data.
"""

import json
import pandas as pd

data = pd.read_csv(
    '2016_lw_survey_public_release_3.csv',
    low_memory=False,
)
column_infos = json.load(open('column_infos.json'))
column_infos = {info['csv_key']: info for info in column_infos}
