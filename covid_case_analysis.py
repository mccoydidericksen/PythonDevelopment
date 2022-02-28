import requests
import pandas as pd
import datetime
import json

# ------------------------------------------------------------------------------
# coverts response json to pandas dataframe and swaps index and columns (transpose),
# then renames columns and sorts rows by date asc, drops off anything after 12/31/21
# ------------------------------------------------------------------------------
def format_json(resp):
    covid_df = pd.DataFrame(resp['All']['dates'], index=[0]).transpose().reset_index()
    covid_df.rename(columns={0: 'total_cases', 'index': 'date'}, inplace=True)
    covid_df.sort_values('date', inplace=True)
    covid_df = covid_df[covid_df['date'] <= '2021-12-31'].reset_index(drop=True)
    covid_df['date'] = pd.to_datetime(covid_df['date'])
    covid_df['year'] = pd.DatetimeIndex(covid_df['date']).year
    covid_df['month'] = pd.DatetimeIndex(covid_df['date']).month
    covid_df['day'] = pd.DatetimeIndex(covid_df['date']).day
    covid_df = covid_df[['date', 'year', 'month', 'day', 'total_cases']]

    return covid_df

# ------------------------------------------------------------------------------
# Calculates new daily cases and required stats for day level and month level
# ------------------------------------------------------------------------------
def calculate_stats(covid_df, country):
    # calcualtes new cases by taking currnet row total_cases minus the row previous (shift)
    covid_df['new_cases'] = covid_df['total_cases'] - covid_df['total_cases'].shift()
    covid_df['new_cases'] = covid_df['new_cases'].fillna(0).astype(int)
    # calcualtes day level stats
    avg_daily = round(covid_df['new_cases'].mean(), 2)
    max_new = covid_df['new_cases'].max()
    max_new_date = covid_df.loc[covid_df['new_cases'] == max_new, 'date'].item().strftime('%Y-%m-%d')
    max_new_date_str = max_new_date + ' (new cases: ' + str(max_new) + ')'
    # creates dataframe where new_cases are 0 or less and gets the most recent date
    zero_cases = covid_df[covid_df['new_cases'] <= 0].sort_values('date', ascending=False).reset_index(drop=True)
    recent_zero_dt = zero_cases.loc[0, 'date'].strftime('%Y-%m-%d')
    # groups dataframe by year and month and sums new_cases to calculate month level stats
    month_df = covid_df.drop(columns={'date', 'day', 'total_cases'})
    month_df = month_df.groupby(['year', 'month']).sum().reset_index()
    month_max_new = month_df['new_cases'].max()
    month_max_new_date_year = month_df.loc[month_df['new_cases'] == month_max_new, 'year'].item()
    month_max_new_date_month = datetime.datetime.strptime(str(month_df.loc[month_df['new_cases'] == month_max_new, 'month'].item()), '%m').strftime("%B")
    month_max_new_date_str = month_max_new_date_month + ' of ' + str(month_max_new_date_year) + ' (new cases: ' + str(month_max_new) + ')'
    month_min_new = month_df['new_cases'].min()
    month_min_new_date_year = month_df.loc[month_df['new_cases'] == month_min_new, 'year'].item()
    month_min_new_date_month = datetime.datetime.strptime(str(month_df.loc[month_df['new_cases'] == month_min_new, 'month'].item()), '%m').strftime("%B")
    month_min_new_date_str = month_min_new_date_month + ' of ' + str(month_min_new_date_year) + ' (new cases: ' + str(month_min_new) + ')'
    stats_data = {'country': country, 'avg_daily': avg_daily, 'max_new_date': max_new_date_str,
    'recent_zero_dt': recent_zero_dt, 'month_max_new_date': month_max_new_date_str, 'month_min_new_date': month_min_new_date_str}

    return stats_data

# ------------------------------------------------------------------------------
# Prints output stats to console
# ------------------------------------------------------------------------------
def output_stats(stats_data):
    print('-----------------------------------------------')
    print('COVID CONFIRMED CASES STATS')
    print('-----------------------------------------------')
    print('Country Name: ' + stats_data['country'])
    print('Average number of new daily confirmed cases for the entire dataset: ' + str(stats_data['avg_daily']))
    print('Date with the highest new number of confirmed cases: ' + stats_data['max_new_date'])
    print('Most recent date with no new confirmed cases: ' + stats_data['recent_zero_dt'])
    print('Month with the highest new number of confirmed cases: ' + stats_data['month_max_new_date'])
    print('Month with the lowest new number of confirmed cases: ' + stats_data['month_min_new_date'])

# ------------------------------------------------------------------------------
# Stores country covid stats in json
# ------------------------------------------------------------------------------
def stats_to_json(stats_data):
    with open(stats_data['country'] + '.json', 'w') as f:
        json.dump(stats_data, f, ensure_ascii=False)

# ------------------------------------------------------------------------------
# Main loop to get country covid data and call transform & load functions
# ------------------------------------------------------------------------------
country_list = ['US', 'Russia', 'Germany']
for country in country_list:
    request_url = 'https://covid-api.mmediagroup.fr/v1/history?country=' + country + '&status=confirmed'
    resp = requests.get(request_url).json()
    covid_df = format_json(resp)
    stats_data = calculate_stats(covid_df, country)
    output_stats(stats_data)
    stats_to_json(stats_data)

