import pandas as pd
from typing import List, Dict

# basically creates a mapping between the abbreviated days and the full day names for the columns in the excel sheet
day_dict = {
    'Su': 'Sunday',
    'M': 'Monday',
    'T': 'Tuesday',
    'W': 'Wednesday',
    'Th': 'Thursday',
    'F': 'Friday',
    'Sa': 'Saturday'
}

# once they're seperated, this processes individual timings. 
def process_time_range(time_range: str) -> str:
    start, end = time_range.split('-')
    if len(start) <= 4: # covers 'HAM', 'HPM', 'HHPM', 'HHAM'
        start = start[:-2] + ':00' + start[-2:]
    if len(end) <= 4:
        end = end[:-2] + ':00' + end[-2:]
    return start.upper() + '-' + end.upper()

# process time string
def process_times(times: str) -> str:
    time_ranges = times.split(',')
    return ', '.join(process_time_range(time_range.strip()) for time_range in time_ranges)

# processes full 'day:time' string
def process_hours(hours: str) -> Dict[str, str]:
    if not isinstance(hours, str):
        return {day: '' for day in day_dict.values()}
    
    hours_list = hours.split('\n')
    hours_dict = {day: '' for day in day_dict.values()}
    for hour in hours_list:
        try:
            # Split the string only on the first ':'
            day_str, time_str = hour.split(':', 1)
            days = []
            # handles the case for consecutive days
            if '-' in day_str:
                start_day, end_day = day_str.split('-')
                days = list(day_dict.keys())[list(day_dict.keys()).index(start_day): list(day_dict.keys()).index(end_day)+1]
            # handles the case for individual days
            else:
                days = day_str.split(',')
            days = [day_dict[day] for day in days]
            for day in days:
                hours_dict[day] = process_times(time_str.strip())
        except Exception as e:
            #throws error if error with formatting
            print(f"Error occurred for {hour} with error {str(e)}")
            continue
    return hours_dict

# uses pandas to read the excel file
df = pd.read_excel('Locations.xlsx', sheet_name='hours')

# processes 'Store Hours' column
for idx, row in df.iterrows():
    store_hours = row['Store Hours']
    day_hours = process_hours(store_hours)
    for day, hours in day_hours.items():
        df.at[idx, day] = hours

# Save the DataFrame to an Excel file
df.to_excel('Updated_Locations.xlsx', sheet_name='hours', index=False)
