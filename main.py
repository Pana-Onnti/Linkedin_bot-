import io
import os
import cv2
import numpy as np
import pyautogui
import requests
import json
from google.cloud import vision
from colorama import init, Fore, Style
from api import api


json_txt = r'linkedin-bot-380614-45f25e177a62.json'

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

class ImageProcessor:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)

    def crop_image(self, x1, y1, x2, y2):
        return self.image[y1:y2, x1:x2]

class MessageProcessor:
    def __init__(self, texts):
        self.texts = texts

    def process_message(self):
        data = {}
        for i, text in enumerate(self.texts):
            if i == 0:
                data['primer pregunta'] = text.description
            else:
                # Aquí puedes agregar más condiciones para agregar los valores a otras claves del diccionario
                pass
        cadena = str(data)
        texto = ["¿Hay algún problema con esta pregunta?", "Enviar comentarios", "Tiempo finalizado", "Comprobar respuesta", "/", '/n', '\n']
        for text in texto:
            cadena = cadena.replace(text, " ")
        return cadena

class ConsolePrinter:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.bar = "###############################################################################"
        self.line = '-------------------------------------------------------------------------------'

    def print_output(self):
        # Inicializar colorama
        init()
        # Dar formato al texto
        print(Fore.RED + self.bar +"\n"+ Style.RESET_ALL)
        print(Fore.GREEN + self.question + "\n"+Style.RESET_ALL)
        print(Fore.RED + self.line + "\n"+Style.RESET_ALL)
        print(Fore.GREEN + self.answer + "\n" + Style.RESET_ALL)


def generar(path):
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image),
                     cv2.COLOR_RGB2BGR)
        cv2.imwrite(path, image)
def main():
    openai = OpenAI(api_key=api)
    detector = TextDetector(credentials_path=json_txt)
    generar(path='image1.png')
    processor = ImageProcessor(image_path="image1.png")
    cropped_image = processor.crop_image(x1=50, y1=150, x2=1500, y2=600)
    cv2.imwrite("cropped_image.png", cropped_image)
    texts = detector.detect_text(image_path="cropped_image.png")
    message_processor = MessageProcessor(texts=texts)
    message = message_processor.process_message()

    response = openai.get_response(message=message)

    printer = ConsolePrinter(question=message, answer=response)
    printer.print_output()


if __name__ == "__main__":
    main()
