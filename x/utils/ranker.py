import datetime

def ranker(
        data: list,
        threshold: int = 75,
        date: datetime = datetime.datetime.today()
) -> list:
    """
    Reads list of json publications and returns
    data filtered by threshold and actual date.
    Input:
    data: list with json publications
    threshold: minimum value for score
    Returns:
    filtered data
    """
    data = [
        publication
        for publication in data
        if publication['date'] == str(date.strftime('%Y-%m-%d'))
    ]

    data = [
        publication
        for publication in data
        if publication['score'] >= threshold
    ]

    return data