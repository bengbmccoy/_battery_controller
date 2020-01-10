# _battery_controller
A machine learning project to: collect and organise data, numerically determine optimal battery controls, train a model to predict optimal battery operation.

Started: Ben McCoy, Jan 9, 2020.

The aim of this project is to train a neural netowrk, or other model to predict the optimal battery charge/discharge control given a number of realistic inputs. To train this model, the optimal battery control for a minimum training period will be required. To generate a "perfect" control training period I will write a script that can numerically determine the optimal 24 hour battery control profile, given a tarff, solar and residential load profile, this script will then determine the optimal traiing period for a year of data. Using the "perfect" control profile the modeal will be trained by using input variables to try and estimate the battery control each hour, then using back-propogation to learn after each time period given to the example. Multiple models will be trained and each model will be tested on a subset of the "perfect" control profile to determine the best model. Results will be presented, however future improvements can be made using new data or more data.

1. Collecting Data:
- Residential load data will be sourced from AEMO online profiles of local networks, which will be scaled to match the average daily household consumption. There are issues with this method, as residential profiles are not actually that smooth, but this application could be better suited to commercial users anyway, who often have much smoother profiles.

- Solar generation data will be sourced from PVSyst, I could access a one month free trial, however I have some previous data from a different project saved. It is a 1kW solar output profile of a residence in Adelaide for a whole year. I will just scale this data as well.

- There may be some data available from the PECAN street project (pecanstreet.org) that I will need to have a quick look at as well.

Edit: I looked into pecan street data and you have to purchase a commercial license to use the data or you need to be part of a university research team.

2. Determine Optimal Operation using Numerical Methods:
- For each 24 hour period where a load profile and a solar profile meet an electricity tariff, there is a optimal battery control profile that minimises the cost pade by the controller. With that in mind, we would like to find the optimal battery control profile.

- Start with 24 hours of load, solar and tariff data, then apply a random battery control profile, that is legal within the battery operating constraints, and determine the cost.

- For each time period in the control profile, nudge the controls up or down, by a small amount and record the change in cost. For the control profile change that had the largest shift in cost, update the battery optimal control profile.

- Repeat until local minimum.

- Perform above process with multilple different random starter profiles and determine best profile for the 24 hour period.

- Repeat above process for up to 365 days.

3. Choose Input Variables:
- To train the model will require inputs to the model, these can be determined by myself closer to the time when the model needs to be trained. Additionally, I can try and train multiple different models with different input variable so this step is not major.

- Considering other papers on battery control optimisation, a good start might involve inputs such as:
day of the week, hour of the day, solar input, solar forecast (next 24 hours), residential load, tariff, load forecast, battery SOC and more.

4. Train a battery controller:
- After a model(s) architecture is chosen, a random initialisation weights matrix will be implemented, then using the inputs to the model, the model will try to predict the optimal battery operation, given the inputs, for each time period in the year.

- After each attempted prediction, the model will learn by performing back propogation and adjusting the weights for each node.

- After learning from the full training set, each model will be tested using a subset of the data where given the inputs, the model will attempt to predict optimal battery operations.

5. Present the results as:
Energy costs per year with no battery
Energy costs per year with basic battery arbitrage operation
Energy costs per year with trained model operating battery in real-time

6. Keep improving the model with new data.
