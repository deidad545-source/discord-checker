import os
import discord
from discord.ext import commands

# Configuración de permisos
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Bot conectado y listo como: {bot.user}")


@bot.command()
async def check(ctx, username: str):
    """Revisa si un nombre de usuario existe en Discord."""
    try:
        user = await bot.fetch_user_by_username(username)
        if user:
            await ctx.send(f"❌ El nick **{username}** YA ESTÁ OCUPADO.")
    except discord.NotFound:
        await ctx.send(f"✅ El nick **{username}** PARECE ESTAR LIBRE.")
    except discord.HTTPException:
        await ctx.send(
            "⚠️ Hubo un error de conexión con Discord. Intenta de nuevo."
        )


TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
