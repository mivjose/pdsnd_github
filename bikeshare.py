
import time
import math
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = { 'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may':5, 'june': 6, 'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6}

WEEK_DATA = { 'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6,'mon': 0, 'tues': 1, 'wed': 2, 'thur': 3, 'fri': 4, 'sat': 5, 'sun': 6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print()
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while 1:
        city = input('Please select a city whose data you want to analyse, either: Chicago/CH, New York City/NYC, or Washington/WA\n').lower()
        print()
        if city=='ch':
            city='chicago'
        elif city=='ny' or city=='nyc':
            city='new york city'
        elif city=='wa' or city=='washington dc':
            city='washington'
        else:
            if city not in CITY_DATA:
                print('Please enter a valid city')
                continue
            city = CITY_DATA[city]
        break
    # TO DO: get user input for month (all, january, february, march, april, may, june)
    # TO DO: get user input for day of week (all, monday, tuesday, wednesday, ... sunday)
    while 1:
        choice = input('Do you want to filter the data by month and week? Yes/No\n').lower()
        print()
        if choice=='yes' or choice=='y':
            choice=True
        elif choice=='no' or choice=='n':
            choice=False
        else:
            print('Please enter a valid choice.')
            continue
        break

    while 1:
        if choice:
            filter=input('You can filter by month / day / both ').lower()
            print()
            if filter=='month':
                print('Which month\'s data do you want to analyse?\n')
                month = input('January/jan, February/feb, March/mar, April/apr, May, June/jun- \n').lower()
                print()
                if month not in MONTH_DATA:
                    print('Please enter a month from the above list?')
                    continue
                month = MONTH_DATA[month]
                day='all'
            elif filter=='day':
                print('Which day\'s data do you want to analyse? ')
                day = input('Monday/mon, Tuesday/tues, Wednesday/wed, Thursday/thur, Friday/fri, Saturday/sat, Sunday/sun- \n').lower()
                print()
                if day not in WEEK_DATA:
                    print('Please select a day from the above list:')
                    continue
                day = WEEK_DATA[day]
                month='all'
            elif filter=='both':
                print('Which month\'s data do want to analyse?')
                month = input('January/jan, February/feb, March/mar, April/apr, May, June/jun- \n').lower()
                print()
                if month not in MONTH_DATA:
                    print('please select a month from the list above')
                    continue
                month = MONTH_DATA[month]
                print('And day of the week?')
                day = input('Monday/mon, Tuesday/tues, Wednesday/wed, Thursday/thur, Friday/fri, Saturday/sat, Sunday/sun- \n').lower()
                print()
                if day not in WEEK_DATA:
                    print('Please select a valid day of the week from the list')
                    continue
                day = WEEK_DATA[day]
            else:
                print('Please enter a valid input')
                continue
            break
        else:
            day='all'
            month='all'
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
    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month]

        # user filters by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    popular_month = df['month'].mode()[0]
    print('The most common month is: {}'.format(popular_month))

    # TO DO: display the most common day of week

    popular_day = df['day_of_week'].mode()[0]
    print('The most common day is: {}'.format(popular_day))


    # TO DO: display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common hour is: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station

    common_start_station = df['Start Station'].value_counts().idxmax()
    print('The most commonly used start station is: {}'.format(common_start_station))


    # TO DO: display most commonly used end station

    common_end_station = df['End Station'].value_counts().idxmax()
    print('\nThe most Commonly used end station is: {}'.format(common_end_station))


    # TO DO: display most frequent combination of start station and end station trip

    frequently_combined_station = df.groupby(['Start Station', 'End Station']).count()
    print('\nThe most frequently combined start and end station trips are:',common_start_station, " & ", common_end_station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    total_travel_time = sum(df['Trip Duration'])
    print('Total travel time:', total_travel_time/86400, " Days")


    # TO DO: display mean travel time

    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time/60, " Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    #print(user_types)
    print('User Types:\n', user_types)

    # TO DO: Display counts of gender

    try:
      gender_types = df['Gender'].value_counts()
      print('\nGender Types:\n', gender_types)
    except KeyError:
      print("\nGender Types:\nNo data available for this month.")

    # TO DO: Display earliest, most recent, and most common year of birth

    try:
      Earliest_Year = df['Birth Year'].min()
      print('\nThe Earliest Year is:', Earliest_Year)
    except KeyError:
      print("\nThe Earliest Year:\nNo data available for this month.")

    try:
      Most_Recent_Year = df['Birth Year'].max()
      print('\nThe most Recent Year is:', Most_Recent_Year)
    except KeyError:
      print("\nThe most Recent Year is:\nNo data available for this month.")

    try:
      Most_Common_Year = df['Birth Year'].value_counts().idxmax()
      print('\nThe most Common Year is:', Most_Common_Year)
    except KeyError:
      print("\nThe most Common Year is:\nNo data available for this month.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    choice = input('Would you like to read some of the raw data? Yes/No ').lower()
    print()
    if choice=='yes' or choice=='y' or choice=='yus':
        choice=True
    elif choice=='no' or choice=='n' or choice=='nope':
        choice=False
    else:
        print('You did not enter a valid choice. Let\'s try that again. ')
        display_data(df)
        return

    if choice:
        while 1:
            for i in range(5):
                print(df.iloc[i])
                print()
            choice = input('Another five? Yes/No ').lower()
            if choice=='yes' or choice=='y' or choice=='yus':
                continue
            elif choice=='no' or choice=='n' or choice=='nope':
                break
            else:
                print('You did not enter a valid choice.')
                return

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        print()
        if restart != 'yes' and restart != 'y':
            break

if __name__ == "__main__":
	main()
