import pandas as pd
from typing import List, Dict

# Abbreviation to full day names mapping
day_dict = {
    'Su': 'Sunday',
    'M': 'Monday',
    'T': 'Tuesday',
    'W': 'Wednesday',
    'Th': 'Thursday',
    'F': 'Friday',
    'Sa': 'Saturday'
}

# Process individual time range string
def process_time_range(time_range: str) -> str:
    start, end = time_range.split('-')

    if len(start) <= 4: # covers 'HAM', 'HPM', 'HHPM', 'HHAM'
        start = start[:-2].zfill(2) + ':00' + start[-2:]
    else:
        start = start[:-5].zfill(2) + ':' + start[-5:-2] + start[-2:]
    
    if len(end) <= 4:
        end = end[:-2].zfill(2) + ':00' + end[-2:]
    else:
        end = end[:-5].zfill(2) + ':' + end[-5:-2] + end[-2:]

    return start.upper() + '-' + end.upper()

# Process time string
def process_times(times: str) -> str:
    times = times.replace('_x000D_', '') # remove line breaks added by Excel
    time_ranges = times.split(',')
    return ', '.join(process_time_range(time_range.strip()) for time_range in time_ranges)

# Process full 'day:time' strings
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
            # Consecutive days
            if '-' in day_str:
                start_day, end_day = day_str.split('-')
                days = list(day_dict.keys())[list(day_dict.keys()).index(start_day): list(day_dict.keys()).index(end_day)+1]
            # Individual days
            else:
                days = day_str.split(',')
            days = [day_dict[day] for day in days]
            for day in days:
                hours_dict[day] = process_times(time_str.strip())
        except Exception as e:
            print(f"Error occurred for {hour} with error {str(e)}")
            continue
    return hours_dict

# Read the file
df = pd.read_excel('Locations.xlsx', sheet_name='hours')

# Process 'Store Hours' column
for idx, row in df.iterrows():
    store_hours = row['Store Hours']
    day_hours = process_hours(store_hours)
    for day, hours in day_hours.items():
        df.at[idx, day] = hours

# Save the DataFrame to an Excel file
df.to_excel('UpdatedLocations.xlsx', sheet_name='hours', index=False)
