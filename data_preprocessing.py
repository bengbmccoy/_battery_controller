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
    parser.add_argument('-solar_scale', type=str,
                        help='ratio to scale the solar profile from 1kW')
    parser.add_argument('-solar_plot', type=str,
                        help='solar profile plot type')
    parser.add_argument('-load_data', type=str,
                        help='residential load data filepath')
    parser.add_argument('-load_plot', type=str,
                        help='load profile plot type')
    parser.add_argument('-profile_type', type=str,
                        help='type of residential load profile to use')
    parser.add_argument('-output_profile', type=str,
                        help='name of output data')
    args = parser.parse_args()

    if args.solar_data:
        solar_data = open_csv(args.solar_data)
        solar_process = data_process(solar_data)
        solar_process.find_max_solar()
        solar_process.scale_data(args.solar_scale)
        print(len(solar_process.scaled_profile))

        if args.solar_plot:
            solar_process.plot(args.solar_plot)
            plt.show()

    if args.load_data:
        load_data = open_csv(args.load_data)
        load_process = data_process(load_data)
        print(len(load_process.find_profile(args.profile_type)))

        if args.load_plot:
            load_process.plot(args.load_plot)
            plt.show()

    if args.output_profile:
        print(pd.concat([load_process.find_profile(args.profile_type), solar_process.scaled_profile], axis=1))
        save_csv(pd.concat([load_process.find_profile(args.profile_type), solar_process.scaled_profile], axis=1), args.output_profile)

class data_process():
    def __init__(self, df):
        self.df = df

    def find_max_solar(self):
        '''Finds the solar output profile with the optimal azimuth angle and
        thus produces the most electricity'''
        self.df.loc['Total'] = self.df.sum()
        totals = list(self.df.loc['Total', :])
        runs = list(self.df.columns)
        self.df = self.df.drop('Total')
        max_index, max_value = max(enumerate(totals), key=operator.itemgetter(1))
        self.opt_az = self.df[runs[max_index]]

    def find_profile(self, profile_type):
        return self.df[profile_type]

    def scale_data(self, scale):
        self.scaled_profile = (float(scale)*self.opt_az)

    def plot(self, plot_type):
        if plot_type == 'mean':
            self.df.T.mean().plot()

        if plot_type == 'max':
            self.opt_az.plot()

        if plot_type == 'max_scaled':
            self.scaled_profile.plot()

        if plot_type == 'all':
            self.df.plot()

def open_csv(filename):
    return pd.read_csv(filename, index_col='Hours since 00:00 Jan 1')

def save_csv(df, save_file):
    df.to_csv(save_file, index=True)

if __name__ == "__main__":
    main()
