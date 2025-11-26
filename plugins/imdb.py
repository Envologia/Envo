# Envo Userbot - IMDb Plugin (Async)
# Created by @envologia

import asyncio
from imdb import IMDb
from telethon import events

ia = IMDb()

def search_imdb(query):
    """Synchronous IMDb search function."""
    movies = ia.search_movie(query)
    if not movies:
        return None

    movie = ia.get_movie(movies[0].movieID)
    title = movie.get('title')
    year = movie.get('year')
    rating = movie.get('rating')
    plot = movie.get('plot outline')

    return f"**{title} ({year})**\n\n**Rating:** {rating}\n\n**Plot:** {plot}"

def register(envo):
    @envo.on(events.NewMessage(pattern=r"\.imdb\s+(.*)", outgoing=True))
    async def imdb(event):
        query = event.pattern_match.group(1)
        loop = asyncio.get_running_loop()
        try:
            # Run the synchronous function in a separate thread
            response = await loop.run_in_executor(None, search_imdb, query)
            if response:
                await event.edit(response)
            else:
                await event.edit(f"No results found for '{query}'.")
        except Exception as e:
            await event.edit(f"An error occurred: {e}")
