# ██████╗  ██████╗ ██╗  ██╗███████╗███╗   ███╗ █████╗ ███╗   ██╗
# ██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝████╗ ████║██╔══██╗████╗  ██║
# ██████╔╝██║   ██║█████╔╝ █████╗  ██╔████╔██║███████║██╔██╗ ██║
# ██╔═══╝ ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╔╝██║██╔══██║██║╚██╗██║
# ██║     ╚██████╔╝██║  ██╗███████╗██║ ╚═╝ ██║██║  ██║██║ ╚████║
# ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
                                                              
                                                                               
from PIL import Image
from io import BytesIO
import discord
from discord.ext import commands
import requests
import os
import webserver
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix= '!', intents=intents)

@bot.command(name='code')
async def code(ctx):
    await ctx.send("https://github.com/Nicolukazzz/botds/blob/main/code")

@bot.command(name='ayuda')
async def ayuda(ctx):
    # Crear el mensaje de ayuda básico
    help_message = """
**¡ola!** 

*Bot creado por Nicolás.*
*Este bot nació en una noche de inspiración inesperada (distorsión de la realidad).*

**¿Cómo usarlo?**

* **!ayuda:** Muestra este mensaje de ayuda.
* **!code:** Muestra el link del código choroto.
* **!poke [nombre del Pokémon] [back (opcional)]:** Muestra la imagen sobre el Pokémon que escribas, algunas de sus estadísticas y con el argumento "back" podrás ver al pokemón de espalda. Y ya, literalmente no hace nada más kajsdkasd (por ahora). Puedes escribir el nombre como quieras, con mayúsculas, minúsculas o con espacios.

**Ejemplos:**
`!poke pikachu`
`!poke pikachu back`

*El bot utiliza la API de PokeAPI para buscar la imagen y estadísticas del Pokémon - Creado en Python con la libreria Discord y otras cositas (!code para más información).*
    """
    await ctx.send(help_message)

@bot.command(name='poke')
async def poke(ctx, arg, arg2: str = None):
    try:
        pokemon = arg.split(" ", 1)[0].lower()
        #perfil = arg2.split(" ", 1)[0].lower()
        result = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon)
        
        if result.status_code !=200:
            await ctx.send("Pokémon no encontrado :c")
        else:
            height_url = result.json()['height']
            weight_url = result.json()['weight']
            type_url = result.json()['types'][0]['type']['name']
            image_url = result.json()['sprites']['front_default']
            imageback_url = result.json()['sprites']['back_default']

            #Frente
            response = requests.get(image_url)
            
            img = Image.open(BytesIO(response.content))
            resized_img = img.resize((300, 300))
            
            buffer = BytesIO()
            resized_img.save(buffer, format="PNG")
            buffer.seek(0)
            
            await ctx.send(file=discord.File(fp=buffer, filename="pokemon.png"))

            #Espalda
            if arg2 and arg2.lower() == "back":
                response_back = requests.get(imageback_url)

                img_back = Image.open(BytesIO(response_back.content))
                resized_img_back = img_back.resize((300, 300))
                
                buffer_back = BytesIO()
                resized_img_back.save(buffer_back, format="PNG")
                buffer_back.seek(0)

                await ctx.send(file=discord.File(fp=buffer_back, filename="pokemon_back.png"))
            else:
                await ctx.send("*Si quieres ver la imagen por la parte trasera, usa el argumento 'back' después del nombre 🫵🏿*")
            await ctx.send(f"""*---Estadísticas---*
                           
**Altura: {height_url}**
**Peso: {weight_url}**
**Tipo: {type_url.capitalize()}**""")
    except Exception as e:
        print(f"Error: {e}")


@poke.error
async def error_type(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Debes pasarme un Pokemon >:)")

webserver.keep_alive()

try:
    bot.run(DISCORD_TOKEN)
except Exception as e:
    print(f"Error al encender el bot. Error: {e}")
