import discord
from discord.ext import commands, tasks
from datetime import datetime

class Eventos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.eventos = []
        self.eventos_verificacao.start()

    @commands.command()
    async def criar_evento(self, ctx, nome: str, tema: str, data: str, *, mensagem: str):
        """
        Cria um novo evento temático.
        Formato da data: DD/MM/YY
        """
        try:
            # Converte e valida a data no formato DD/MM/YY
            data_formatada = datetime.strptime(data, "%d/%m/%y")
            self.eventos.append({"nome": nome, "tema": tema, "data": data_formatada, "mensagem": mensagem})
            await ctx.send(f":white_check_mark: Evento **{nome}** criado com sucesso para o dia {data_formatada.strftime('%d/%m/%Y')}!")
        except ValueError:
            await ctx.send(":x: Formato de data inválido. Use o formato DD/MM/YY.")

    @commands.command()
    async def listar_eventos(self, ctx):
        """Lista todos os eventos futuros."""
        if not self.eventos:
            await ctx.send(":calendar: Não há eventos cadastrados.")
            return

        mensagem = ":tada: **Eventos Futuros**:\n"
        for evento in self.eventos:
            mensagem += f"- **{evento['nome']}** ({evento['tema']}) em {evento['data'].strftime('%d/%m/%Y')}\n"
        await ctx.send(mensagem)

    @commands.command()
    async def deletar_evento(self, ctx, nome: str):
        """Remove um evento pelo nome."""
        for evento in self.eventos:
            if evento["nome"].lower() == nome.lower():
                self.eventos.remove(evento)
                await ctx.send(f":white_check_mark: Evento **{nome}** foi removido com sucesso.")
                return
        await ctx.send(f":x: Não foi encontrado nenhum evento com o nome **{nome}**.")

    @tasks.loop(minutes=1)
    async def eventos_verificacao(self):
        """Verifica se há eventos no dia atual para notificar."""
        agora = datetime.now()
        for evento in list(self.eventos):  # Copia da lista para evitar problemas ao remover
            if evento["data"].date() == agora.date():
                canal = self.bot.get_channel(1204135960019730473/1324878097576624270)  # Substitua pelo ID do seu canal
                if canal:
                    await canal.send(f":tada: Hoje é dia do evento **{evento['nome']}**!\nTema: **{evento['tema']}**\nMensagem: {evento['mensagem']}")
                self.eventos.remove(evento)

    @eventos_verificacao.before_loop
    async def before_eventos_verificacao(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Eventos(bot))
