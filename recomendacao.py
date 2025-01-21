import discord
from discord.ext import commands
import requests
from unidecode import unidecode

class Recomendacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.TMDB_API_KEY = "68f03abe2f8060924d95c90197919807"
        self.ANILIST_CLIENT_ID = "23668"
        self.ANILIST_CLIENT_SECRET = "npl37Fvf5hJpxw6PtvFjNOyS5gJDKHt6GUbsWiol"
        self.GOOGLE_BOOKS_API_KEY = "AIzaSyAvLE-yj2aPXsaveLWKnnj9NTr0-0hGVGc"

        # Gêneros disponíveis para filmes e séries na TMDB
        self.TMDB_GENRES = {
            "ação": 28,
            "aventura": 12,
            "animação": 16,
            "comédia": 35,
            "crime": 80,
            "documentário": 99,
            "drama": 18,
            "família": 10751,
            "fantasia": 14,
            "história": 36,
            "terror": 27,
            "música": 10402,
            "mistério": 9648,
            "romance": 10749,
            "ficção científica": 878,
            "cinema tv": 10770,
            "thriller": 53,
            "guerra": 10752,
            "faroeste": 37,
        }

    def normalizar_genero(self, genero):
        """Remove acentos e coloca o gênero em minúsculas para evitar erros."""
        return unidecode(genero.lower())

    def get_anime_recommendations(self, genero):
        """Busca recomendações de animes no AniList."""
        query = """
        query ($genre: String) {
          Page(perPage: 5) {
            media(genre: $genre, type: ANIME, sort: POPULARITY_DESC) {
              title {
                romaji
                english
              }
            }
          }
        }
        """
        variables = {"genre": genero.capitalize()}
        url = "https://graphql.anilist.co"
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(
                url, json={"query": query, "variables": variables}, headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                return [
                    anime["title"]["romaji"] or anime["title"]["english"]
                    for anime in data["data"]["Page"]["media"]
                ]
            else:
                print(response.status_code, response.text)
        except Exception as e:
            print(f"Erro ao buscar animes: {e}")
        return ["Erro ao buscar animes."]

    def get_movie_recommendations(self, genero):
        """Busca recomendações de filmes no TMDB."""
        genero_id = self.TMDB_GENRES.get(self.normalizar_genero(genero))
        if not genero_id:
            return ["Gênero inválido. Verifique os gêneros disponíveis."]
        url = "https://api.themoviedb.org/3/discover/movie"
        params = {
            "api_key": self.TMDB_API_KEY,
            "with_genres": genero_id,
            "language": "pt-BR",
            "sort_by": "popularity.desc",
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return [movie["title"] for movie in data["results"][:5]]
            else:
                print(response.status_code, response.text)
        except Exception as e:
            print(f"Erro ao buscar filmes: {e}")
        return ["Erro ao buscar filmes."]

    def get_series_recommendations(self, genero):
        """Busca recomendações de séries no TMDB."""
        genero_id = self.TMDB_GENRES.get(self.normalizar_genero(genero))
        if not genero_id:
            return ["Gênero inválido. Verifique os gêneros disponíveis."]
        url = "https://api.themoviedb.org/3/discover/tv"
        params = {
            "api_key": self.TMDB_API_KEY,
            "with_genres": genero_id,
            "language": "pt-BR",
            "sort_by": "popularity.desc",
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return [serie["name"] for serie in data["results"][:5]]
            else:
                print(response.status_code, response.text)
        except Exception as e:
            print(f"Erro ao buscar séries: {e}")
        return ["Erro ao buscar séries."]

    def get_book_recommendations(self, genero):
        """Busca recomendações de livros no Google Books."""
        url = f"https://www.googleapis.com/books/v1/volumes"
        params = {"q": f"subject:{genero}", "maxResults": 5, "key": self.GOOGLE_BOOKS_API_KEY}
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return [book["volumeInfo"]["title"] for book in data.get("items", [])]
            else:
                print(response.status_code, response.text)
        except Exception as e:
            print(f"Erro ao buscar livros: {e}")
        return ["Erro ao buscar livros."]

    @commands.command(name="recomendar")
    async def recomendar(self, ctx, tipo: str, *, genero: str):
        """Recomenda animes, filmes, séries ou livros com base no gênero fornecido."""
        tipo = tipo.lower()
        genero = self.normalizar_genero(genero)
        recomendacoes = []

        loading_message = await ctx.send("🔍 Buscando recomendações, por favor, aguarde...")

        if tipo == "anime":
            recomendacoes = self.get_anime_recommendations(genero)
        elif tipo == "filme":
            recomendacoes = self.get_movie_recommendations(genero)
        elif tipo == "série":
            recomendacoes = self.get_series_recommendations(genero)
        elif tipo == "livro":
            recomendacoes = self.get_book_recommendations(genero)
        else:
            await ctx.send("Tipo inválido! Use: anime, filme, série ou livro.")
            await loading_message.delete()
            return

        await loading_message.delete()

        if len(recomendacoes) == 1 and "Erro" in recomendacoes[0]:
            await ctx.send(recomendacoes[0])
        else:
            mensagem = f"Recomendações de {tipo.capitalize()} no gênero {genero.capitalize()}:\n" + "\n".join(recomendacoes)
            await ctx.send(mensagem)

async def setup(bot):
    await bot.add_cog(Recomendacao(bot))
