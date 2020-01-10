'''
Written by: Ben McCoy Jan 2020

This script is the start of the _battery_controller project and its purpose
will be to preprocess any data required into the correct format, as well
as screen and visualize the data to ensure that it looks good and will not
break the main optimal operation number crunching code.

This script will have to preprocess the data below:
- AEMO residential profile data
-- Scale the data to match the annual consumption of an average house
-- Organise the data into proper time periods
-- Search for anomalies or missing data
-- Visualize the data (anomalies and averages)

- PVSyst solar output data
-- Scale the data to an average array size (probably 5kW)
-- Search data for anomalies or missing data
-- Visualize the data (anomalies and averages)

- Tariff data
-- This will need to be placed into an easily accessible format to be stored
separately from the load and solar time series data.
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import operator
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-solar_data', type=str,
                        help='solar data filepath')
    parser.add_argument('-solar_plot', type=str,
                        help='solar profile plot type')
    parser.add_argument('-load_data', type=str,
                        help='residential load data filepath')
    args = parser.parse_args()

    if args.solar_data:
        solar_data = open_csv(args.solar_data)
        solar_data = solar_data_process(solar_data, args.solar_plot)
        solar_profile = solar_data.find_max_solar()

        if args.solar_plot:
            solar_data.plot()
            plt.show()


class solar_data_process():
    def __init__(self, df, plot_type=False):
        self.df = df
        self.plot_type = plot_type

    def find_max_solar(self):
        self.df.loc['Total'] = self.df.sum()
        totals = list(self.df.loc['Total', :])
        runs = list(self.df.columns)
        self.df = self.df.drop('Total')
        max_index, max_value = max(enumerate(totals), key=operator.itemgetter(1))
        self.opt_az = self.df[runs[max_index]]

        return self.opt_az

    def plot(self):
        if self.plot_type == 'mean':
            self.df.T.mean().plot()

        if self.plot_type == 'max':
            self.opt_az.plot()



def open_csv(filename):
    return pd.read_csv(filename, index_col='Hours since 00:00 Jan 1')

if __name__ == "__main__":
    main()
