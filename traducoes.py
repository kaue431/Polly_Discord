import discord
from discord.ext import commands
from deep_translator import GoogleTranslator  # Alternativa ao googletrans

# Classe do módulo de tradução
class Translation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def translate(self, ctx, target_lang, *, text):
        """
        Traduz um texto para o idioma especificado.
        Uso: !translate <código do idioma> <texto>
        Exemplo: !translate pt Hello, how are you?
        """
        await ctx.send(":earth_africa: Traduzindo, por favor aguarde...")
        try:
            # Realiza a tradução
            translated_text = GoogleTranslator(target=target_lang).translate(text)
            await ctx.send(f":white_check_mark: Tradução concluída:\n**{translated_text}**")
        except Exception as e:
            await ctx.send(f":x: Erro ao traduzir: {e}")

# Função para adicionar o módulo ao bot
async def setup(bot):
    await bot.add_cog(Translation(bot))