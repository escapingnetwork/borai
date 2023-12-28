from typing import List
import datetime
from tiktoken import Tokenizer

CHUNK_SIZE = 4000
OVERLAP = 200
INPUT_FORMAT = '%d/%m/%Y'
OUTPUT_FORMAT = '%Y-%m-%d'

def chop(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> List[str]:
    """
    Takes a text as input and returns a list
    of chunks of max size chunk_size. GPT tokens
    are used to determine the chunk size.
    """
    tokenizer = Tokenizer()

    tokens = tokenizer.tokenize(text)
    num_tokens = len(tokens)
    
    chunks = []
    for i in range(0, num_tokens, chunk_size - overlap):
        chunk = tokens[i:i + chunk_size]
        chunks.append(''.join(chunk))
    
    return chunks

def transform_date(date: str, input_format: str = INPUT_FORMAT, output_format: str = OUTPUT_FORMAT) -> str:
    """
    Transform str date from input format to
    output format.
    """
    try:
        date = datetime.datetime.strptime(date, input_format)
        date = date.strftime(output_format)
    except ValueError as e:
        print(f"Error occurred: {e}")
        return None

    return date