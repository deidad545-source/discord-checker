import os
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread

# Servidor Web para mantener el servicio activo en Railway
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

# Configuración del bot con Slash Commands
class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Sincroniza los comandos '/' con Discord al iniciar
        await self.tree.sync()
        print("✅ Comandos de barra (/) sincronizados exitosamente.")

bot = Client()

@bot.event
async def on_ready():
    print(f"✅ Bot conectado y listo como: {bot.user}")

# Comando Slash: /check
@bot.tree.command(name="check", description="Verifica si un nombre de usuario de Discord está disponible")
@app_commands.describe(username="El usuario que deseas consultar")
async def check(interaction: discord.Interaction, username: str):
    await interaction.response.defer()

    url = "https://discord.com/api/v9/users/@me/pomelo-attempt"
    headers = {"Content-Type": "application/json"}
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
                        await interaction.followup.send(f"🔴 El nick `{username}` **NO** está disponible.")
                    else:
                        await interaction.followup.send(f"🟢 El nick `{username}` **SÍ** está disponible.")
                else:
                    await interaction.followup.send(f"⚠️ No se pudo verificar `{username}` (Código: {resp.status}).")
        except Exception as e:
            await interaction.followup.send(f"❌ Ocurrió un error al consultar: {e}")

if __name__ == "__main__":
    keep_alive()
    TOKEN = os.environ.get("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ Error: No se encontró la variable DISCORD_TOKEN")
