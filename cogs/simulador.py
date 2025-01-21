import discord
from discord.ext import commands
import random
import requests

class Simulador(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.search_api_key = "AIzaSyAvLE-yj2aPXsaveLWKnnj9NTr0-0hGVGc"  # Substitua por sua chave da API de pesquisa
        self.search_engine_id = "d594cf9b711554fb8"    # Substitua pelo seu ID do mecanismo de pesquisa (CX)

    @commands.command(name="entrevista")
    async def entrevista(self, ctx, tipo: str, area: str):
        """
        Simulador de entrevistas com avaliação detalhada.
        Uso: Polly entrevista <tipo> <área>
        """
        tipo = tipo.lower()
        area = area.lower()

        await ctx.send(
            f"Buscando informações sobre **{area.capitalize()}** para gerar perguntas..."
        )

        # Buscar informações na API
        try:
            perguntas = self.obter_perguntas(tipo, area)
        except Exception as e:
            await ctx.send(f"Erro ao buscar informações: {e}")
            return

        if not perguntas:
            await ctx.send("Não consegui gerar perguntas para essa área. Tente novamente com outra.")
            return

        await ctx.send(
            f"**Iniciando a entrevista de {tipo.capitalize()} na área de {area.capitalize()}.**"
        )

        respostas = []
        for i, pergunta in enumerate(perguntas, 1):
            await ctx.send(f"**Pergunta {i}:** {pergunta}")

            try:
                resposta = await self.bot.wait_for(
                    "message",
                    timeout=60.0,
                    check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                )
                respostas.append(resposta.content)
                await ctx.send(f"Resposta registrada: {resposta.content}")
            except discord.TimeoutError:
                await ctx.send("Tempo esgotado para responder. A entrevista foi encerrada.")
                return

        # Avaliação da entrevista
        await ctx.send("**Entrevista concluída! Avaliando suas respostas...**")
        await self.avaliar_entrevista(ctx, respostas, perguntas, area)

    def obter_perguntas(self, tipo, area):
        """Busca informações na API e gera perguntas com base nos resultados."""
        search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.search_api_key,
            "cx": self.search_engine_id,
            "q": f"{tipo} na área de {area}",
            "num": 5,
        }
        response = requests.get(search_url, params=params)

        if response.status_code != 200:
            raise Exception("Erro na API de pesquisa.")

        data = response.json()
        items = data.get("items", [])

        # Gerar perguntas com base nos resultados
        perguntas = []
        for item in items:
            perguntas.append(f"O que você sabe sobre {item.get('title', 'essa área')}?")
            perguntas.append(f"Como você aplicaria {item.get('snippet', 'esse conceito')} no trabalho?")
        
        return perguntas

    async def avaliar_entrevista(self, ctx, respostas, perguntas, area):
        """Avalia as respostas com base nas perguntas e informações da área."""
        if not respostas:
            await ctx.send("Nenhuma resposta fornecida. Não é possível avaliar.")
            return

        # Avaliar respostas com base em palavras-chave da pesquisa
        palavras_chave = ["dedicação", "conhecimento", "habilidades", "experiência", "aprendizado"]  # Exemplos
        feedback_detalhado = []
        acertos = 0

        for i, resposta in enumerate(respostas):
            resposta_feedback = {
                "pergunta": perguntas[i],
                "resposta": resposta,
                "feedback": [],
            }
            encontrou_chave = False

            for palavra in palavras_chave:
                if palavra.lower() in resposta.lower():
                    encontrou_chave = True
                    acertos += 1
                    resposta_feedback["feedback"].append(
                        f"A resposta abordou a palavra-chave: **{palavra}**"
                    )

            if not encontrou_chave:
                resposta_feedback["feedback"].append(
                    "A resposta não abordou nenhuma das palavras-chave esperadas. "
                    "Tente incluir mais detalhes ou termos técnicos específicos da área."
                )

            feedback_detalhado.append(resposta_feedback)

        # Calcular a nota final
        nota = min(10, acertos + random.randint(0, 2))  # Adiciona um pouco de aleatoriedade

        # Feedback geral com base na nota
        if nota >= 9:
            feedback_geral = "Excelente! Você demonstrou ótimo conhecimento e habilidades."
        elif nota >= 7:
            feedback_geral = "Bom trabalho! Algumas melhorias podem te levar ainda mais longe."
        else:
            feedback_geral = "Precisa melhorar. Continue estudando e praticando!"

        # Enviar feedback detalhado
        for item in feedback_detalhado:
            await ctx.send(f"**Pergunta:** {item['pergunta']}")
            await ctx.send(f"**Sua Resposta:** {item['resposta']}")
            for fb in item["feedback"]:
                await ctx.send(f"- {fb}")

        # Enviar nota final e feedback geral
        await ctx.send(f"**Sua nota final: {nota}/10**")
        await ctx.send(f"**Feedback Geral:** {feedback_geral}")

async def setup(bot):
    await bot.add_cog(Simulador(bot))
