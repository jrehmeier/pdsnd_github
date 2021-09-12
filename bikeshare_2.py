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
    last_check = "n"
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    while last_check != "y":
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        check_city = "n"
        while check_city != "y":
            city = str(input("Enter the name of the city you'd like to look at data for ('chicago', 'new york city', or 'washington'): "))
            try:
                city = city.strip().lower()
                if city == "chicago" or city == "new york city" or city == "washington":
                    check_city = "y"
                else:
                    print("Please check your spelling and enter one of the three listed cities: chicago, new york city, or washington.")
            #check = "n"
                #check = str(input("Are you sure you want to look at {} (y/n)?".format(city)))
            except:
                print("Error: Please check your spelling and enter one of the three listed cities: chicago, new york city, or washington.")
                continue


    # get user input for month (all, january, february, ... , june)
    #
        check_month = "n"

        while check_month != "y":
            month = str(input("Enter a month from january to june (inclusive) or enter 'all' to look at all months: "))
            try:
                month = month.strip().lower()
                if month in months or month == 'all':
                    check_month = "y"
                else:
                    print("Please check your spelling and enter one of the following months: {}, or enter 'all' to view data for all months".format(months))
            #check = "n"
                #check = str(input("Are you sure you want to look at {} (y/n)?".format(city)))
            except:
                print("Error: Please check your spelling and enter one of the following months: {}, or enter 'all' to view data for all months".format(months))
                continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
        check_day = "n"

        while check_day != "y":
            day = str(input("Enter a day of the week from monday to sunday (inclusive) or enter 'all' to look at all days of the week: "))
            try:
                day = day.strip().lower()
                if day in days or day == 'all':
                    check_day = "y"
                else:
                    print("Please check your spelling and enter one of the following days: {}, or enter 'all' to view data for all days of the week".format(days))
            #check = "n"
                #check = str(input("Are you sure you want to look at {} (y/n)?".format(city)))
            except:
                print("Error: Please check your spelling and enter one of the following days: {}, or enter 'all' to view data for all days of the week".format(days))
                continue
        check_all = "n"
        while check_all != "y":
            try:
                check_all = str(input("Are you sure you want to look at data for the city of {} from {} (months) on {} (days)? (Enter 'y' or 'n'): ".format(city, month, day)))
                check_all = check_all.strip().lower()
                if check_all == "n":
                    check_city = "n"
                    check_month = "n"
                    check_day = "n"
                    break
                elif check_all == "y":
                    last_check = "y"
                else:
                    print("Please enter only 'y' or 'n' (without the quotation marks)")
            except:
                print("Error: Please enter only 'y' or 'n' (without the quotation marks)")

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
    filename = CITY_DATA[city]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    df = pd.read_csv(filename)
    # need to get dataframe set up for filtering
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def raw_data(df):
    """Asks if user would like to see 5 rows of raw data at a time"""

    raw_data = str(input('Would you like to see the first 5 lines of raw data? ("y" or "n"): '))
    if raw_data == 'y' or raw_data == 'yes':
        user_check = 'n'
        i = 0
        time_out = time.time() + 15
        while user_check != 'y' and time.time() < time_out:
            while i < (len(df)):
                pd.set_option('display.max_columns',20)
                print(df.iloc[i:i+5])
                time_out = time.time() + 30
                i += 5
                repeat = str(input('Do you want to see the next 5 lines? (y or n): '))
                if repeat == "y" or repeat == "yes":
                    continue
                else:
                    user_check = "y"
                    break

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    try:
    # display the most common month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        common_month = df['month'].mode()[0]
        print("The most common month for travelling was: {}".format(months[common_month - 1].title()))
    # display the most common day of week
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
        common_day = df['day_of_week'].mode()[0]
        print("The most common day for travelling was: {}".format(days[common_day].title()))
    # display the most common start hour
        common_hour = df['hour'].mode()[0]
        print("The most common start hour (0-23) for travelling was: {}".format(common_hour - 1))
    except:
        print("No data for this combination of inputs.")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    try:
    # display most commonly used start station
        pop_start_station = df['Start Station'].mode()[0]
        print("Most popular station to start from: {}".format(pop_start_station))

    # display most commonly used end station
        pop_end_station = df['End Station'].mode()[0]
        print("Most popular station to end at: {}".format(pop_end_station))

    # display most frequent combination of start station and end station trip
        df['combo'] = df['Start Station'] + " to " + df['End Station']
        pop_trip = df['combo'].mode()[0]
        print("Most popular trip is: {}".format(pop_trip))
    except:
        print("No data for this combination of inputs.")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    try:
    # display total travel time
        travel_days = (df['Trip Duration'].sum())//(3600*24)
        travel_hours = (((df['Trip Duration'].sum())/(3600*24))-travel_days)*24
        travel_minutes = (travel_hours - int(travel_hours))*60
        travel_sec = (travel_minutes - int(travel_minutes))*60

        print("Sum of all trips in the selected time frame is: {} days, {} hours, {} minutes, and {} seconds.".format(travel_days, int(travel_hours), int(travel_minutes), int(travel_sec)))

    # display mean travel time
        avg_hours = df['Trip Duration'].mean()/3600
        avg_min = (avg_hours - int(avg_hours))*60
        avg_sec = (avg_min - int(avg_min))*60

        print("Average travel time is: {} hours, {} minutes, and {} seconds.".format(int(avg_hours), int(avg_min), int(avg_sec)))
    except:
        print("No data for this combination of inputs.")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    if df.empty:
        print("No data for this combination of inputs.")
    else:
        try:
    # Display counts of user types
            if df['User Type'].isnull().any():
                df['User Type'].fillna('Unknown', inplace = True)
            else:
                print('No unknown User Types')
            print(df['User Type'].value_counts())

    # Display counts of gender
            try:
                if df['Gender'].isnull().any():
                    df['Gender'].fillna('No response', inplace = True)
                else:
                    print('No unknown Genders')
                print(df['Gender'].value_counts())
            except:
                print("No column for 'Gender'")

    # Display earliest, most recent, and most common year of birth
            try:
                if df['Birth Year'].isnull().any():
                    df['Birth Year'].fillna(0)
                else:
                    print("No unkown Birth Years")
                print('The earliest Birth Year is: {}'.format(int(df['Birth Year'].min())))
                print('The most recent Birth Year is: {}'.format(int(df['Birth Year'].max())))
                print('The most common Birth Year is: {}'.format(int(df['Birth Year'].mode())))
            except:
                print("No column for 'Birth Year'")
        except:
            print("No data for this combination of inputs.")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)


        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
