import os
import asyncio
import json
import aiohttp
import discord
from discord.ext import commands

API_START = "https://friendsofrisk.com/riskmatch.php?startgame"
API_GAME = "https://friendsofrisk.com/riskmatch.php?gameid={game_id}"

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def run_round(session, game_id):
    async with session.get(API_GAME.format(game_id=game_id)) as resp:
        resp.raise_for_status()
        return await resp.json()

async def play_game(thread: discord.Thread, game_id: str):
    async with aiohttp.ClientSession() as session:
        while True:
            data = await run_round(session, game_id)
            playerdata = data.get("playerdata", {})
            round_no = playerdata.get("round", 0)
            actions = data.get("actions", [])
            lines = [a.get("text", "") for a in actions]
            if lines:
                await thread.send(f"**Round {round_no}**\n" + "\n".join(lines))
            state = playerdata.get("state")
            if state == "completed":
                remaining = playerdata.get("players", [])
                winner = remaining[0].get("name") if remaining else "Unknown"
                await thread.send(f"Game over! Winner: {winner}")
                break
            await asyncio.sleep(1)

@bot.command()
async def match(ctx: commands.Context, *members: discord.Member):
    if len(members) < 2 or len(members) > 6:
        await ctx.send("Please mention between 2 and 6 players.")
        return
    names = [m.display_name for m in members]
    async with aiohttp.ClientSession() as session:
        async with session.post(API_START, json=names) as resp:
            resp.raise_for_status()
            data = await resp.json()
    game_id = data.get("gameid")
    if not game_id:
        await ctx.send("Failed to start game.")
        return
    thread = await ctx.message.create_thread(name=f"RiskMatch-{game_id[:8]}")
    await thread.send(f"Starting RiskMatch with {', '.join(names)} (Game ID: {game_id})")
    await play_game(thread, game_id)

if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("DISCORD_TOKEN environment variable not set")
    bot.run(TOKEN)
