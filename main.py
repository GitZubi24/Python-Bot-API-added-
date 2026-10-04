import requests
import random
import os
import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
bot.remove_command('help')

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def help(ctx):
    help_text = '''
    Comandos disponibles:
    /help - Muestra esta lista de comandos
    /random_meme - Envía un meme aleatorio desde la carpeta "images"
    /get_duck - Envía una imagen aleatoria de un pato
    /open_meme - Envía un meme por probabilidad de programación
    '''
    await ctx.send(help_text)

@bot.command()
async def random_meme(ctx):
    # Vamos a obtener la ruta de la carpeta "images" y luego listaremos todos los archivos en esa carpeta.
    image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
    fl = os.listdir(image_dir)
    choice = random.choice(fl)
    with open(os.path.join(image_dir, choice), 'rb') as f:
        # ¡Vamos a almacenar el archivo de la biblioteca Discord convertido en esta variable!
        picture = discord.File(f)
    # A continuación, podemos enviar este archivo como parámetro.
    await ctx.send(file=picture)

@bot.command()
async def open_meme(ctx):
    await ctx.send("¡Veamos qué meme aleatorio podemos encontrar!")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 70% de probabilidad de elegir programación y 30% de elegir "otros"
    categoria = random.choices(
        ["programacion", "otros"],
        weights=[60, 40],
        k=1
    )[0]
    category_dir = os.path.join(base_dir, "images", categoria)
    imagenes = os.listdir(category_dir)
    imagen = random.choice(imagenes)
    image_path = os.path.join(category_dir, imagen)
    await ctx.send(file=discord.File(image_path))

@bot.command()
async def get_duck(ctx):
    '''Una vez que llamamos al comando duck, 
    el programa llama a la función get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

bot.run("Your Token Here")
