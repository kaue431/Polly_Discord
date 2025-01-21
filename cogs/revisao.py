import discord
from discord.ext import commands
import cohere
import os

class Revisao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Obtém a chave da API da Cohere
        self.api_key = os.getenv('CO_API_KEY') or "uteoGKiDJHdZyukFWFo3jfb6VVYp0wrKIEPjXOr6"

        if not self.api_key or self.api_key == "SUA_CHAVE_AQUI":
            raise ValueError("A chave da API da Cohere (CO_API_KEY) não foi configurada corretamente. "
                             "Defina a variável de ambiente ou insira a chave no código.")

        # Inicializa o cliente da Cohere
        self.cohere_client = cohere.Client(self.api_key)

    @commands.command()
    async def revisar(self, ctx, *, texto):
        """
        Revise um texto e forneça feedback detalhado.
        Uso: !revisar <texto>
        """
        await ctx.send(":pencil: Analisando o texto, por favor aguarde...")

        try:
            # Solicita à API da Cohere a revisão do texto
            resposta = self.cohere_client.generate(
                model="command-xlarge-nightly",
                prompt=(
                    "Você é um revisor de textos. Analise o seguinte texto, identificando erros gramaticais, "
                    "sugestões de melhoria e se o texto está correto ou não. "
                    "Se estiver perfeito, retorne apenas: 'Texto correto. Excelente trabalho!'. "
                    "Caso contrário, forneça as informações:\n"
                    "- Quantidade de erros.\n"
                    "- Sugestões específicas para corrigir os erros encontrados.\n\n"
                    f"Texto: {texto}"
                ),
                max_tokens=300,
                temperature=0.5
            )

            feedback = resposta.generations[0].text.strip()

            # Garante que a resposta seja exibida corretamente
            if len(feedback) > 2000:
                feedback = feedback[:1997] + "..."

            await ctx.send(f":white_check_mark: Revisão Concluída:\n{feedback}")

        except cohere.CohereError as e:
            await ctx.send(f":x: Erro ao revisar o texto: {e}")
        except Exception as e:
            await ctx.send(f":x: Ocorreu um erro inesperado: {e}")

async def setup(bot):
    await bot.add_cog(Revisao(bot))
