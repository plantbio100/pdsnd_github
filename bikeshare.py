import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). Changes input to lower to prevent errors.

    while True:
        city = input("Choose which city to explore, Chicago, New York City, or Washington. ").lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print("That's not a valid response. Please pick one of these three cities: Chicago, New York City, or Washington.")
        else:
            break

    # get user input for month (all, january, february, ... , june). Changes input to lower to prevent errors.
    while True:
        month = input("Choose a month to explore - January, February, March, April, May, June, or all. ").lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print("/n That's not a valid response. Please pick one of these six months - January, February, March, April, May, June, or type all.")
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday). Changes input to lower to prevent errors.
    while True:
        day = input("Choose a day of the week to explore (e.g., Monday, Tuesday, Wednesday...), or type all. ").lower()
        if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            print("/n That's not a valid response. Please pick one of these seven days - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or type all.")
        else:
            break

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    print(df.head())
    print(df.columns.values.tolist())

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print("The most popular month was ", popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most popular day was ", popular_day)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("The most popular start hour was ", popular_hour)

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    print("The most popular hour was ", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Frequent_combo creates a new column which contains both the start and 
    end station in order to find the most popular combination

    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print("\nThe most popular Start Station was ", popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print("\nThe most popular End Station was ", popular_end)

    # display most frequent combination of start station and end station trip
    df['combo'] = df['Start Station'] + " x " + df['End Station']
    frequent_combo = df['combo'].mode()[0]
    print("\nThe most popular combination was ", frequent_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Travelers used the bikeshare system for a total of ", (df['Trip Duration'].sum()/360), " hours.")


    # display mean travel time
    print("Travelers used the bikeshare system for an average of ", (df['Trip Duration'].mean()/60), " minutes.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        print('\nUser types\n ' , df['User Type'].value_counts())
    else:
        print('\nNo User type data was collected for this city.\n')

    # If gender data is available, display counts of gender
    if 'Gender' in df.columns:
        print('\nGender count:\n ' , df['Gender'].value_counts())
    else:
        print('\nNo gender data was collected for this city.\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nEarliest birth year:\n ', df['Birth Year'].min())
        print('\nMost recent birth year:\n ', df['Birth Year'].max())
        print('\nMost common birth year:\n ', df['Birth Year'].mode())
    else:
        print('\nNo birth year data was collected for this city.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Asks the user if they want to see the raw data."""

    rowNum = 0

    user_response = input("\n Would you like to see five rows of the raw data? Please write 'yes' or 'no' \n").lower()

    while True:
        if user_response == 'no':
            break

        if user_response == 'yes':
            print(df[rowNum: rowNum + 5])
            rowNum = rowNum + 5
            user_response = input("\n Would you like to see five more rows of the raw data? Please write 'yes' or 'no' \n").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
