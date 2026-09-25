import os
import aiohttp
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# Servidor Web para mantener el servicio activo
app = Flask('')

@app.route('/')
def home():
    return "Bot activo 24/7"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

# Configuración del bot de Discord
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado y listo como: {bot.user}")

@bot.command(name="check")
async def check_username(ctx, username: str = None):
    if not username:
        await ctx.send("❌ Por favor especifica un nombre. Ejemplo: `!check usuario`")
        return

    # Usamos la API pública de Discord para validar disponibilidad de pomelo/username
    url = "https://discord.com/api/v9/users/@me/pomelo-attempt"
    headers = {
        "Content-Type": "application/json"
    }
    # Si la variable DISCORD_TOKEN está definida se envía en el header
    token = os.environ.get("DISCORD_TOKEN")
    if token:
        headers["Authorization"] = token

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json={"username": username}, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    taken = data.get("taken", False)
                    if taken:
                        await ctx.send(f"🔴 El nick `{username}` **NO** está disponible.")
                    else:
                        await ctx.send(f"🟢 El nick `{username}` **SÍ** está disponible.")
                else:
                    await ctx.send(f"⚠️ No se pudo verificar `{username}` (Código de respuesta: {resp.status}).")
        except Exception as e:
            await ctx.send(f"❌ Ocurrió un error al consultar la API: {e}")

if __name__ == "__main__":
    keep_alive()
    TOKEN = os.environ.get("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ Error: No se encontró la variable DISCORD_TOKEN")
