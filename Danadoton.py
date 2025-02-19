# python "C:\Users\Guilh\Documents\Programming\Danadoton BOT\Danadoton.py"
# desligar: Crtl+C

import os
import discord
from discord.ext import commands
import random
import re
from dotenv import load_dotenv  # Carregar o token de um arquivo .env

# Carregar variáveis do ambiente 
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # O token agora é lido do arquivo .env

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="//", intents=intents)

# Evento de inicialização
@bot.event
async def on_ready():
    print(f'Bot {bot.user} está online.')

# Comando ping-pong
@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

# Função para processar a rolagem de dados
def rolar_dado(expressao):
    match = re.match(r"(\d*)d(\d+)([+-]\d+)?", expressao)
    if not match:
        return None, None, None, None

    try:
        quantidade = int(match.group(1)) if match.group(1) else 1
        faces = int(match.group(2))
        modificador = int(match.group(3)) if match.group(3) else 0

        if quantidade > 100 or faces > 1000:
            return "Limite de rolagem excedido", None, None, None

        resultados = [random.randint(1, faces) for _ in range(quantidade)]
        total = sum(resultados) + modificador

        return resultados, modificador, total, faces

    except ValueError:
        return None, None, None, None

# Evento para capturar mensagens e interpretar comandos de dados
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    match = re.match(r"^//(\d*d\d+([+-]\d+)?)$", message.content)
    if match:
        expressao = match.group(1)
        resultados, modificador, total, faces = rolar_dado(expressao)

        if resultados == "Limite de rolagem excedido":
            await message.reply("O limite para rolagem de dados foi excedido. Use até 100 dados com até 1000 faces cada.")
            return

        if resultados is None:
            await message.reply("Formato inválido. Tente algo como `1d20+2`.")
            return

        resultados_str = " + ".join(
            f"[**{r}**]" if r == faces or r == 1 else f"[{r}]" for r in resultados
        )

        modificador_str = f" {modificador:+}" if modificador != 0 else ""
        expressao_sem_modificador = expressao.split('+')[0] if '+' in expressao else expressao.split('-')[0]

        if any(result == faces for result in resultados):
            mensagem_final = f"{expressao_sem_modificador} {resultados_str}{modificador_str} ⟶ ` {total} ` **Puro e Natural** 🌱"
        elif any(result == 1 for result in resultados):
            mensagem_final = f"{expressao_sem_modificador} {resultados_str}{modificador_str} ⟶ ` {total} ` (**Vixe!**) "
        else:
            mensagem_final = f"{expressao_sem_modificador} {resultados_str}{modificador_str} ⟶ ` {total} `"

        await message.reply(mensagem_final)
    
    await bot.process_commands(message)  # Permite que outros comandos continuem funcionando

# Rodar o bot
bot.run(TOKEN)
