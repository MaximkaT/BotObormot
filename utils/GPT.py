import openai
import requests
from PIL import Image

def chatGptReuqest(messages):
    history = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages)
    reply = history.choices[0].message.content
    return reply

def dalleRequest(prompt, images_num, preferred_size):
    generation_response = openai.Image.create(
        prompt=prompt,
        n=images_num,
        size=preferred_size,
        response_format="url",
    )
    return generation_response
