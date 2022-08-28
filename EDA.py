import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn

data = pd.read_csv('./Covid Data Analysis/all_weekly_excess_deaths.csv')   # a dot is compulsory
print("The shape of the dataframe :",data.shape)
print("The columns headings of the dataframe :")
print(data.columns)
print(data.info)
print(data['region_code'])    # Since region code is all zero we remove it from the table
data = data.drop(index=2, columns='region_code')
print(data.shape)
datacopy = data.copy()
# Storing integer based values of deaths in another dataframe
deaths = data[['total_deaths', 'covid_deaths', 'expected_deaths', 'excess_deaths', 'non_covid_deaths']]
print(deaths.shape)     # 5769 x 5
deaths = deaths.astype('int32')
print(deaths)
# Since we have each week of 7 days we remove the week column from the data
data = data.drop(index=7, columns='week')     
print(data.shape)        # 5768 x 15
# Storing time based data in interval data frame
interval = data[['days', 'year']]
data['start_date'] = pd.to_datetime(data['start_date'])
data['end_date'] = pd.to_datetime(data['end_date'])
# Changing format to date time index
data['month'] = pd.DatetimeIndex(data['start_date']).month

month_file = data.groupby('month')[['total_deaths', 'covid_deaths', 'expected_deaths', 'excess_deaths', 'non_covid_deaths']].sum()
year_file = data.groupby('year')[['total_deaths', 'covid_deaths', 'expected_deaths', 'excess_deaths', 'non_covid_deaths']].sum()

month_file = month_file / 10000
year_file = year_file / 100000
print("Month file :")
print(month_file)
print("Year file : ")
print(year_file)
# Making user understand that the ratio is of millions and ten thousand
year_file['death_millions'] = 'millions'
month_file['death_10k'] = 'TenThousand'
# Storing various columns as an Numpy array
td1 = np.array(month_file['total_deaths'])
cd1 = np.array(month_file['covid_deaths'])
td2 = np.array(year_file['total_deaths'])
cd2 = np.array(year_file['covid_deaths'])
mon = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
year = np.array([2020, 2021, 2022])

# Now Drawing the Graph
new_month_file = month_file[['total_deaths', 'covid_deaths']] / 10      # For Visualization purposes
print("The New Month File for Visualization Purposes is :")
print(new_month_file)
# Graph of Monthly Deaths in the Covid Pandemic
plt.bar(mon, new_month_file['total_deaths'], alpha=0.5, color='blue')
plt.bar(mon, new_month_file['covid_deaths'], alpha=0.8, color='red')
plt.title('Monthly Deaths')
plt.xlabel('Month')
plt.ylabel('Deaths in Lakhs')
plt.legend(['Total Deaths', 'Covid Deaths'])
plt.show()
# Graph of Yearly Deaths in the Covid Pandemic
new_year_file = year_file[['total_deaths', 'covid_deaths']] + 2
print("The new Year file for Visualization Purposes is :")
print(new_year_file)
plt.bar(year, new_year_file['total_deaths'], alpha=0.5, color='blue')
plt.bar(year, new_year_file['covid_deaths'], alpha=0.8, color='red')
plt.title('Yearly Deaths')
plt.xlabel('Year')
plt.ylabel('Deaths in Millions')
plt.legend(['Total Deaths', 'Covid Deaths'])
plt.show()

# Evaluating Ratio of Monthly and Yearly Deaths
new_month_file['ratio'] = new_month_file['total_deaths'] / new_month_file['covid_deaths']
new_year_file['ratio'] = new_year_file['total_deaths'] / new_year_file['covid_deaths']
ratio1 = max(new_month_file['ratio'])
ratio2 = max(new_year_file['ratio'])
if ratio1 > ratio2:
    print("The Monthly Covid ratio is larger, thus the Covid Deaths in the months have decreased")
if ratio1 < ratio2:
    print("The Yearly Covid ratio is larger, thus the Covid Deaths yearly have increased")
print(ratio1, ratio2)

'''1st Inference :- The Monthly Covid Death Ratio is larger than the Yearly Covid Death Ratio...'''
# Displaying the Subplots
plt.subplot(1, 2, 1)
plt.plot(new_month_file['ratio'], marker='o', color='orange', markerfacecolor='red', linestyle='solid')
plt.xlabel('Months')
plt.ylabel('Death Ratio')
plt.title("Monthly Covid Death Ratio")
plt.subplot(1, 2, 2)
plt.plot(new_year_file['ratio'], marker='o', color='orange', markerfacecolor='red', linestyle='solid')
plt.xlabel('Years')
plt.ylabel('Death Ratio')
plt.title('Yearly Covid Death Ratio')
plt.show()

death1 = data[['total_deaths', 'expected_deaths', 'excess_deaths']]
death1 = death1 / 10
print(death1)
d1 = np.array(death1['total_deaths'])
d2 = np.array(death1['expected_deaths'])
d3 = np.array(death1['excess_deaths'])
plt.plot(d2, color='blue', linestyle='solid')
plt.plot(d3, color='darkblue', linestyle='solid')
plt.show()

'''2nd Inference :- Coming to the end of 2021 and beginning of 2022, both the expected deaths and excess deaths rise exponentially within a short time... such that the peak of the Covid Disease came in the end of 2021...'''

a1 = data[['covid_deaths', 'non_covid_deaths', 'excess_deaths', 'expected_deaths']]
sn.pairplot(a1, hue='covid_deaths')
plt.show()
'''3rd Inference :- The Most Common Death in the later pandemic was due to Covid as there was a peak in the end pandemic season...'''