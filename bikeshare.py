
import time
import pandas as pd
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze. Can also chose "all" in any of the parameters.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Which city would you like to know more? Chicago, New York City or Washington?')
    city = input().lower()
    cities = ['chicago', 'new york city', 'washington']
    while city not in cities:
        print('city name not valid!, please type Chicago, New York City or Washington')
        city = input().lower() 
    
    # TO DO: get user input for month (all, january, february, ... , june)
    print('Do you want to know data for a particular month, or for all? (all, january, february, ... , june)')
    month = input().lower()
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while month not in months:
              print('invalid input, please enter a valid input!')
              month = input().lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print('For what day of the week? or want for all week? (all, monday, tuesday, ... sunday)')
    day = input().lower()
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while day not in days:
              print('invalid input, please enter a valid input!')
              day = input().lower()

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
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    
    #extract hours
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the days list to get the corresponding int
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day) + 1
        
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
        
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month_mode = df['month'].mode()[0]
    month_name = calendar.month_name[month_mode]
    print(f'\nThe most common month was {month_name}.')

    # TO DO: display the most common day of week
    day_mode = df['day_of_week'].mode()[0]
    day_name = calendar.day_name[day_mode]
    print(f'\nThe most common day of the week was {day_name}.')
    
    # TO DO: display the most common start hour
    hour_mode = df['hour'].mode()[0]
    print(f'\nThe most common hour of the day was {hour_mode}h.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    sstation_mode = df['Start Station'].mode()[0]
    print(f'\nThe most commonly used start station was {sstation_mode}.')

    # TO DO: display most commonly used end station
    estation_mode = df['End Station'].mode()[0]
    print(f'\nThe most commonly used end station was {estation_mode}.')

    # TO DO: display most frequent combination of start station and end station trip
    combinations = df.groupby(['Start Station',
                                   'End Station']).size().sort_values(ascending=False)

    comb_start = combinations.index[0][0]
    comb_end = combinations.index[0][1]
    number_comb = combinations.iloc[0]
    print(f'\nThe most frequent combination of start station and end station trip was from {comb_start} to {comb_end} with a total of {number_comb} trips.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    travel_sum = df['Trip Duration'].sum()
    print(f'\nThe total travel time was {travel_sum}.')

    # TO DO: display mean travel time
    travel_mean = df['Trip Duration'].mean()
    print(f'\nThe mean travel time was {travel_mean}.')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    for i in range(user_types.size):
        print(f'\nThere were {user_types.iloc[i]} {user_types.index[i]}s.')

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        for i in range(genders.size):
            print(f'\nThere were {genders.iloc[i]} {genders.index[i]}s.')
    else:
        print('\nNo data on gender is available!')
        
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        oldest_user = int(df['Birth Year'].min())
        yongest_user = int(df['Birth Year'].max())
        year_mode = int(df['Birth Year'].mode()[0])
    
        print(f'\nThe oldest user was born in {oldest_user}, the yongest user was born in {yongest_user} while most users were born in {year_mode}.')
    else:
        print('\nNo information on year of birth is available!')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_df(df):
    """ Displays the first 5 lines of df, and askes if wants to see more."""
    num_rows = len(df)
    showmore = True
    
    while showmore:
        for start in range(0, num_rows, 5):
            end = min(start + 5, num_rows)
            print(df.iloc[start:end])
            print('\n')
            if end < num_rows:
                seemore = input("\nDo you want to see more? (yes/no)")
                if seemore.lower() != 'yes':
                    showmore = False
                    break
                
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        if df.size == 0:
            restart = input('\nNothing selected. Would you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        else:
            print(f'\nCollected {df.shape[0]} lines of data!')
            
        
        print('\nShowing the first 5 lines of the selected data:\n')
        display_df(df)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()