import tiktoken
import datetime

def chop(
    text: str, 
    chunk_size=4000, 
    overlap=200,
) -> list:
    """
    Takes a text as input and returns a list
    of chunks of max size chunk_size. GPT tokens
    are used to determine the chunk size.
    Inputs:
    * text: Input text
    * chunk_size: Max tokens per chunk
    overlap: Overlapping tokens with previos/next chunk.
    Returns:
    List of text chunks.
    """
    encoding = tiktoken.get_encoding("gpt2")

    tokens = encoding.encode(text)
    num_tokens = len(tokens)
    
    chunks = []
    for i in range(0, num_tokens, chunk_size - overlap):
        chunk = tokens[i:i + chunk_size]
        chunks.append(chunk)
    chunks = [encoding.decode(chunk) for chunk in chunks]
    
    return chunks

def transform_date(
        date: str,
        input_format: str = '%d/-%m/%Y',
        output_format: str = '%Y-%m-%d',
) -> str:
    """
    Transform str date from input format to
    output format.
    Parameters:
    * date: desired str date to transofrm
    * input_format: original date format 
    * output_format: desired date format
    Returns:
    New str date with desired format.
    """
    # Read date as actual format
    date = datetime.datetime.strptime(date, '%d/%m/%Y')
    # Transform to desired format
    date = date.strftime('%Y-%m-%d')

    return date
