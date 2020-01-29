def valid_year(year_in_question, start_year, end_year):
    """
    Given year is included in start and end years of timeline
    """
    return year_in_question >= start_year and year_in_question <= end_year
