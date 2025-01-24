import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    print('\nHello! Let\'s explore some US bikeshare data!')
    print('-'*40)

    # Get user input for city
    while True:
        city = input("Please choose a city (Chicago, New York city, Washington): ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city. Please choose from Chicago, New York city, or Washington.")

    # Get user input for month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Please choose a month (january, february, ... , june) or 'all': ").lower()
        if month in months:
            break
        else:
            print("Invalid month. Please choose from january to june, or 'all'.")

    # Get user input for day of the week
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Please choose a day (monday, tuesday, ... sunday) or 'all': ").lower()
        if day in days:
            break
        else:
            print("Invalid day. Please choose a valid day of the week or 'all'.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):

    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['start_hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\n#1 Popular times of travel (i.e., occurs most often in the start time)\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['month'].mode()[0]
    print(f"Most Common Month: {most_common_month}")

    # Display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(f"Most Common Day of Week: {most_common_day.title()}")

    # Display the most common start hour
    most_common_hour = df['start_hour'].mode()[0]
    print(f"Most Common Start Hour: {most_common_hour}")

    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\n#2 Popular stations and trip\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"Most Common Start Station: {most_common_start_station}")

    # Display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"Most Common End Station: {most_common_end_station}")

    # Display most frequent combination of start station and end station trip
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"Most Common Trip: {most_common_trip}")

    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\n#3 Trip duration\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total Travel Time: {total_travel_time} seconds")

    # Display avg travel time
    avg_travel_time = df['Trip Duration'].mean()
    print(f"Average Travel Time: {avg_travel_time:.2f} seconds")

    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\n#4 User info\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of User Types:")
    for user_type, count in user_types.items():
        print(f"{user_type}: {count}")

    # Display counts of gender (if available)
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of Gender:")
        for gender, count in gender_counts.items():
            print(f"{gender}: {count}")

    # Display earliest, most recent, and most common year of birth (if available)
    if 'Birth Year' in df:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print("\nBirth Year Stats:")
        print(f"Earliest Year: {earliest_year}")
        print(f"Most Recent Year: {most_recent_year}")
        print(f"Most Common Year: {most_common_year}")

    print('-'*40)

def display_raw_data(df):
    """Displays raw data upon request by the user in increments of 5 rows."""
    start_loc = 0
    while True:
        view_data = input("\nWould you like to view 5 rows of raw data? Enter yes or no: ").lower()
        print('-'*40)
        if view_data != 'yes':
            break
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        print('-'*40)
        if start_loc >= len(df):
            print("No more data to display.")
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df)


        restart = input('\nWould you like to restart? Enter yes or no: ')
        if restart.lower() != 'yes':
            break
        print('-'*40)

if __name__ == "__main__":
    main()
