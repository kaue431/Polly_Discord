import discord
from discord.ext import commands
import requests

# Substitua com sua chave de API e ID do mecanismo de pesquisa
API_KEY = "AIzaSyAvLE-yj2aPXsaveLWKnnj9NTr0-0hGVGc"
CX = "d594cf9b711554fb8"

# Função para realizar a busca
def google_search(query):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": API_KEY,
        "cx": CX,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro na API: {response.text}")

# Classe para o bot
class GoogleSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def search(self, ctx, *, query):
        """
        Realiza uma pesquisa no Google e retorna os resultados.
        Exemplo de uso: Polly search Python programming
        """
        await ctx.send("🔎 Buscando informações, por favor aguarde...")
        try:
            results = google_search(query)
            if "items" in results:
                for item in results["items"][:3]:  # Mostra os 3 primeiros resultados
                    await ctx.send(f"**{item['title']}**\n{item['link']}\n{item.get('snippet', 'Sem descrição')}\n")
            else:
                await ctx.send("❌ Nenhum resultado encontrado.")
        except Exception as e:
            await ctx.send(f"❌ Erro ao buscar informações: {e}")

# Adicionar o módulo ao bot
async def setup(bot):
    await bot.add_cog(GoogleSearch(bot))
