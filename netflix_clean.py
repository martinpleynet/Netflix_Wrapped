'''
This script cleans my Netflix viewing activity data and
prepares it to be used from my dashboard
'''

import pandas as pd

def main():

    # Load viewing history and reference data
    history = pd.read_csv("NetflixViewingHistory.csv")
    reference1 = pd.read_csv("NetflixShowData.csv")
    
    # Convert dates to datetime
    history['Date'] = pd.to_datetime(history['Date'])
    # Look at only 2020 viewing data
    history_2020 = history[history['Date'].dt.year == 2020]
    # Remove any rows with NaN values
    history_2020.dropna()

    # Create new columns for month and day of week
    history_2020['Month'] = history_2020['Date'].dt.month
    history_2020['DayOfWeek'] = history_2020['Date'].dt.day_name()

    # Clean up titles to only include show/movie name (i.e. no episode titles)
    history_2020['Title'] = history_2020['Title'].str.split(':', n = 1, expand=True)[0]
    
    # Join the reference and viewing data using a left join
    netflix_merged = pd.merge(left=history_2020, right=reference1, how='left', left_on='Title', right_on='Title')

    # Save new dataset
    netflix_merged.to_csv("NetflixWrapped.csv")
    

if __name__ == '__main__':
    main()
