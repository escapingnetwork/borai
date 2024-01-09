import os
import time

from dotenv import load_dotenv
load_dotenv()

# Google
import pathlib
import textwrap

import google.generativeai as genai

# Used to securely store your API key
# from google.colab import userdata

delimiter = "####"
MAX_TOKENS = 4096
# openai.api_key  = os.getenv('OPENAI_API_KEY')
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


def get_completion(prompt, model="gemini-pro"): 
    gemini = genai.GenerativeModel(model)
    response = gemini.generate_content(prompt)
    if len(response.candidates) == 0 or len(response.parts) == 0:
        print(response)
        return ""
    return response.text

def summarize(chunks):
    if len(chunks) <= 1:
        prompt = f"""
            Resumir el siguiente texto de manera formal en 140 caracteres maximo \
            no decorar con caracteres especiales, ni hashtags, solo texto simple.

            Texto:{delimiter}{chunks[0]}{delimiter}
        """
        response = get_completion(prompt)

    else:
        print(f"{len(chunks)} chunks. Please wait!")
        initial_response = ''
        for i, chunk in enumerate(chunks):
            prompt = f"""
                Resumir el fragmento de un artículo publicado en el Boletín \
                Oficial de Argentina. \
                Tener en cuenta que es el trozo {i+1} de {len(chunks)+1} trozos. \
                Luego, todos estos trozos serán unificados en el mismo mensaje. \
                El resultado final tener 140 caracteres maximo, \
                no decorar con caracteres especiales, ni hashtags, solo texto simple.
                
                Review: {delimiter}{chunk}{delimiter}
            """
            initial_response += get_completion(prompt)
            time.sleep(20)
            print(f"{i+1} done.")

        prompt = f"""
            Resumir el siguiente texto de manera formal en 140 caracteres maximo, \
            no decorar con caracteres especiales, ni hashtags, solo texto simple.

            Texto:{delimiter}{initial_response}{delimiter}
        """
        response = get_completion(prompt)

    tags = []
    
    return tags, 0, response