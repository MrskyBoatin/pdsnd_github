import time
import pandas as pd
import numpy as np
import datetime as dt
import click

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months, days, cities = ('january', 'february', 'march', 'april', 'may', 'june'), ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday'),tuple(CITY_DATA.keys())
confirmation_responds = ('n','y')


def responds(prompt, expected_answer):
    """Given a specific responds , Return as well formated array of expected answers by user.
    Args:
        (str) prompt - input from user
        (tuple) expected_answer - a tuple of expected answers from userr
    Returns:
        None 
    """
    while True:
        opt = input(prompt).lower().strip()

        # triggers if the input has more than one name
        if ',' in opt:
            opt = [i.strip().lower() for i in opt.split(',')]
            if list(filter(lambda x: x in expected_answer, opt)) == opt:
                break
            # triggers if the input has only one name
        if ',' not in opt:
            if opt in expected_answer:
                break
        if opt == 'end':
            raise SystemExit

        prompt = ("\nWrong input, Enter a valid option or type end if you would like to end program :\n>")

    return opt



def column_filter():
    """Ask user to specify city(ies) and filters, month(s) and weekday(s).
    Returns:
        (str) city -name of the city(ies) to analyze
        (str) month -name of the month(s) to filter
        (str) day -name of the day(s) of week to filter
    """

    print("\n\nLet's explore some US bikeshare data!\n")

    print("Type end at any time if you would like to exit the program.\n")

    while True:
        city = responds("\nFor what city/cities do you want do select data, "
                      "New York City, Chicago or Washington? Use commas "
                      "to list the names.\nType end at any time if you would like to exit the program\n>", cities)
        month = responds("\nFrom January to June, for what month/months do you "
                       "want do filter data? Use commas to list the names.\nType end at any time if you would like to exit the program\n>",
                       months)
        day = responds("\nFor what day/days do you want do filter bikeshare "
                     "data? Use commas to list the names. \nType end at any time if you would like to exit the program\n>", days)

        # confirm the user input
        selection = responds("\nPlease confirm that you would like to apply "
                              "the following filters to the bikeshare data."
                              "\n\n City(ies): {}\n Month(s): {}\n Weekday(s)"
                              ": {}\n\n [y] Yes\n [n] No\nType end at any time if you would like to exit the program\n\n>"
                              .format(city, month, day), confirmation_responds)
        if selection == 'y':
            break
        else:
            print("\nTry this again!")
    print('-'*50)
    print('\n')
    print('-'*50)
    return city, month, day


def data_source(city, month, day):
    """
        Loads data for the specified city and filters by month and day if applicable.
        Args:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
        Returns:
            df - Pandas DataFrame containing city data filtered by month and day
    """

    print("\nThe program is loading the data for the filters according to your responds.")
    start_time = time.time()

    # filter the data according to the selected city filters
    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city),
                       sort=True)
        # reorganize DataFrame columns after a city concat
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time',
                                     'Trip Duration', 'Start Station',
                                     'End Station', 'User Type', 'Gender',
                                     'Birth Year'])
        except:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])

    # create columns to display statistics
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour

    # filter the data according to month and weekday into two new DataFrames
    if isinstance(month, list):
        df = pd.concat(map(lambda month: df[df['Month'] ==
                           (months.index(month)+1)], month))
    else:
        df = df[df['Month'] == (months.index(month)+1)]

    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Weekday'] ==
                           (day.title())], day))
    else:
        df = df[df['Weekday'] == day.title()]

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*50)
    print('\n')
    print('-'*50)

    return df


def timings(df):
    """Display statistics on the most frequent times of travel.
        Args:
            df - Pandas DataFrame 
        Returns:
            None
        Print's statement
    """

    print('\nDisplaying the statistics on the most frequent times of '
          'travel according to your responds...\n')
    start_time = time.time()

    # display the popular month
    popular_month = df['Month'].mode()[0]
    print('For the selected filter, the month with the most travels is: ' +
          str(months[popular_month-1]).title() + '.')

    # display the popular day of week
    popular_day = df['Weekday'].mode()[0]
    print('For the selected filter, the popular day of the week is: ' +
          str(popular_day) + '.')

    # display the popular start hour
    popular_hour = df['Start Hour'].mode()[0]
    print('For the selected filter, the popular start hour is: ' +
          str(popular_hour) + '.')

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*50)
    print('\n')
    print('-'*50)


def station_stats(df):
    """Display statistics on the most popular stations and trip.
        Args:
            df - Pandas DataFrame 
        Returns:
            None
        Print statement
    """

    print('\nCalculating The Most Popular Stations and Trip according to your responds...\n')
    start_time = time.time()

    # display popular used start station
    popular_start_station = str(df['Start Station'].mode()[0])
    print("For the selected filters, the popular start station is: " +
          popular_start_station)

    # display popularly used end station
    popular_end_station = str(df['End Station'].mode()[0])
    print("For the selected filters, the popular start end is: " +
          popular_end_station)

    # display most frequent combination of start station and
    # end station trip
    df['Start-End Combination'] = (df['Start Station'] + ' - ' +
                                   df['End Station'])
    popular_start_end_combination = str(df['Start-End Combination']
                                            .mode()[0])
    print("For the selected filters, the popular start-end combination "
          "of stations is: " + popular_start_end_combination)

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*50)
    print('\n')
    print('-'*50)


def trip_duration_stats(df):
    """Display statistics on the total and average trip duration.
        Args:
            df - Pandas DataFrame 
        Returns:
            None
        Print statement
    """

    print('\nCalculating Trip Duration according to your responds...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = (str(int(total_travel_time//86400)) +
                         'd ' +
                         str(int((total_travel_time % 86400)//3600)) +
                         'h ' +
                         str(int(((total_travel_time % 86400) % 3600)//60)) +
                         'm ' +
                         str(int(((total_travel_time % 86400) % 3600) % 60)) +
                         's')
    print('For the selected filters, the total travel time is : ' +
          total_travel_time + '.')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = (str(int(mean_travel_time//60)) + 'm ' +
                        str(int(mean_travel_time % 60)) + 's')
    print("For the selected filters, the mean travel time is : " +
          mean_travel_time + ".")

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*50)
    print('\n')
    print('-'*50)


def user_stats(df, city):
    """Display statistics on bikeshare users.
        Args:
            df - Pandas DataFrame 
        Returns:
            None
        Print statement
    """

    print('\nCalculating User Stats according to your responds...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    print("Distribution for user types:")
    print(user_types)

    # Display counts of gender
    try:
        gender_distribution = df['Gender'].value_counts().to_string()
        print("\nDistribution for each gender:")
        print(gender_distribution)
    except KeyError:
        print("We're sorry! There is no data of user genders for {}."
              .format(city.title()))

    # Display earliest, most recent, and popular year of birth
    try:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print("\nFor the selected filter, the oldest person to ride one "
              "bike was born in: " + earliest_birth_year)
        most_recent_birth_year = str(int(df['Birth Year'].max()))
        print("For the selected filter, the youngest person to ride one "
              "bike was born in: " + most_recent_birth_year)
        popular_birth_year = str(int(df['Birth Year'].mode()[0]))
        print("For the selected filter, the popular birth year amongst "
              "riders is: " + popular_birth_year)
    except:
        print("We're sorry! There is no data of birth year for {}."
              .format(city.title()))

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*50)
    print('\n')
    print('-'*50)


def raw_data(df, mark_place):
    """Display 5 line of sorted raw data each time.
            Args:
            df - Pandas DataFrame 
            mark_place 
        Returns:
            None
        Print statement
    """


    print("\nViewing raw data.")

    # this variable holds where the user last stopped
    if mark_place > 0:
        last_place = responds("\nWould you like to continue from where you "
                            "stopped last time? \n [y] Yes\n [n] No\n Type end at any time if you would like to exit the program\n\n>", confirmation_responds)
        if last_place == 'n':
            mark_place = 0

    # sort data by column
    if mark_place == 0:
        sort_df = responds("\nHow would you like to sort the way the data is "
                         "displayed in the dataframe? Hit Enter to view "
                         "unsorted.\n \n [1] Start Time\n [2] End Time\n "
                         "[3] Trip Duration\n [4] Start Station\n "
                         "[5] End Station\n Type end at any time if you would like to exit the program\n\n>",
                         ('1', '2', '3', '4', '5', 'end',''))

        order = responds("\nWould you like it to be sorted ascending or "
                             "descending? \n [1] Ascending\n [2] Descending\n Type end at any time if you would like to exit the program.\n"
                             "\n\n>",
                             ('1', '2'))

        if order == '1':
            order = True
        elif order == '2':
            order = False
        elif order == 'end':
            raise SystemExit

        if sort_df == '1':
            df = df.sort_values(['Start Time'], ascending=order)
        elif sort_df == '2':
            df = df.sort_values(['End Time'], ascending=order)
        elif sort_df == '3':
            df = df.sort_values(['Trip Duration'], ascending=order)
        elif sort_df == '4':
            df = df.sort_values(['Start Station'], ascending=order)
        elif sort_df == '5':
            df = df.sort_values(['End Station'], ascending=order)
        elif sort_df == 'end':
            raise SystemExit
        elif sort_df == '':
            pass

    # each loop displays 5 lines of raw data
    while True:
        for i in range(mark_place, len(df.index)):
            print("\n")
            print(df.iloc[mark_place:mark_place+5].to_string())
            print("\n")
            mark_place += 5

            if responds("Do you want to keep printing raw data?"
                      "\n\n[y]Yes\n[n]No\n\n>", confirmation_responds) == 'y':
                continue
            else:
                break
        break

    return mark_place


def main():
    while True:
        click.clear()
        city, month, day = column_filter()
        df = data_source(city, month, day)

        mark_place = 0
        while True:
            select_data = responds("\nPlease select the information you would "
                                 "like to obtain.\n\n [1] Time Stats\n [2] "
                                 "Station Stats\n [3] Trip Duration Stats\n "
                                 "[4] User Stats\n [5] Display Raw Data\n "
                                 "[6] Restart\n Type end at any time if you would like to exit the program\n\n>",
                                 ('1', '2', '3', '4', '5', '6','end'))
            click.clear()
            if select_data == '1':
                timings(df)
            elif select_data == '2':
                station_stats(df)
            elif select_data == '3':
                trip_duration_stats(df)
            elif select_data == '4':
                user_stats(df, city)
            elif select_data == '5':
                mark_place = raw_data(df, mark_place)
            elif select_data == '6':
                break
            elif select_data == 'end':
                raise SystemExit

        restart = responds("\nWould you like to restart?\n\n[y]Yes\n[n]No\nType end at any time if you would like to exit the program\n\n>", confirmation_responds)
        if restart.lower() != 'y':
            break
        elif restart == 'end':
            raise SystemExit


if __name__ == "__main__":
    main()