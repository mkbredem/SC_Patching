#!/usr/bin/env python3

from datetime import datetime, timedelta

def second_occurrence(year, month, day_of_week, hour):
    """
    Determine the second occurrence of a specific day of the week in a given year and month.
    """
    # Dictionary to map day names to weekday numbers
    days_map = {'MON': 0, 'TUE': 1, 'WED': 2, 'THU': 3, 'FRI': 4, 'SAT': 5, 'SUN': 6}

    if day_of_week not in days_map:
        raise ValueError("Invalid day_of_week. Use 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', or 'SUN'.")

    # Start from the 1st of the given month and year
    first_day = datetime(year, month, 1)
    target_weekday = days_map[day_of_week]

    # Calculate the offset to the first occurrence of the target weekday
    days_to_first = (target_weekday - first_day.weekday() + 7) % 7
    first_occurrence = first_day + timedelta(days=days_to_first)

    # Add 7 days to the first occurrence to get the second occurrence
    second_occurrence_date = first_occurrence + timedelta(days=7)

    # Ensure the second occurrence is still within the same month
    if second_occurrence_date.month != month:
        raise ValueError(f"The second {day_of_week} does not exist in {month}/{year}.")

    second_occurrence_date = second_occurrence_date.replace(hour=hour, minute=0, second=0)

    # If the second occurrence date is in the past, recalculate for the next year
    if second_occurrence_date.date() <= datetime.today().date():
        return second_occurrence(year + 1, month, day_of_week, hour)

    return second_occurrence_date.strftime('%Y-%m-%d %H:%M:%S')

def extract_details(input_string):
    """
    Extract details from a host collection string.
    """
    input_string = input_string.replace("foreman_hostcollection_", "")
    
    # Extract the quarter (indices 13-14)
    quarter = input_string[12:14]

    # Map quarters to their starting months
    quarter_start_months = {
        "01": 1,  # Q1 starts in January
        "02": 4,  # Q2 starts in April
        "03": 7,  # Q3 starts in July
        "04": 10  # Q4 starts in October
    }

    if quarter not in quarter_start_months:
        raise ValueError(f"Invalid quarter value: {quarter}")
    start_month = quarter_start_months[quarter]

    # Extract the day of the week (indices 15-17)
    day_of_week = input_string[14:17].upper()

    # Validate the day of the week
    valid_days = {"MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"}
    if day_of_week not in valid_days:
        raise ValueError(f"Invalid day_of_week value: {day_of_week}")

    # Get the current year
    current_year = datetime.now().year

    # Extract the hour (indices 18-20)
    hour_of_day = int(input_string[18:20])

    return {
        "quarter": quarter,
        "month": start_month,
        "day_of_week": day_of_week,
        "year": current_year,
        "hour": hour_of_day,
    }

def extract_patch_date_from_host_collection(host_collection):
    """
    Ansible filter function to extract the patch date from a host collection string.
    """
    details = extract_details(host_collection)
    return second_occurrence(
        details["year"],
        details["month"],
        details["day_of_week"],
        details["hour"],
    )

class FilterModule:
    def filters(self):
        return {
            "extract_patch_date_from_host_collection": extract_patch_date_from_host_collection,
        }