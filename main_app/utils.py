"""
Utility Function
"""

def validate_session(start_year, end_year):
    start_year = int(start_year)
    end_year = int(end_year)

    # session start year cannot be grater than session end year
    if start_year > end_year:
        return False

    # longest single degree course is 6 years
    if end_year - start_year > 6:
        return False
    return True
