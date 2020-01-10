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

def main():
    print('suh world')

if __name__ == "__main__":
    main()
