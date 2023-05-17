import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

class music_cog(commands.Cog): # Cog de música
    def __init__(self, bot): # Constructor
        self.bot = bot # Guardamos el bot en una variable
        
        self.is_playing = False # Variable que indica si se está reproduciendo una canción
        self.is_paused = False # Variable que indica si la canción está pausada
        
        self.music_queue = [] # Lista que contiene las canciones que se van a reproducir
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'} # Opciones de youtube-dl
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'} # Opciones de ffmpeg

        self.vc = None # Variable que guarda el canal de voz en el que se encuentra el bot
    def search_yt(self, item): # Función que busca una canción en youtube
        with YoutubeDL(self.YDL_OPTIONS) as ydl: # Creamos un objeto de la clase YoutubeDL
            try: # Intentamos obtener la información de la canción
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0] # Obtenemos la información de la canción
            except Exception: # Si no se pudo obtener la información, regresamos False
                return False
            
        return {'source': info['formats'][0]['url'], 'title': info['title']} # Regresamos la información de la canción
    
    def play_next(self): # Función que reproduce la siguiente canción
        if len(self.music_queue) > 0: # Si hay canciones en la cola, reproducimos la siguiente
            self.is_playing = True # Indicamos que se está reproduciendo una canción
            
            m_url = self.music_queue[0][0]['source'] # Obtenemos la url de la siguiente canción
            
            self.music_queue.pop(0) # Eliminamos la canción de la cola
            
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next()) # Reproducimos la canción
        else:
            self.is_playing = False # Indicamos que no se está reproduciendo nada
    async def play_music(self, ctx): # Función que reproduce una canción
        
        if len(self.music_queue) > 0: # Si hay canciones en la cola, reproducimos la primera
            self.is_playing = True # Indicamos que se está reproduciendo una canción
            
            m_url = self.music_queue[0][0]['source'] # Obtenemos la url de la canción
            
            if self.vc == None or not self.vc.is_connected(): # Si el bot no está en un canal de voz, nos conectamos
                self.vc = await self.music_queue[0][1].connect() # Nos conectamos al canal de voz
                
                if self.vc == None: # Si no se pudo conectar, le avisamos al usuario
                    await ctx.send("No puedo conectarme al canal de voz") 
            else:
                await self.vc.move_to(self.music_queue[0][1]) # Si ya está conectado, nos movemos al canal de voz en el que se encuentra el usuario
            
            await ctx.send("Ahora estas escuchando: %s" % self.music_queue[0][0]['title'])  # Le avisamos al usuario que se está reproduciendo la canción
            
            self.music_queue.pop(0) # Eliminamos la canción de la cola
            
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next()) # Reproducimos la canción
        else: 
            self.is_playing = False # Indicamos que no se está reproduciendo nada
    
    @commands.command(name="play", aliases=["p", "pone"],help="Pone una canción de youtube") # Comando que reproduce una canción
    async def p(self, ctx, *args):
        query = " ".join(args)                          # Guardamos la canción que se quiere reproducir en una variable llamada query
        
        voice_channel = ctx.author.voice.channel        # Guardamos el canal de voz en el que se encuentra el usuario que ejecutó el comando
        if voice_channel is None:                       # Si el usuario no está en un canal de voz, le avisamos
            await ctx.send("No estás en un canal de voz papu :v")
        elif self.is_paused:                            # Si la canción está pausada, la reanudamos
            await self.vc.resume()
        else:                                           # Si no está pausada, la reproducimos
            song = self.search_yt(query)                # Buscamos la canción en youtube
            if type(song) == type(True):                # Si no se encontró la canción, le avisamos al usuario
                await ctx.send("No se pudo reproducir la canción prro :,v")  
            else:                                       # Si se encontró la canción, la agregamos a la cola
                await ctx.send("Canción agregada a la cola :v noHomo")
                self.music_queue.append([song, voice_channel]) # Agregamos la canción a la cola
                
                if self.is_playing == False:           # Si no se está reproduciendo nada, reproducimos la canción
                    await self.play_music(ctx)         # Reproducimos la canción
    
    @commands.command(name="pause",help="Pausa la canción B)")  # Comando que pausa la canción que se está reproduciendo
    async def pause(self, ctx, *args):                              
        if self.is_playing:                                     # Si se está reproduciendo una canción, la pausamos
            self.is_playing = False                              # Indicamos que no se está reproduciendo nada
            self.is_paused = True                               # Indicamos que la canción está pausada
            self.vc.pause()                                     # Pausamos la canción
            await ctx.send("Canción pausada con exito prro :v") # Le avisamos al usuario que la canción está pausada
        elif self.is_paused :                                                   # Si la canción ya está pausada, le avisamos al usuario y la reanudamos
            await ctx.send("La cancion ya esta pausada prro :v, la quieres pausar mas?, te la voy a pausar mas :v")
            self.vc.resume()                                                    # Reanudamos la canción
        else:
            await ctx.send("No hay canciones reproduciendose prro :v, no puedo pausar nada :v") # Si no se está reproduciendo nada, le avisamos al usuario
    
    @commands.command(name="resume",aliases=["r"],help="Reanuda la canción B)") # Comando que reanuda la canción que se está reproduciendo
    async def resume(self, ctx, *args):
        if self.is_paused:                                                     # Si la canción está pausada, la reanudamos
            self.is_playing = True                                            # Indicamos que se está reproduciendo una canción
            self.is_paused = False                                          # Indicamos que la canción no está pausada
            self.vc.resume()                                               # Reanudamos la canción

    @commands.command(name="skip", aliases=["s"],help="Skipea la canción :v") # Comando que salta la canción que se está reproduciendo
    async def skip(self, ctx, *args):
         if self.vc != None and self.vc: # Si el bot está en un canal de voz, salta la canción
             self.vc.stop()
             await self.play_music(ctx)
             await ctx.send("Canción skipeada con exito prro :v")   
    
    @commands.command(name="cola", aliases=["q", "c"],help="Muestra la cola de canciones que hay {]:{V")  # Comando que muestra la cola de canciones
    async def queue(self, ctx, *args):
        retval = "" # Variable que guarda la cola de canciones
        
        for i in range(0, len(self.music_queue)): # Recorremos la cola de canciones
            retval += self.music_queue[i][0]['title'] + "\n" # Agregamos la canción a la cola
        
        if retval != "":
            await ctx.send(retval) # Si hay canciones en la cola, las mostramos
        else:
            await ctx.send("No hay canciones en la cola prro :v, deberias agregar mas papu") # Si no hay canciones en la cola, le avisamos al usuario
    
    @commands.command(name="clear", aliases=["cl", "bin"],help="Elimina toda la cola de canciones y para la actual :(") # Comando que elimina la cola de canciones
    async def clear(self, ctx, *args): 
        if self.vc != None and self.is_playing: # Si el bot está en un canal de voz y se está reproduciendo una canción, la paramos
            self.vc.stop() 
        self.music_queue.clear() # Eliminamos la cola de canciones
        await ctx.send("Cola de canciones eliminada con exito prro :v") # Le avisamos al usuario que la cola de canciones fue eliminada
        
    @commands.command(name="leave", aliases=["l", "salir"],help="Saca al bot del canal de voz :v") # Comando que saca al bot del canal de voz
    async def leave(self, ctx, *args):
        self.is_playing = False # Indicamos que no se está reproduciendo nada
        self.is_paused = False # Indicamos que la canción no está pausada
        self.music_queue.clear() # Eliminamos la cola de canciones
        await self.vc.disconnect() # Desconectamos al bot del canal de voz
        await ctx.send("Adios prro :'v") # Le avisamos al usuario que el bot se desconectó del canal de voz