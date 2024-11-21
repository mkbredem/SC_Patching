import yaml
from datetime import datetime, timedelta

# Input list of strings
input_list = ['LXP-RHE-QTR-02SAT-0800-TS', 'LXP-RHE-QTR-01FRI-1000-TS']

# Mapping of quarters to starting months
quarter_start_months = {
    "01": 1,
    "02": 4,
    "03": 7,
    "04": 10,
}

# Mapping of days of the week to integers (Monday=0, Sunday=6)
day_mapping = {
    "MON": 0,
    "TUE": 1,
    "WED": 2,
    "THU": 3,
    "FRI": 4,
    "SAT": 5,
    "SUN": 6,
}

# Function to calculate the second occurrence of a weekday in a month
def get_second_weekday(year, month, weekday):
    first_day = datetime(year, month, 1)
    first_weekday = (weekday - first_day.weekday()) % 7
    if first_weekday == 0:
        first_weekday += 7
    second_weekday = first_day + timedelta(days=first_weekday + 7)
    return second_weekday.day

# Function to process each string in the input list
def process_string(entry):
    name = entry
    quarter = entry[14]  # Quarter is at index 14
    day_of_week = entry[15:18]  # Day of week is at indices 15-17
    hour = int(entry[19:21])  # Hour is at indices 19-20
    
    month = quarter_start_months[quarter + "1"]  # Get starting month of the quarter
    weekday = day_mapping[day_of_week]  # Map day of week to integer
    
    # Determine the year based on whether the date has passed this year
    today = datetime.today()
    year = today.year
    
    second_weekday_day = get_second_weekday(year, month, weekday)
    target_date = datetime(year, month, second_weekday_day)
    
    if target_date < today:
        year += 1
        second_weekday_day = get_second_weekday(year, month, weekday)
    
    return {
        "name": name,
        "year": year,
        "month": month,
        "day": second_weekday_day,
        "hour": hour,
    }

# Process the input list
output_list = [process_string(entry) for entry in input_list]

# Convert the output to YAML for visualization
print(yaml.dump({"host-collections": output_list}, default_flow_style=False))
