import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands

# Servidor web para mantener el bot activo gratis en Render
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot activo")

def run_web_server():
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()

# Configuración del bot de Discord
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
        await ctx.send("⚠️ Hubo un error de conexión con Discord. Intenta de nuevo.")

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
