import pandas as pd
from typing import List, Dict

day_dict = {
    'Su': 'Sunday',
    'M': 'Monday',
    'T': 'Tuesday',
    'W': 'Wednesday',
    'Th': 'Thursday',
    'F': 'Friday',
    'Sa': 'Saturday'
}

def process_time_range(time_range: str) -> str:
    start, end = time_range.split('-')

    if len(start) <= 4: 
        start = start[:-2].zfill(2) + ':00' + start[-2:]
    else:
        start = start[:-5].zfill(2) + ':' + start[-5:-2] + start[-2:]
    
    if len(end) <= 4:
        end = end[:-2].zfill(2) + ':00' + end[-2:]
    else:
        end = end[:-5].zfill(2) + ':' + end[-5:-2] + end[-2:]

    return start.upper() + '-' + end.upper()

def process_times(times: str) -> str:
    times = times.replace('_x000D_', '') # remove line breaks added by Excel in case there are any
    time_ranges = times.split(',')
    processed_times = ', '.join(process_time_range(time_range.strip()) for time_range in time_ranges)
    return processed_times.replace('::', ':')

def process_hours(hours: str) -> Dict[str, str]:
    if not isinstance(hours, str):
        return {day: '' for day in day_dict.values()}
    
    hours_list = hours.split('\n')
    hours_dict = {day: '' for day in day_dict.values()}
    for hour in hours_list:
        try:
            day_str, *time_str = hour.split(':')
            time_str = ':'.join(time_str)
            days = []
            if '-' in day_str:
                start_day, end_day = day_str.split('-')
                days = list(day_dict.keys())[list(day_dict.keys()).index(start_day): list(day_dict.keys()).index(end_day)+1]
            else:
                days = day_str.split(',')
            days = [day_dict[day] for day in days]

            if 'CLOSED' in time_str:
                time_str = time_str.split(',')[0]

            for day in days:
                hours_dict[day] = process_times(time_str.strip())
        except Exception as e:
            print(f"Error occurred for {hour} with error {str(e)}")
            continue
    return hours_dict

df = pd.read_excel('Locations.xlsx', sheet_name='hours')

for idx, row in df.iterrows():
    store_hours = row['Store Hours']
    day_hours = process_hours(store_hours)
    for day, hours in day_hours.items():
        df.at[idx, day] = hours

df.to_excel('UpdatedLocations.xlsx', sheet_name='hours', index=False)
