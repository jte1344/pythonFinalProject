import datetime
import re


def date_range_creator(date):

    # Initialize return value
    dateRange = []

    # create date regex
    dateRegex = re.compile(r'([01][0-9])/([0-3][0-9])/([0-9]{4})')
    mo = dateRegex.search(date)

    # Strip each section of the date for use in datetime
    month = int(mo[1])
    day = int(mo[2])
    year = int(mo[3])

    # Create initial date datetime
    initialDate = datetime.date(month=month, day=day, year=year)

    # Incriment the initial date to two new dates
    firstNewDate = initialDate + datetime.timedelta(days=1)
    secondNewDate = initialDate + datetime.timedelta(days=2)

    # Adjust formatting of the new dates
    firstNewDate = firstNewDate.strftime("%m/%d/%Y")
    secondNewDate = secondNewDate.strftime("%m/%d/%Y")

    # Add all dates to the range list
    dateRange.append(date)
    dateRange.append(firstNewDate)
    dateRange.append(secondNewDate)

    return dateRange

# Test the function
date = '12/31/2019'

print(date_range_creator(date))
