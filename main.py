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
    embed_git = discord.Embed(title="Repositorio de Github: ", color=0x00ff00)
    embed_git.description = "https://github.com/Nicolukazzz/botpoke"
    await ctx.send(embed=embed_git)

@bot.command(name='ayuda')
async def ayuda(ctx):
    embed = discord.Embed(title="¡Ola!", color=0x00ff00)
    embed.description = "*Bot creado por Nicolás*"

    embed.add_field(name="¿Cómo usarlo?", value="""
    * **!ayuda:** Muestra este mensaje de ayuda.
    * **!code:** Muestra el link del código choroto.
    * **!poke [nombre del Pokémon] [shiny (opcional)]:** Muestra la imagen del Pokémon que escribas, algunas de sus estadísticas. Escribe "shiny" como segundo argumento para ver su forma shiny. Puedes escribir el nombre como quieras, con mayúsculas, minúsculas o con espacios.
    """, inline=False)

    embed.add_field(name="Ejemplos:", value="""
    `!poke pikachu`
    `!poke pikachu shiny`
    """, inline=False)

    embed.set_footer(text="El bot utiliza la API de PokeAPI para buscar la imagen y estadísticas del Pokémon - Creado en Python con la librería Discord y otras cositas (!code para más información).")

    await ctx.send(embed=embed)


@bot.command(name='poke')
async def poke(ctx, arg, arg_shiny: str = None):
    try:
        pokemon = arg.split(" ", 1)[0].lower()
        result = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon)
        
        if result.status_code != 200:
            await ctx.send("Pokémon no encontrado :c")
            return 


        abilities = result.json()['abilities']
        first_ability_url = abilities[0]['ability']['name']
        second_ability_url = abilities[1]['ability']['name'] if len(abilities) > 1 else "Ninguna"
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
            back_image_url = image_url_shiny_back
            back_filename = "pokemon_shiny_back.png"
        else:
            image_url = image_url_front
            filename = "pokemon.png"
            back_image_url = image_url_back
            back_filename = "pokemon_back.png"


        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        resized_img = img.resize((300, 300))
        
        buffer = BytesIO()
        resized_img.save(buffer, format="PNG")
        buffer.seek(0)
        
        file_front= discord.File(fp=buffer, filename=filename)


        response_back = requests.get(back_image_url)
        img_back = Image.open(BytesIO(response_back.content))
        resized_img_back = img_back.resize((300, 300))
        
        buffer_back = BytesIO()
        resized_img_back.save(buffer_back, format="PNG")
        buffer_back.seek(0)

        file_back = discord.File(fp=buffer_back, filename=back_filename)

        await ctx.send(files=[file_front, file_back])


        embed_title = f"Estadísticas de *{pokemon.capitalize()}{' Shiny' if arg_shiny and arg_shiny.lower() == 'shiny' else ''}*"
        embed = discord.Embed(title=embed_title, color=0x00ff00)
        embed.add_field(name="Altura", value=f"{height_url}", inline=True)
        embed.add_field(name="Peso", value=f"{weight_url}", inline=True)
        embed.add_field(name="Tipo", value=f"{type_url.capitalize()}", inline=True)
        embed.add_field(name="Habilidades", value=f"- {first_ability_url.capitalize()}\n- {second_ability_url.capitalize()}", inline=False)
        embed.set_thumbnail(url=image_url)

        await ctx.send(embed=embed)

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
