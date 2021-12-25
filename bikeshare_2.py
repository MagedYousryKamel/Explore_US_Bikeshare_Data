import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'september', 'october', 'november', 'december']

WEEKDAY_DATA = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']



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
    cities = ''
    months = ''
    days = ''
    while cities.lower() not in CITY_DATA: 
        cities = input('What is the name of the city that you want to analyze ?  (Chicago, Washington, New York)')
        if cities.lower() in CITY_DATA:
            city = CITY_DATA[cities.lower()]
            print('Thank you for filtering by city: ',city.title())
        else:
            print('Sorry couldn\'t filter by this name, please write city name as following " Chicago, Washington, New York"')

    # get user input for month (all, january, february, ... , june)

    while months.lower() not in MONTH_DATA:
        months = input ('Write the name of the month that you\'d like to filter by or write "all"')
        if months.lower() in MONTH_DATA:
            month = months.lower()
        else:
            print('Sorry, please type either "all" for no filters or month name to filter by ( january, february, march,... etc)')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while days.lower() not in WEEKDAY_DATA:
        days = input('Write the day name that you\'d like to filter by or write "all"')
        if days.lower() in WEEKDAY_DATA:
            day = days.lower()
        else:
            print('Sorry, please type either "all" for no filters by week day or write day name (Sunday, Monday, Tuesday,.. etc)')

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
    df = pd.read_csv(city)  # loads file into DataFrame
    df['Start Time'] = pd.to_datetime(df['Start Time']) # converts start time into datatime

    df['month'] = df['Start Time'].dt.month # gets the month from the datatime
    df['weekday'] = df['Start Time'].dt.day_name() # get the weekday name from the datatime
    df['hour'] = df['Start Time'].dt.hour # get the hour from the datatime.

    #Filters : 

    if month != 'all':
        month = MONTH_DATA.index(month)
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['weekday'] == day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print("The most common month is: " + MONTH_DATA[common_month].title())


    # display the most common day of week
    common_day_of_week = df['weekday'].mode()[0]
    print("The most common day of week is: " + str(common_day_of_week))


    # display the most common start hour


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is: " + common_start_station)


    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is: " + common_end_station)


    # display most frequent combination of start station and end station trip
    frequent_combination = (df['Start Station'] + " & " + df['End Station']).mode()[0]
    print("The most frequent combination of start station and end station trip is : " + str(frequent_combination.split("&")))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time from the given fitered data is: " + str(total_travel_time))


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time is: " + str(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if 'Gender' in df:
        genders = df['Gender'].value_counts()
        print(genders)
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        most_common_birth = df['Birth Year'].mode()[0]
        print('Earliest birth year is: {}\n'.format(int(earliest_birth)))
        print('Most recent birth year is: {}\n'.format(int(most_recent_birth)))
        print('Most common birth year is: {}\n'.format(int(most_common_birth)))
    else:
        print('Birth Year stats cannot be calculated because Birth Year doesnt appear in the dataframe')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data on user request.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    print(df.head(5))
    next = 0
    while True:
        view_raw_data = input('\nWould you like to view next five row of raw data? Enter yes or no.\n')
        if view_raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next+5])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
