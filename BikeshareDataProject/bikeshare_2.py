import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 1: 'chicago.csv',
              2: 'new_york_city.csv',
              3: 'washington.csv' }
cities_print = {1:'Chicago', 
                2:'New York City', 
                3:'Washington'}



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print("This is the list of available cities: \n1. Chicago\n2. New York City\n3. Washington")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    answ = input("Please select the city: ")
    while True:
    # this will try to convert the answer to an integer, if its fails i'll start a loop    
        try:
            int(answ)
        except:
            print("Invalid input: This is the list of available cities: \n1. Chicago\n2. New York City\n3. Washington")
            answ = input("City: ")
            continue
    # if the answer escape from that loop, it will verify the answer integer    
        else:
            while int(answ) != 1 and int(answ) != 2 and int(answ) != 3:
                print("Invalid input: This is the list of available cities: \n1. Chicago\n2. New York City\n3. Washington")
                answ = int(input("City: "))
        break
    
    city = CITY_DATA[int(answ)]

    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)

    print("Would you like to filter data by month, day, both, or not at all? Type 'none' to not apply any filter")
    filter_choose = ['month','day','both','none']
    user_choice = input()
    choice = user_choice.lower()
    while choice not in filter_choose:
        print("That's an invalid input, please select a filter again")
        user_choice = input()
        choice = user_choice.lower()

    if choice == 'month':
        print("Please select the month you want to apply the filter: \n1.January\n2.February\n3.March\n4.April\n5.May\n6.June\n7.All")
        month = int(input()) - 1
        day = 'all'
    elif choice == 'day':
        print("Please select the day you want to apply the filter: \n1.Monday\n2.Tuesday\n3.Wednesday\n4.Thursday\n5.Friday\n6.Satuday\n7.Sunday\n8.All")
        day = int(input())
        month = 'all'
    elif choice == 'both':
        """ In case the user choose both filters """
        print("Please select the month you want to apply the filter: \n1.January\n2.February\n3.March\n4.April\n5.May\n6.June\n7.All")
        month = int(input())
        print("Please select the day you want to apply the filter: \n1.Monday\n2.Tuesday\n3.Wednesday\n4.Thursday\n5.Friday\n6.Satuday\n7.Sunday\n8.All")
        day = int(input())
    else:
        """ When the user dont want to apply any filter """
        month = 'all'
        day = 'all'
    
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

    df = pd.read_csv(city)
    """ In here we use pandas to load the city file according the user input """


    df['Start Time'] = pd.to_datetime(df['Start Time'])
    """ Convert Start Time column, so we can get the month and day """
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.dayofweek
    if month != 'all':       
        df = df[df.month == month]
        

    if day != 'all':
        df = df[df.day == day - 1]

    print('-'*40)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['month'].apply(lambda x: calendar.month_name[x])
    frequent_month = df['month'].mode()[0]


    # display the most common day of week
    df['day'] = df['day'].apply(lambda x: calendar.day_name[x])
    frequent_day = df['day'].mode()[0]

    # display the most common start hour
    frequent_hour = df['Start Time'].dt.hour.mode()[0]

    print("The most frequent month is: {}".format(frequent_month))
    print("The most frequent day is: {} ".format(frequent_day))
    print("The most frequent hour is {} ".format(frequent_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    frequent_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    frequent_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    trip_counter = df.groupby(['Start Station','End Station']).size().reset_index(name = 'trips')
    sort_trips = trip_counter.sort_values('trips', ascending = False)
    freq_start = sort_trips['Start Station'].iloc[0]
    freq_end = sort_trips['End Station'].iloc[0]
    print("Most frequent start station is: {}".format(frequent_start_station))
    print("Most frequent ending station is: {}".format(frequent_end_station))
    print("Most popular trip is between station: {} and the station: {}".format(freq_start,freq_end))
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()

    # display mean travel time
    mean_time = df['Trip Duration'].mean()

    print("Total travel time is: {} ".format(total_time))
    print("Average travel time is: {}" .format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print("Calculating User stats..!")
    start_time = time.time()
   

    # Display counts of user types
    # print value counts for each user type
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print(user_types)
    else:
        print("Gender is not valid for this dataset")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        max_year = df['Birth Year'].max()

        print("Most Recent Birth Year is %s " % (max_year))

        min_year = df['Birth Year'].min()

        print("Most Earliest Birth Year is %s " % (min_year))

        freq_year = df['Birth Year'].mode()[0]

        print("Most Frequent Birth Year is %s " % (freq_year))
    else:
        print("Birth year is not valid for this dataset")

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

        #Asking for raw data
        #settings the row quantity to 0
        i_data = 0
        raw_answ = input("Would you like to see 5 rows of raw data? Type 'Yes' or 'No': ").lower()
        while True:
            options = ['yes' , 'no']
            if raw_answ not in options:
                raw_answ = input("Invalid input. Would you like to see 5 rows of raw data? Type 'Yes' or 'No': ").lower()
            elif raw_answ == 'yes':
                print(df.iloc[i_data:i_data+5])
                i_data += 5
                new_answ = input("Would you like to see 5 more rows? Type 'Yes' or 'No': ").lower()
                if new_answ == 'no':
                    break
            elif raw_answ == 'no':
                break     

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
