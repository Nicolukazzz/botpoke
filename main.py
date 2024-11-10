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
async def poke(ctx, arg, arg_shiny: str = None, arg_back: str = None):
    try:
        pokemon = arg.split(" ", 1)[0].lower()
        result = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon)
        
        if result.status_code != 200:
            await ctx.send("Pokémon no encontrado :c")
            return 

        
        height_url = result.json()['height']
        weight_url = result.json()['weight']
        type_url = result.json()['types'][0]['type']['name']
        image_url_front = result.json()['sprites']['front_default']
        image_url_back = result.json()['sprites']['back_default']
        image_url_shiny_front = result.json()['sprites']['front_shiny']
        image_url_shiny_back = result.json()['sprites']['back_shiny']

        
        if arg_shiny and arg_shiny.lower() == "shiny":
            image_url = image_url_shiny_front
            filename = "pokemon_shiny.png"
        else:
            image_url = image_url_front
            filename = "pokemon.png"

        
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        resized_img = img.resize((300, 300))
        
        buffer = BytesIO()
        resized_img.save(buffer, format="PNG")
        buffer.seek(0)
        
        await ctx.send(file=discord.File(fp=buffer, filename=filename))

   
        if arg_back and arg_back.lower() == "back":
            if arg_shiny and arg_shiny.lower() == "shiny":
                image_url_back_to_send = image_url_shiny_back
                back_filename = "pokemon_shiny_back.png"
            else:
                image_url_back_to_send = image_url_back
                back_filename = "pokemon_back.png"

            response_back = requests.get(image_url_back_to_send)
            if response_back.status_code == 200:
                img_back = Image.open(BytesIO(response_back.content))
                resized_img_back = img_back.resize((300, 300))
                
                buffer_back = BytesIO()
                resized_img_back.save(buffer_back, format="PNG")
                buffer_back.seek(0)

                await ctx.send(file=discord.File(fp=buffer_back, filename=back_filename))
            else:
                await ctx.send("No se pudo obtener la imagen de la parte trasera.")

        
        await ctx.send(f"""*---Estadísticas---*
                           
**Altura: {height_url}**
**Peso: {weight_url}**
**Tipo: {type_url.capitalize()}**""")
    except Exception as e:
        print(f"Error: {e}")
        await ctx.send("Ha ocurrido un error al intentar consultar la API")



@poke.error
async def error_type(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Debes pasarme un Pokemon >:)")

webserver.keep_alive()

try:
    bot.run(DISCORD_TOKEN)
except Exception as e:
    print(f"Error al encender el bot. Error: {e}")
