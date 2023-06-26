import openai
import logging

def setup_openai_api(api_key):
    """
    Setup the OpenAI API with the provided API key.
    """
    try:
        openai.api_key = api_key
        return True
    except Exception as e:
        logging.error(f"Error setting up OpenAI API: {e}")
        return False

def generate_response(prompt, engine='davinci', temperature=0.7, max_tokens=50):
    """
    Generate a response using OpenAI GPT-3.
    
    :param prompt: The prompt to send to GPT-3.
    :param engine: The GPT-3 engine to use (e.g., 'davinci').
    :param temperature: Controls the randomness of the output (0 to 1).
    :param max_tokens: The maximum number of tokens in the output.
    :return: The generated response as a string.
    """
    try:
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"Error generating response from OpenAI API: {e}")
        return None
