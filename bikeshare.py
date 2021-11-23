import time
import pandas as pd
import numpy as np
from datetime import date,datetime


# Dictionaries to help with some of the logic in the rest of the code.
city_data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = { 'january': ['01-01-2017 00:00:01', '01-31-2017 23:59:59', 0],
          'february': ['02-01-2017 00:00:01', '02-28-2017 23:59:59', 1],
          'march': ['03-01-2017 00:00:01', '03-31-2017 23:59:59', 2],
          'april': ['04-01-2017 00:00:01', '04-30-2017 23:59:59', 3],
          'may': ['05-01-2017 00:00:01', '05-31-2017 23:59:59', 4],
          'june': ['06-01-2017 00:00:01', '06-30-2017 23:59:59', 5],
          'all': ['01-01-2017 00:00:01', '12-31-2017 23:59:59', 12],
}

days = {'monday' : 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6,
        'all': 7}


# re-iniitialized variables to help with user input data later in the script.
city = ""
day = ""
month = ""


# helper functions to return day and month based on integer values from months and days
def return_day(intDay):
    for day in days:
        #print('day is {} and intDay is {} and days[day][0] is {}'.format(day, intDay, days[day]))
        if intDay == days.get(day):
            return day.capitalize()

def return_month(intMonth):
    for month in months:
        if intMonth - 1 == months[month][2]:
            return month.capitalize()

# Script to request the City, month, and if the user wants to check days.
# Exception handling to prevent obvious errors like wrong choices or capitalization
# Including logic to allow selection of all by clicking Enter or typing 'All'

def get_city():
    while True:
        try:
            city = str(input("Input one of the following cities:  New York City, Washington, or Chicago:  "))
            if city.lower() in city_data:
                print("Completed city capture")
                return city.lower()
                break
            else:
                print("You must enter the city as shown in the prompt.")
        except:
            print("you must enter a valid option as shown in the prompt")


def get_month():
    while True:
        try:
            month = str(input("Input a month between January and June you'd like to analyze or choose 'All': e.g.  January, February, May, All:  "))
            if month == "":
                month = "all"
                return month
                print("Completed month capture")
                break
            elif month.lower() in months:
                return month.lower()
                print("Completed month capture")
                break
            else:
                print("You must enter a month as shown in the prompt and select between January and June")
        except:
            print("you must enter a valid option as shown in the prompt")


def get_day():
    while True:
        try:
            day = str(input("[Optional] Select a day you'd like to specifically analyze:  Monday, Tuesday, All: "))
            if day == "":
                day = "all"
                return day
                break
            elif day.lower() in days:
                return day.lower()
                break
            else:
                print("you must enter a day as shown in the prompt")
        except:
            print("you must enter a valid option as shown in the prompt")

# Function to call helper functions to get month, city, and day information from user.

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
    city = get_city()

    # get user input for month (all, january, february, ... , june)
    month = get_month()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_day()

    print('-'*40)
    return city, month, day

# master function to pull information from the user to input into pandas filters.

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

    file_name = city.replace(" ", "_") + ".csv"
    print("loading {} file".format(file_name))
    file = pd.read_csv('./' + file_name)
    # create start and end time filters based on user input.
    start = datetime.strptime(months[month][0], '%m-%d-%Y %H:%M:%S')
    finish = datetime.strptime(months[month][1], '%m-%d-%Y %H:%M:%S')
    file['Start Time'] = pd.to_datetime(file['Start Time'], format='%Y-%m-%d %H:%M:%S')
    # create data frame using start and end time filters.
    df = file[(file["Start Time"] >= start) & (file["Start Time"] <= finish)]

    # create a weekday, month, and hour column to help with later filtering of dataframe.
    df['Weekday'] = df['Start Time'].dt.dayofweek
    df['Month'] = df['Start Time'].dt.month
    df['Hour'] = df['Start Time'].dt.hour

    # check for if user has selected a particular day or if they're looking at all.  Filter accordingly and return dataframe.
    if day != "all":
        print("You've selected a particular day - {}".format(days[day]))
        return df[df['Weekday'] == days[day]]

    else:
        print("You've selected all days")
        return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()



    # display the most common month
    print('Most common month of travel in this dataset is: {}'.format(return_month(int(df['Month'].mode()[0]))))

    # display the most common day of week
    print('Most common day of the the week people traveled in this dataset is:  {}'.format(return_day(int(df['Weekday'].mode()[0]))))

    # display the most common start hour
    print('The most common start hour of the day for travelers in this dataset is {}'.format(df['Hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is:  {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most commonly used end station is:  {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    most_common_combo = df.groupby(['Start Station', 'End Station']).count().sort_values(by=['Start Station', 'End Station'], ascending = (False, False))
    new_most_common_combo = df.groupby(['Start Station', 'End Station']).count().sort_values(by=['Start Station', 'End Station'], ascending = (False, False))
    most_common_is = df.sort_values(by='Unnamed: 0', ascending = False).head(1)
    startLoc = most_common_is.iloc[0]['Start Station']
    endLoc = most_common_is.iloc[0]['End Station']
    print('the most frequent combination of start station and end station for trips is from {} and ends at {}'
    .format(startLoc, endLoc))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration_days = round(df['Trip Duration'].sum() / 86400, 2)
    print('Total travel time is: {} days'.format(total_duration_days))

    # display mean travel time
    mean_travel_time_hours = round(df['Trip Duration'].mean()/360, 2)
    print('Average travel time is: {} hours'.format(mean_travel_time_hours))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Total subscribers:\n {}".format(df["User Type"].value_counts()))

    # Display counts of gender
    print("Users by gender:\n{}".format(df["Gender"].value_counts()))

    # Display earliest, most recent, and most common year of birth
    print("Earliest birth year: {}\nMost recent birth year: {}\nMost common birth year: {}"
            .format(int(df["Birth Year"].min()), int(df["Birth Year"]
            .max()), int(df["Birth Year"].mode().max())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# Main function allowing running of helper functions and controlling flow of logic.

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print(df.head)
        print(df.shape)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if city != "washington":
            user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break

# Function to allow user to step through raw rows of filtered data in DataFrame
def raw_data(df):
    cont = ""
    start = 0
    end = 5
    while cont.lower() != 'no' and end <= df.shape[0] - 1:

        cont = input("Do you want to see raw data? (Type 'no' to stop): ")
        if cont == 'no':
            break
        else:
            print(df.iloc[start:end,:])
            start += 5
            end += 5

if __name__ == "__main__":
	main()
