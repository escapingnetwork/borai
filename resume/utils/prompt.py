from dotenv import load_dotenv

load_dotenv()

from xai_sdk import Client
from xai_sdk.chat import user

delimiter = "####"


def get_completion(prompt, model="grok-4-1-fast"):
    client = Client()
    chat = client.chat.create(model=model, messages=[user(prompt)])
    response = chat.sample()
    return response.content


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
        initial_response = ""
        for i, chunk in enumerate(chunks):
            prompt = f"""
                Resumir el fragmento de un artículo publicado en el Boletín \
                Oficial de Argentina. \
                Tener en cuenta que es el trozo {i + 1} de {len(chunks)} trozos. \
                Luego, todos estos trozos serán unificados en el mismo mensaje. \
                El resultado final tener 140 caracteres maximo, \
                no decorar con caracteres especiales, ni hashtags, solo texto simple.

                Review: {delimiter}{chunk}{delimiter}
            """
            initial_response += get_completion(prompt)
            print(f"{i + 1} done.")

        prompt = f"""
            Resumir el siguiente texto de manera formal en 140 caracteres maximo, \
            no decorar con caracteres especiales, ni hashtags, solo texto simple.

            Texto:{delimiter}{initial_response}{delimiter}
        """
        response = get_completion(prompt)

    tags = []

    return tags, 0, response
        # Placeholder for tags extraction (can be implemented later)
