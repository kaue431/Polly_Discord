import discord
from discord.ext import commands


class RankConquistas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conquistas = [
            {"nome": "Primeira Mensagem", "descricao": "Envie sua primeira mensagem no servidor.", "xp": 10},
            {"nome": "Interação Ativa", "descricao": "Envie 100 mensagens no servidor.", "xp": 100},
            {"nome": "Mestre do Chat", "descricao": "Envie 1.000 mensagens no servidor.", "xp": 1000},
            {"nome": "Líder de Ranking", "descricao": "Alcance o primeiro lugar no ranking.", "xp": 5000},
        ]
        self.ranking = {}  # Estrutura do ranking: {user_id: {"nome": "Usuário", "xp": 1000, "conquistas": []}}

    @commands.Cog.listener()
    async def on_message(self, message):
        """Evento para adicionar XP quando uma mensagem for enviada."""
        if message.author.bot:
            return  # Ignorar mensagens de bots

        user_id = message.author.id

        if user_id not in self.ranking:
            self.ranking[user_id] = {"nome": message.author.name, "xp": 0, "conquistas": []}

        # Incrementa o XP
        self.ranking[user_id]["xp"] += 10  # XP por mensagem enviada
        await self.verificar_conquistas(message.channel, user_id)

    async def verificar_conquistas(self, channel, user_id):
        """Verifica e desbloqueia conquistas com base no XP."""
        usuario = self.ranking[user_id]
        xp_atual = usuario["xp"]

        for conquista in self.conquistas:
            if conquista["nome"] not in usuario["conquistas"] and xp_atual >= conquista["xp"]:
                usuario["conquistas"].append(conquista["nome"])
                await channel.send(
                    f":trophy: **{usuario['nome']}** desbloqueou a conquista: **{conquista['nome']}**! "
                    f"Descrição: *{conquista['descricao']}*"
                )

    @commands.command()
    async def ranking(self, ctx):
        """Exibe o ranking dos usuários."""
        if not self.ranking:
            await ctx.send(":medal: O ranking está vazio no momento.")
            return

        # Ordena o ranking por XP
        sorted_ranking = sorted(
            self.ranking.items(), key=lambda item: item[1]["xp"], reverse=True
        )

        embed = discord.Embed(
            title="Ranking do Servidor",
            description="Aqui está o ranking atualizado dos usuários:",
            color=discord.Color.blue(),
        )
        for idx, (user_id, dados) in enumerate(sorted_ranking, start=1):
            user = self.bot.get_user(user_id) or f"Usuário {user_id}"  # Garante nome mesmo se o ID não corresponder
            embed.add_field(
                name=f"#{idx} - {user}",
                value=f"XP: {dados['xp']}",
                inline=False,
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def conquistas(self, ctx):
        """Exibe todas as conquistas disponíveis."""
        embed = discord.Embed(
            title="Conquistas Disponíveis",
            description="Aqui estão todas as conquistas que você pode desbloquear:",
            color=discord.Color.gold(),
        )
        for c in self.conquistas:
            embed.add_field(name=c["nome"], value=c["descricao"], inline=False)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(RankConquistas(bot))
