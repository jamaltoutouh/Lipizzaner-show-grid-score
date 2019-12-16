import string
import re
import json
import pandas as pd
from datetime import datetime
import numpy as np
import math

from collections import OrderedDict
from datetime import date

import os
import glob
import sys
from scipy.stats import shapiro
import csv
from pathlib import Path


def split_equal(data):
    container = data.split("=")
    return container[0], container[1]


def get_datetime(str):
    return datetime.strptime(str, '%Y-%m-%d %H:%M:%S')

class LogParsing:
    def __init__(self, data_path):
        self.data_path = data_path

    def get_log_files(self, prefix):
        return [file_path for file_path in glob.iglob(self.data_path + prefix + '/*/*/*log')]

    def log_file_to_dataframe(self, file_path):
        list_of_data = []
        data_storage = None

        try:
            for line in open(file_path, 'r'):
                if 'Iteration=' in line:
                    splitted_data = re.split("- |,", line)
                    analyzed_data = splitted_data[3:9]
                    data_storage = {}
                    data_storage['iteration'] = int(split_equal(analyzed_data[0])[1])
                    data_storage['f(Generator(x))'] = float(split_equal(analyzed_data[1])[1])
                    data_storage['f(Discriminator(x))'] = float(split_equal(analyzed_data[2])[1])
                    data_storage['lr_gen'] = float(split_equal(analyzed_data[3])[1])
                    data_storage['lr_dis'] = float(split_equal(analyzed_data[4])[1])
                    data_storage['score'] = float(split_equal(analyzed_data[5])[1])
                    data_storage['date_time'] = str(get_datetime(splitted_data[0]))

                if data_storage is not None:
                    list_of_data.append(data_storage)
                    data_storage = None

            return pd.DataFrame(list_of_data)
        except FileNotFoundError:
            return None()

    def get_cell_possition(self, checkpoint_file):
        for line in open(checkpoint_file, 'r'):
            if 'position' in line:
                splitted_data = re.split(": |,|}|{", line)
                x = int(splitted_data[3])
                y = int(splitted_data[5])
                return '{},{}'.format(x,y)
        return '-1,-1'

    def get_file_from_folder(self, folder, prefix):
        return [file_path for file_path in glob.iglob(str(folder) + '/*' + prefix + '*')][0]

    def get_scores_from_grid(self, prefix, score_column):
        data = dict()
        log_files = self.get_log_files(prefix)
        for log_file in log_files:
            data_df = self.log_file_to_dataframe(log_file)
            checkpoint = self.get_file_from_folder(str(Path(log_file).parent), 'checkpoint')
            cell_possition = self.get_cell_possition(checkpoint)
            data[cell_possition] = list(data_df[score_column])
        return pd.DataFrame(data)










