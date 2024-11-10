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
    await ctx.send("https://github.com/Nicolukazzz/botpoke")

@bot.command(name='ayuda')
async def ayuda(ctx):
    # Crear el mensaje de ayuda básico
    help_message = """
**¡ola!** 

**Creado por Nicolás**
*Este bot nació en una noche de inspiración inesperada.*

**¿Cómo usarlo?**

* **!ayuda:** Muestra este mensaje de ayuda.
* **!code:** Muestra el link del código choroto.
* **!poke [nombre del Pokémon]:** Muestra una imagen sobre el Pokémon que escribas. Y ya, literalmente no hace nada más kajsdkasd (por ahora). Puedes escribir el nombre como quieras, con mayúsculas, minúsculas o con espacios.

**Ejemplo:**
`!poke pikachu`

*El bot utiliza la API de PokeAPI para buscar la imagen del Pokémon - Creado en Python con la libreria Discord y otras cositas.*
    """
    await ctx.send(help_message)

@bot.command(name='poke')
async def poke(ctx, arg):
    try:
        pokemon = arg.split(" ", 1)[0].lower()
        result = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon)
        
        if result.status_code == 404:
            await ctx.send("Pokémon no encontrado :c")
        else:
            image_url = result.json()['sprites']['front_default']
            response = requests.get(image_url)
            
            img = Image.open(BytesIO(response.content))
            resized_img = img.resize((300, 300))
            
            buffer = BytesIO()
            resized_img.save(buffer, format="PNG")
            buffer.seek(0)
            
            await ctx.send(file=discord.File(fp=buffer, filename="pokemon.png"))
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
