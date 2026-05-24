from utils.gemini_api import ask_gemini
from utils.llama_api import ask_llama

def ask_ai(prompt):

    try:

        response = ask_gemini(prompt)

        if "429" in response:
            raise Exception("Gemini quota exceeded")

        return response

    except:

        return ask_llama(prompt)