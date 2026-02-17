import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_NAMES = ('all', 'january', 'february', 'march', 'april', 'may', 'june')

WEKKDAY_NAMES = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = None
    month = None
    day = None
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while (city not in CITY_DATA):
        city = input("Please enter a city name (chicago, new york city, washington):").lower()

    # get user input for month (all, january, february, ... , june)
    while (month not in MONTH_NAMES):
        month = input("Please enter a month name (all, january, february, ... , june):").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while (day not in WEKKDAY_NAMES):
        day = input("Please enter a day name (all, monday, tuesday, ... sunday):").lower()

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
    df=pd.read_csv(CITY_DATA[city], sep=',', parse_dates=['Start Time', 'End Time'])
    if (month != 'all'):
        month_index = MONTH_NAMES.index(month)
        df = df[df['Start Time'].dt.month == month_index]

    if (day != 'all'):
        day_index = WEKKDAY_NAMES.index(day)
        df = df[df['Start Time'].dt.weekday == day_index - 1]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_comon_month = np.bincount(df['Start Time'].dt.month).argmax()
    print(f"The most common month of travel is {MONTH_NAMES[most_comon_month]}.")

    # display the most common day of week
    most_common_dow = np.bincount(df['Start Time'].dt.weekday).argmax()
    print(f"The most common day of the week for travel is {WEKKDAY_NAMES[most_common_dow + 1]}.")

    # display the most common start hour
    most_common_start_hour = np.bincount(df['Start Time'].dt.hour).argmax()
    print(f"The most common start hour for travel is {most_common_start_hour:02} o'clock.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    unique_starts = np.unique(df['Start Station'], return_counts=True)
    most_common_start = unique_starts[0][unique_starts[1].argmax()]
    print(f"The most commonly used start station is {most_common_start}.")

    # display most commonly used end station
    unique_ends = np.unique(df['End Station'], return_counts=True)
    most_common_end = unique_ends[0][unique_ends[1].argmax()]
    print(f"The most commonly used end station is {most_common_end}.")

    # display most frequent combination of start station and end station trip
    start_end_combinations = df.apply(lambda row: (row['Start Station'], row['End Station']), axis=1)
    most_common_start_end = start_end_combinations.value_counts().idxmax()
    print(f"The most frequent combination of start station and end station trip is {most_common_start_end}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Trip Duration'] = (df['End Time'] - df['Start Time']).dt.total_seconds()
    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"The total travel time is {total_travel_time} seconds.")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"The mean travel time is {mean_travel_time} seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    for user_type, user_count in user_types.items():
        print(f'User Type {user_type}: {user_count}')

    # Display counts of gender
    gender_counts = df['Gender'][df['Gender'] != ''].value_counts()
    for gender, gender_counts in gender_counts.items():
        print(f'Gender {gender}: {gender_counts}')

    # Display earliest, most recent, and most common year of birth
    year_of_birth = df['Birth Year'][df['Birth Year'] != 0]
    earliest_yob = year_of_birth.min()
    latest_yob = year_of_birth.max()
    most_common_yob = year_of_birth.value_counts().idxmax()
    print(f'Year of Birth: earliest: {earliest_yob}, most recent: {latest_yob}, most common: {most_common_yob}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
