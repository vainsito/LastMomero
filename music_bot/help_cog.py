import discord
from discord.ext import commands

class help_cog(commands.Cog): # Cog de ayuda
    def __init__(self, bot):
        self.bot = bot # Guardamos el bot en una variable
        
        
        self.help_embed = discord.Embed(title="Comandos", description="Lista de comandos", color=discord.Color.blue()) # Creamos un embed para mostrar la lista de comandos
        self.help_message = """ 
```
Asi que quieres saber los comandos que tengo, ¿eh? Pues TOMAAAAAAAAA:

/help: Muestra la lista de comandos del papu
/p <nombre de la canción>: Reproduce una canción bien machin
/q : Muestra la cola de canciones B)
/skip: Salta la canción que se está reproduciendo prro
/clear : Limpia la cola de canciones maldita sea
/andate : Desconectas al prro del canal de voz :c
/pause : Pausa la canción que se está reproduciendo verdad que si
/resume : Continua la canción que se está reproduciendo alv

```     
""" # Creamos un string para guardar la lista de comandos

        self.help_embed.add_field(name="Comandos", value=self.help_message, inline=False) # Añadimos el string al embed
        self.text_channel = None # Creamos una variable para guardar el canal de texto donde se mostrará la lista de comandos
    
    @commands.Cog.listener()
    async def on_ready(self): # Evento que se ejecuta cuando el bot está listo
        for guild in self.bot.guilds: # Recorremos todos los servidores donde está el bot
            for channel in guild.text_channels: # Recorremos todos los canales de texto del servidor      # Comprobamos si el bot tiene permisos para enviar mensajes en el canal
                self.text_channel.append(channel) # Añadimos el canal a la lista de canales de texto
        await self.send_to_all(self.help_message) # Enviamos el mensaje a todos los canales de texto
    async def send_to_all(self, message): # Función para enviar un mensaje a todos los canales de texto
        for channel in self.text_channel: # Recorremos todos los canales de texto
            await channel.send(message) # Enviamos el mensaje al canal de texto
    
    @commands.command(name = "help", help = "Muestra la lista de comandos") 
    async def help(self, ctx): # Comando para mostrar la lista de comandos
        await ctx.send(embed=self.help_embed) # Enviamos el embed con la lista de comandos
        await ctx.send(self.help_message) # Enviamos el string con la lista de comandos