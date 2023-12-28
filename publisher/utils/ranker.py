import datetime
from typing import List, Dict

def filter_publications_by_date_and_score(
        data: List[Dict],
        threshold: int = 75,
        date: datetime = datetime.datetime.today()
) -> List[Dict]:
    """
    Filters a list of publications by date and score.

    Parameters:
    data (List[Dict]): The data to filter.
    threshold (int): The minimum score a publication must have to be included. Defaults to 75.
    date (datetime): The date the publications must match. Defaults to today's date.

    Returns:
    List[Dict]: The filtered data.
    """
    date_str = date.strftime('%Y-%m-%d')
    return [
        publication
        for publication in data
        if publication['date'] == date_str and publication['score'] >= threshold
    ]