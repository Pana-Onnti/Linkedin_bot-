import discord
import requests


api_discord = 'MTA5NzY1NjMzNjI4MTUwMTY5Ng.Gb62-k.7i-zwAmkv5E5-s3WjtTmV0AWX2hryF-0YKC7og'
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
from peticion import OpenAI ,TextDetector ,MessageProcessor,api_key,json_txt

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game('Tirando notas'))


@client.event
async def on_ready():
    print('Bot iniciado como {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!ojo'):
        # Comprobar si el mensaje tiene algún archivo adjunto
        if len(message.attachments) > 0:
            # Descargar la imagen del archivo adjunto
            url = message.attachments[0].url
            response = requests.get(url)
            
            # Guardar la imagen en el disco duro
            with open('foto_guardada.png', 'wb') as f:
                f.write(response.content)
                
            await message.channel.send('¡Foto capturada correctamente!')
            await message.channel.send('¡Esperando Respuesta!')
        else:
            await message.channel.send('¡No se encontró ninguna foto adjunta!')

        
        # #
        detector = TextDetector(credentials_path=json_txt)
        texts = detector.detect_text(image_path="foto_guardada.png")
        message_processor = MessageProcessor(texts=texts)
        mensaje = message_processor.process_message()
        openai = OpenAI(api_key=api_key)
        response = openai.get_response(message=mensaje)

        await message.channel.send(f"Crack sos tu pregunta es\n{mensaje}\n Tu respuesta es \n {response} ")


client.run(api_discord)