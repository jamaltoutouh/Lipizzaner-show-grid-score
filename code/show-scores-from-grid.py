from matplotlib import pyplot
from scipy.stats import shapiro
import random
import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
from matplotlib.figure import figaspect
import seaborn as sns
sns.set(style="whitegrid")
sns.set(font_scale=2)

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

from parse_distributed_logs_NO_DOKER import LogParsing

parser = LogParsing('../data/')
print(parser.get_scores_from_grid('*SPa*', 'score').columns)

class ShowGrid:
    def __init__(self, data_df):
        self.data = data_df

    def get_grid_status(self, iteration):
        return self.data.iloc[iteration]

    def get_possition_from_column_name(self, column_name):
        splitted_data = re.split(",", column_name)
        return int(splitted_data[0]), int(splitted_data[1])

    def get_grid_size(self):
        mmax = 0
        for column in self.data.columns:
            x, y = self.get_possition_from_column_name(column)
            if x>mmax:
                mmax=x
        return mmax+1

    def create_heatmap_data(self, data_df, file_name='', title='',  show=False, vmax=800, vmin=0, annot=False, create_pdf=True):
        grid_size = self.get_grid_size()
        values = np.zeros((grid_size, grid_size))
        for x in range(grid_size):
            for y in range(grid_size):
                values[x][y] = int(data_df['{},{}'.format(x,y)])

        w, h = figaspect(4 / 4)
        f, ax = plt.subplots(figsize=(w, h))
        if title != '':
            ax.set_title(title)
        ax = sns.heatmap(values.astype(int), linewidth=0.5, vmax=vmax, vmin=vmin, annot=annot, cbar=False, cmap="Blues", fmt="0d")
        if file_name != '':
            plt.savefig(file_name + '.png')
            if create_pdf:
                plt.savefig(file_name + '.pdf')
        if show:
            plt.show()

        return values

    def createa_heatmap_video(self, experiment, vmax, vmin, annot=False, step=1):
        tmp = './tmp/'
        images = []
        if not os.path.exists('./tmp'):
            os.makedirs(tmp)

        for i in range(self.data.shape[0]):
            if i%step==0:
                image_path = tmp + experiment + '{:04d}'.format(i)
                self.create_heatmap_data(self.get_grid_status(i), image_path, title='Epoch: {}'.format(i),  show=False, vmax=vmax,
                                      vmin=vmin, annot=annot, create_pdf=False)
                print('Created frame {}'.format(i))

            images.append(imageio.imread(image_path + '.png'))
        imageio.mimsave(experiment + '.gif', images)
        print('Finished: Created animation in file {}'.format(experiment+'.gif'))



vmax = 300
vmin = 40
annot = True



parser = LogParsing('../data/')
experiment = 'SPaGAN'
data_df = parser.get_scores_from_grid('*'+experiment+'*', 'score')
show = ShowGrid(data_df)
show.createa_heatmap_video('SPaGAN', vmax=vmax, vmin=vmin, annot=False, step=2)

experiment = 'Lipi'
data_df = parser.get_scores_from_grid('*'+experiment+'*', 'score')
show = ShowGrid(data_df)
show.createa_heatmap_video('Lipi', vmax=vmax, vmin=vmin, annot=False, step=2)


# show.create_heatmap_data(show.get_grid_status(0), file_name=experiment + '-000', vmax=vmax, vmin=vmin, annot=annot)
# show.create_heatmap_data(show.get_grid_status(24), file_name=experiment + '-025', vmax=vmax, vmin=vmin, annot=annot)
# show.create_heatmap_data(show.get_grid_status(49), file_name=experiment + '-050', vmax=vmax, vmin=vmin, annot=annot)
# show.create_heatmap_data(show.get_grid_status(74), file_name=experiment + '-075', vmax=vmax, vmin=vmin, annot=annot)
# show.create_heatmap_data(show.get_grid_status(99), file_name=experiment + '-100', vmax=vmax, vmin=vmin, annot=annot)
#
# experiment = 'Lipi'
# data_df = parser.get_scores_from_grid('*'+experiment+'*', 'score')
# print(data_df)
# show = ShowGrid(data_df)
# show.create_heatmap_data(show.get_grid_status(0), file_name=experiment + '-000', vmax=vmax, vmin=vmin, annot=annot)
# show.create_heatmap_data(show.get_grid_status(24), file_name=experiment + '-025', vmax=vmax, vmin=vmin, annot=annot)
# show.create_heatmap_data(show.get_grid_status(49), file_name=experiment + '-050', vmax=vmax, vmin=vmin, annot=annot)
# show.create_heatmap_data(show.get_grid_status(74), file_name=experiment + '-075', vmax=vmax, vmin=vmin, annot=annot)
# show.create_heatmap_data(show.get_grid_status(99), file_name=experiment + '-100', vmax=vmax, vmin=vmin, annot=annot)