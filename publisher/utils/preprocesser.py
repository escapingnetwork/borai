from typing import List, Dict

def sort_by(data: List[Dict], by: str = 'score', reverse: bool = True) -> List[Dict]:
    """
    Sorts a list of dictionaries by a specified key.

    Parameters:
    data (List[Dict]): The data to sort.
    by (str): The key to sort the data by. Defaults to 'score'.
    reverse (bool): Whether to sort the data in reverse order. Defaults to True.

    Returns:
    List[Dict]: The sorted data.
    """
    data.sort(key=lambda item: item[by], reverse=reverse)
    return data