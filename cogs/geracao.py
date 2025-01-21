import discord
from discord.ext import commands
import cohere

# Substitua pela sua chave de API do Cohere
COHERE_API_KEY = "uteoGKiDJHdZyukFWFo3jfb6VVYp0wrKIEPjXOr6"

class Geracao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cohere_client = cohere.Client(COHERE_API_KEY)

    @commands.command(name="gerar")
    async def gerar_texto(self, ctx, tipo: str, *, tema: str):
        """
        Gera um texto ou poema baseado no tipo e no tema fornecidos.
        :param tipo: 'texto' ou 'poema'
        :param tema: Tema do texto ou poema
        """
        await ctx.send("⏳ Gerando sua criação, aguarde...")

        if tipo.lower() not in ["texto", "poema"]:
            await ctx.send("❌ Tipo inválido. Use 'texto' ou 'poema'.")
            return

        # Instruções claras para geração em português
        prompt = (
            f"Crie um {tipo.lower()} em português sobre o tema '{tema}'. "
            "Certifique-se de que o conteúdo seja criativo, coeso e em linguagem natural."
        )

        try:
            response = self.cohere_client.generate(
                model="command",  # Modelo padrão do Cohere
                prompt=prompt,
                max_tokens=300,  # Número máximo de tokens na resposta
                temperature=0.7,  # Controle da criatividade do texto
            )

            if response.generations:
                resultado = response.generations[0].text.strip()
                await ctx.send(f"✨ Aqui está o {tipo.lower()} gerado com o tema '{tema}':\n\n{resultado}")
            else:
                await ctx.send("❌ Não foi possível gerar um resultado. Tente novamente.")
        except Exception as e:
            await ctx.send(f"❌ Erro ao gerar {tipo.lower()}: {str(e)}")

# Configuração para adicionar o módulo ao bot
async def setup(bot):
    await bot.add_cog(Geracao(bot))
