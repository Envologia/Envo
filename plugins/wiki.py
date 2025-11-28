# Envo Userbot - Wikipedia Plugin (Async)
# Created by @envologia

import asyncio
import wikipedia
from telethon import events

def search_wikipedia(query):
    """Synchronous Wikipedia search function."""
    try:
        summary = wikipedia.summary(query, sentences=3)
        return f"**{query.title()}**\n\n{summary}"
    except wikipedia.exceptions.PageError:
        return f"Could not find a Wikipedia page for '{query}'."
    except wikipedia.exceptions.DisambiguationError as e:
        return f"'{query}' is ambiguous. Options: {e.options[:5]}"
    except Exception as e:
        return f"An error occurred: {e}"

def register(envo):
    @envo.on(events.NewMessage(pattern=r"\.wiki\s+(.*)", outgoing=True))
    async def wiki(event):
        query = event.pattern_match.group(1)
        loop = asyncio.get_running_loop()
        # Run the synchronous function in a separate thread
        response = await loop.run_in_executor(None, search_wikipedia, query)
        await event.edit(response)
