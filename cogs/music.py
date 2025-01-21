from discord.ext import commands
import yt_dlp
import discord
import asyncio

# Configurações do yt_dlp
YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
    "quiet": True,
    "no_warnings": True,
}

# Configurações do FFmpeg
FFMPEG_OPTIONS = {
    "before_options": (
        "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 "
        "-nostdin -loglevel quiet -hide_banner"
    ),
    "options": "-vn",
}

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []  # Fila de músicas
        self.current_song = None  # Música atualmente tocando
        self.is_playing = False  # Status de reprodução

    @commands.command()
    async def join(self, ctx):
        """Faz o bot entrar no canal de voz."""
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await channel.connect()
                await ctx.send(f"Conectado ao canal: {channel.name}")
            else:
                await ctx.send("Já estou conectado a um canal de voz.")
        else:
            await ctx.send("Você precisa estar em um canal de voz para usar este comando.")

    @commands.command()
    async def play(self, ctx, *, search: str):
        """Reproduz uma música ou adiciona à fila."""
        vc = ctx.voice_client

        if not vc:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                vc = await channel.connect()
            else:
                return await ctx.send("Você precisa estar em um canal de voz para usar este comando.")

        # Adicionar à fila se já estiver tocando
        if self.is_playing or self.queue:
            await ctx.send(f"🎶 Adicionado à fila: **{search}**")
            self.queue.append(search)
        else:
            await self._play_music(ctx, search)

    async def _play_music(self, ctx, search):
        """Função auxiliar para reproduzir uma música."""
        vc = ctx.voice_client
        self.is_playing = True
        loading_message = await ctx.send("🔄 Carregando a música, aguarde...")

        try:
            with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ytdl:
                info = ytdl.extract_info(f"ytsearch:{search}", download=False)["entries"][0]
                url = info["url"]
                title = info["title"]

            self.current_song = title
            vc.stop()  # Certifica que não há áudio em execução
            vc.play(
                discord.PCMVolumeTransformer(
                    discord.FFmpegPCMAudio(source=url, **FFMPEG_OPTIONS),
                    volume=0.5  # Ajuste de volume padrão
                ),
                after=lambda e: asyncio.run_coroutine_threadsafe(self._next(ctx), self.bot.loop),
            )
            await loading_message.edit(content=f"🎶 Tocando agora: **{title}**")
        except Exception as e:
            self.is_playing = False
            await loading_message.edit(content=f"❌ Ocorreu um erro ao carregar a música: {str(e)}")

    async def _next(self, ctx):
        """Função chamada automaticamente ao terminar uma música."""
        vc = ctx.voice_client
        if self.queue:
            next_song = self.queue.pop(0)
            await self._play_music(ctx, next_song)
        else:
            self.is_playing = False
            self.current_song = None
            if vc:
                await vc.disconnect()

    @commands.command()
    async def pause(self, ctx):
        """Pausa a música atual."""
        vc = ctx.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await ctx.send("⏸ Música pausada.")
        else:
            await ctx.send("Nenhuma música está tocando no momento.")

    @commands.command()
    async def resume(self, ctx):
        """Retoma a música pausada."""
        vc = ctx.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await ctx.send("▶ Música retomada.")
        else:
            await ctx.send("Nenhuma música está pausada no momento.")

    @commands.command()
    async def skip(self, ctx):
        """Pula para a próxima música na fila."""
        vc = ctx.voice_client
        if vc and vc.is_playing():
            vc.stop()  # Para a música atual e chama `_next`
            await ctx.send("⏭ Música pulada.")
        else:
            await ctx.send("Nenhuma música está tocando para pular.")

    @commands.command()
    async def queue(self, ctx):
        """Exibe a fila de músicas."""
        if self.queue:
            queue_list = "\n".join([f"{idx + 1}. {song}" for idx, song in enumerate(self.queue)])
            await ctx.send(f"📜 **Fila de músicas:**\n```\n{queue_list}\n```")
        else:
            await ctx.send("🚫 A fila está vazia no momento.")

    @commands.command()
    async def leave(self, ctx):
        """Faz o bot sair do canal de voz."""
        vc = ctx.voice_client
        if vc:
            await vc.disconnect()
            self.queue.clear()  # Limpa a fila ao sair
            self.is_playing = False
            self.current_song = None
            await ctx.send("Desconectado do canal de voz.")
        else:
            await ctx.send("Eu não estou conectado a nenhum canal de voz.")

async def setup(bot):
    await bot.add_cog(Music(bot))
