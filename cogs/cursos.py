import discord
from discord.ext import commands
import requests

class CursosBasicos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = "AIzaSyAvLE-yj2aPXsaveLWKnnj9NTr0-0hGVGc"  # Substitua pela sua API Key
        self.cx = "d594cf9b711554fb8"  # Substitua pelo seu ID do mecanismo de pesquisa personalizado

    def pesquisar_tema(self, tema):
        """Realiza uma pesquisa no Google para obter informações sobre o tema."""
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.api_key,
            "cx": self.cx,
            "q": tema,
            "hl": "pt-BR"  # Define o idioma da pesquisa para português
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            resultados = response.json().get("items", [])
            conteudo = []
            for item in resultados[:3]:  # Obtém até 3 resultados relevantes
                conteudo.append(item.get("snippet", ""))
            return " ".join(conteudo)
        else:
            return None

    def gerar_aula(self, tema, conteudo_pesquisado):
        """Gera uma estrutura de aula básica com base no conteúdo pesquisado."""
        detalhes = (
            conteudo_pesquisado[:1500] + "..." if conteudo_pesquisado and len(conteudo_pesquisado) > 1500 else conteudo_pesquisado
        )
        aula = {
            "tema": tema,
            "resumo": conteudo_pesquisado[:300] + "..." if conteudo_pesquisado else "Resumo não disponível.",
            "topicos": [
                "Introdução ao tema",
                "Principais características",
                "Importância do tema na sociedade",
                "Exemplos e aplicações práticas"
            ],
            "detalhes": detalhes if detalhes else "Detalhes não disponíveis."
        }
        return aula

    def dividir_mensagem(self, mensagem, limite=2000):
        """Divide uma mensagem longa em partes menores de até 2000 caracteres."""
        partes = []
        while len(mensagem) > limite:
            indice = mensagem.rfind("\n", 0, limite)  # Divide no último ponto ou quebra de linha
            if indice == -1:
                indice = limite
            partes.append(mensagem[:indice])
            mensagem = mensagem[indice:].strip()
        partes.append(mensagem)
        return partes

    @commands.command()
    async def curso(self, ctx, *, tema):
        """Cria um curso básico sobre o tema solicitado pelo usuário."""
        await ctx.send(f":books: Gerando uma aula básica sobre **{tema}**, aguarde...")
        conteudo_pesquisado = self.pesquisar_tema(tema)
        if conteudo_pesquisado:
            aula = self.gerar_aula(tema, conteudo_pesquisado)
            mensagem = (
                f"**Tema:** {aula['tema']}\n\n"
                f"**Resumo:** {aula['resumo']}\n\n"
                f"**Tópicos Principais:**\n"
                f"- {aula['topicos'][0]}\n"
                f"- {aula['topicos'][1]}\n"
                f"- {aula['topicos'][2]}\n"
                f"- {aula['topicos'][3]}\n\n"
                f"**Detalhes Adicionais:**\n{aula['detalhes']}"
            )
            partes = self.dividir_mensagem(mensagem)
            for parte in partes:
                await ctx.send(parte)
        else:
            await ctx.send(f":x: Não foi possível encontrar informações sobre **{tema}**. Tente um tema diferente.")

async def setup(bot):
    await bot.add_cog(CursosBasicos(bot))
