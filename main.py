import pandas as pd
import matplotlib.pyplot as plt

# Import csv files to dataframe
confirmed = pd.read_csv('covid19_confirmed.csv')
deaths = pd.read_csv('covid19_deaths.csv')
recovered = pd.read_csv('covid19_recovered.csv')

# Dropping the columns not needed
confirmed = confirmed.drop(['Province/State', 'Lat', 'Long'], axis=1)
deaths = deaths.drop(['Province/State', 'Lat', 'Long'], axis=1)
recovered = recovered.drop(['Province/State', 'Lat', 'Long'], axis=1)

# grouping by country
confirmed = confirmed.groupby(confirmed['Country/Region']).aggregate('sum')
deaths = deaths.groupby(deaths['Country/Region']).aggregate('sum')
recovered = recovered.groupby(recovered['Country/Region']).aggregate('sum')

# Row - Column exchanges places
confirmed = confirmed.T
deaths = deaths.T
recovered = recovered.T

#Calculate the increase of cases per day
new_cases = confirmed.copy()

# Cases today - Cases yesterday
# len(confirmed) corresponds to number of rows of the dataframe
for day in range(1, len(confirmed)):
    new_cases.iloc[day] = confirmed.iloc[day] - confirmed.iloc[day - 1]

# Calculates the growth rate per day using the new_cases from the previous loop
growth_rate = confirmed.copy()

for day in range(1, len(confirmed)):
    growth_rate.iloc[day] = (new_cases.iloc[day] / confirmed.iloc[day - 1]) * 100


active_cases = confirmed.copy()
# Starting from 0 as we do not have to go one day back
# Only interested from the particular day
for day in range(0, len(confirmed)):
    active_cases.iloc[day] = confirmed.iloc[day] - deaths.iloc[day] - recovered.iloc[day]


overall_growth_rate = confirmed.copy()
# Overall growth rate at certain day is based on the actual cases
for day in range(1, len(confirmed)):
    overall_growth_rate.iloc[day] = ((active_cases.iloc[day] - active_cases.iloc[day-1]) / active_cases.iloc[day - 1]) * 100

overall_growth_rate = confirmed.copy()

for day in range(0, len(confirmed)):
    overall_growth_rate.iloc[day] = (deaths.iloc[day] / confirmed.iloc[day]) * 100


countries = ['Bangladesh']

# Adding visualization

for country in countries:
    ax = plt.subplot()
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_title(f'COVID-19 - Overall Active Growth Rate [{country}]', color='white')
    overall_growth_rate[country][30:].plot.bar()
    plt.show()