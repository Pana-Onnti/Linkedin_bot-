import io
import os
import numpy as np
import requests
import json
from api import api
from google.cloud import vision
import cv2
json_txt = r'linkedin-bot-380614-36ad6b61a17e.json'

api_key = api


class OpenAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def get_response(self, message):
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": message}],
            "temperature": 1.0,
            "top_p": 1.0,
            "n": 1,
            "stream": False,
            "presence_penalty": 0,
            "frequency_penalty": 0,
        }

        response = requests.post(self.url, headers=self.headers, json=payload, stream=False)
        json_string = response.content.decode('utf-8')
        json_data = json.loads(json_string)
        return json_data['choices'][0]['message']['content']
class TextDetector:
    def __init__(self, credentials_path):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        self.client = vision.ImageAnnotatorClient()

    def detect_text(self, image_path):
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = self.client.text_detection(image=image)
        texts = response.text_annotations
        return texts


class MessageProcessor:
    def __init__(self, texts):
        self.texts = texts

    def process_message(self):
        data = {}
        for i, text in enumerate(self.texts):
            if i == 0:
                data['primer pregunta'] = text.description
            else:
                pass
        cadena = str(data)
        texto = ["¿Hay algún problema con esta pregunta?", "Enviar comentarios", "Tiempo finalizado", "Comprobar respuesta", "/", '/n']
        for text in texto:
            cadena = cadena.replace(text, " ")
            cadena = cadena.replace("\\n",  " [Salto de linea, otra opcion es:] " ) 
        cadena = cadena.strip() 

        return cadena
