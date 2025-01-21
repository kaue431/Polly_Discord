import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True  # Habilitar leitura de mensagens

bot = commands.Bot(command_prefix="Polly ", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} está online!")

# Carregar os módulos
async def main():
    try:
        # Carregar módulo de música
        await bot.load_extension("cogs.music")
        print("Módulo de música carregado com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar o módulo de música: {e}")

    try:
        # Carregar módulo de respostas inteligentes
        await bot.load_extension("cogs.respostas")  
        print("Módulo de respostas inteligentes carregado com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar o módulo de respostas inteligentes: {e}")

    try:
        # Carregar módulo de traduções
        await bot.load_extension("cogs.traducoes")  
        print("Módulo de traduções carregado com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar o módulo de traduções: {e}")

    try:
        # Carregar módulo de recomendação
        await bot.load_extension("cogs.recomendacao")  
        print("Módulo de recomendação carregado com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar o módulo de recomendação: {e}")

    try:
        # Carregar módulo de simulador
        await bot.load_extension("cogs.simulador")  
        print("Módulo de simulador carregado com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar o módulo de simulador: {e}")

    try:
        # Carregar módulo de geração
        await bot.load_extension("cogs.geracao")  
        print("Módulo de geração carregado com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar o módulo de geração: {e}")

    try:
        # Carregar módulo de eventos
        await bot.load_extension("cogs.eventos")  
        print("Módulo de eventos carregado com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar o módulo de eventos: {e}")

    try:
        # Carregar módulo de revisao
        await bot.load_extension("cogs.revisao")  
        print("Módulo de revisao carregado com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar o módulo de revisao: {e}")

    try:
        # Carregar módulo de rank
        await bot.load_extension("cogs.rank")  
        print("Módulo de rank carregado com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar o módulo de rank: {e}")

    try:
        # Carregar módulo de cursos
        await bot.load_extension("cogs.cursos")  
        print("Módulo de cursos carregado com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar o módulo de cursos: {e}")

    # Substitua pelo token do seu bot
    await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
