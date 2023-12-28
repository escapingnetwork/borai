import os
import time
import logging

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

delimiter = "####"
MAX_TOKENS = 4096
SLEEP_DELAY = 20

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_completion(prompt, model="gemini-pro"): 
    gemini = genai.GenerativeModel(model)
    response = gemini.generate_content(prompt)
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
        logging.info(f"{len(chunks)} chunks. Please wait!")
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
            time.sleep(SLEEP_DELAY)
            logging.info(f"{i+1} done.")

        response = initial_response

    return response