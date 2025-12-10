import os
import datetime

from xai_sdk import Client


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
    api_key = os.getenv("XAI_API_KEY")
    client = Client(api_key=api_key)
    tokens = client.tokenize.tokenize_text(text, model="grok-4-1-fast")
    num_tokens = len(tokens)

    chunks = []
    for i in range(0, num_tokens, chunk_size - overlap):
        chunk = tokens[i : i + chunk_size]
        chunk_text = "".join([t.string_token for t in chunk])
        chunks.append(chunk_text)

    return chunks


def transform_date(
    date: str,
    input_format: str = "%d/-%m/%Y",
    output_format: str = "%Y-%m-%d",
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
    parsed_date = datetime.datetime.strptime(date, "%d/%m/%Y")
    # Transform to desired format
    parsed_date = parsed_date.strftime("%Y-%m-%d")

    return parsed_date
