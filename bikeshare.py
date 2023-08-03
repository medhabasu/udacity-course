
from datetime import datetime
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = ['chicago', 'new york city', 'washington']
months = ['all','january', 'february', 'march', 'april', 'may','june']
days = ['monday', 'tuesday','wednesday','thursday','friday','saturday', 'sunday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    entered_valid_city = False
    while not entered_valid_city:
        city = input("Select a city: {} \n".format(', '.join(cities).title()))
        if city.lower() in cities:
            entered_valid_city = True
        else:
            print("Sorry, city must be one of {}\n".format(', '.join(cities).title()))


    # get user input for month (all, january, february, ... , june)
    entered_valid_month = False
    while not entered_valid_month:
        month = input("Select a month or 'all' to choose all months: {}\n".format(', '.join(months)).title())
        if month.lower() in months:
            entered_valid_month = True
        else:
            print("Sorry, the month selection must be 'all' or one of {} \n".format(', '.join(months).title()))
    


    # get user input for day of week (all, monday, tuesday, ... sunday)
    entered_valid_day = False
    while not entered_valid_day:
        day = input("Select a day of the week or 'all' to view all days: {}\n".format(', '.join(days).title()))
        if day.lower() in days:
            entered_valid_day = True
        else:
            print("Sorry, the day selection must be 'all' or one of {}\n".format(', '.join(days).title()))
    

    print('Thank you. You have selected data for: \nCity: {}\nMonth: {}\nDay: {}.'.format(city.title(), month.title(), day.title()))

    city = city.lower()
    month = months.index(month)
    day = days.index(day)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city], parse_dates=True)
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    df['dow'] = pd.DatetimeIndex(df['Start Time']).dayofweek
    if month != 0:
        df = df[df['month'] == month]
    if day != 7:
        df = df[df['dow'] == day]

    return df


def view_data(df):
    """Displays raw data for the specific city and filters."""

    row = 0
    while row < df.shape[0]:
        if row == 0:
            view = input('\nWould you like to see the first 5 lines of the raw data? Enter yes or no.\n')
        else:
            view = input('\nWould you like to see the next five lines? Enter yes or no.\n')
        
        if view.lower() == 'yes':
            print(df.iloc[row:row+5])
            row += 5
        else:
            print('\nThank you. We will now show you data on travel times, trips and users for the city, months and days you have selected.')
            break


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 0:
        common_month = df['month'].value_counts()
        # common_month_count = common_month.iloc[0]
        common_month = common_month.index[0]
        print('\nThe most popular month was {}, with a total of {} trips.'.format(months[common_month].title(), common_month.iloc[0]))

    # display the most common day of week
    if day == 7:
        common_dow = df['dow'].value_counts()
        # common_dow_count = common_dow.iloc[0]
        common_dow = common_dow.index[0]
        print('\nThe most popular day of the week was {}, with a total of {} trips.'.format(days[common_dow].title(), common_dow.iloc[0]))


    # display the most common start hour
    df['hour'] = pd.DatetimeIndex(df['Start Time']).hour
    common_hour = df['hour'].value_counts()
    # common_hour_count = common_hour.iloc[0]
    # common_hour = common_hour.index[0]
    print('\nThe most popular hour of the day was {}:00, with a total of {} rides.'.format(common_hour.index[0], common_hour.iloc[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start = df['Start Station'].value_counts()
    print('\nThe most popular start station was {}, with a total of {} rides'.format(pop_start.index[0], pop_start.iloc[0]))


    # display most commonly used end station
    pop_end = df['End Station'].value_counts()
    print('\nThe most popular end station was {}, with a total of {} rides'.format(pop_end.index[0], pop_end.iloc[0]))


    # display most frequent combination of start station and end station trip
    pop_combo = df[['Start Station','End Station']].value_counts()
    print('\nThe most popular trip taken was from {}, with a total of {} rides'.format(' to '.join(pop_combo.index[0]), pop_combo.iloc[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time /= 3600
    print("\nThe total travel time was {} hours.".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time /= 60
    print('\nThe average trip duration was {} minutes.'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print("\nThere are two types of users: {} are {}s and {} are {}s.".format(user_type.iloc[0], user_type.index[0], user_type.iloc[1], user_type.index[1]))

    # Display counts of gender. Not available for Washington.
    if city != 'washington':
        gender_count = df['Gender'].value_counts()
        print('\nThere are {} {}s and {} {}s.'.format(gender_count.iloc[0], gender_count.index[0], gender_count.iloc[1], gender_count.index[1]))

    # Display earliest, most recent, and most common year of birth. Not available for Washington.
    if city != 'washington':
        earliest_dob = int(df['Birth Year'].min())
        latest_dob = int(df['Birth Year'].max())
        common_dob = int(df['Birth Year'].mode().iloc[0])
        print('\nThe earliest year of birth was {} and the most recent was {}. The most common year of birth was {}.'.format(earliest_dob, latest_dob, common_dob))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        view_data(df)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
 	main()


