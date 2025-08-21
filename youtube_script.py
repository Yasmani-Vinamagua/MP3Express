import os
import sys
from pathlib import Path
import yt_dlp


class Documentos:
    """Clase para crear carpeta de descarga y leer lista de links de YouTube."""

    def __init__(self):

        self.download_folder = Path.home() / "YouTube_MP3" #Crea la carpeta de descarga
        self.links_file = Path.home() / "YouTube_MP3" / "youtube_links.txt" #Crea el archivo de links
    
    def crear_carpeta_descarga(self):
        """Crea la carpeta de descarga si no existe."""
        if not self.download_folder.exists():
            self.download_folder.mkdir(parents=True)
            print(f"Carpeta creada en: {self.download_folder}")
        else:
            print(f"La carpeta ya existe en: {self.download_folder}")
        return self.download_folder
    
    def crear_archivo_links(self):
        """Crea el archivo de links si no existe."""
        if not self.links_file.exists():
            with open(self.links_file, 'w') as f:
                f.write("# Lista de URLs de YouTube para descargar \n# Las líneas que empiecen con # son comentarios y se ignoran \n# Líneas vacías se ignoran también \n# Una URL por línea.\n")
            print(f"Archivo de links creado en: {self.links_file}")
        else:
            print(f"El archivo de links ya existe en: {self.links_file}")
        return self.links_file
        

class ConvertirDescargar:
    """Clase para convertir y descargar videos de YouTube a mp3."""

    def leer_links(self, archivo_links):
        """Lee los links del archivo y devuelve una lista de URLs."""
        links = []

        try:

            with open(archivo_links, 'r') as archivo:
                # Enumerar las líneas del archivo
                for numero_linea, linea in enumerate(archivo, start=1):
                    linea = linea.strip() # Elimina espacios al inicio y al final

                    # Ignorar líneas que son comentarios o están vacías
                    if linea and not linea.startswith('#'):
                        if 'youtube.com' in linea or 'youtu.be' in linea:
                            links.append(linea)
                            print(f"✓ Línea {numero_linea}: URL agregada")
                        else:
                            print(f"⚠️  Línea {numero_linea}: No es una URL de YouTube válida - {linea[:50]}...")
            print(f"\n📋 Se encontraron {len(links)} URLs válidas en el archivo")
            return links
        except FileNotFoundError:
            print(f"❌ Error: El archivo {archivo_links} no existe.")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error al leer el archivo {archivo_links}: {e}")
            sys.exit(1)
    def convertir_videos(self, link, carpeta_descarga):
        """Convierte un video de YouTube a mp3 y lo guarda en la carpeta de descarga."""
        
        opciones_ydl = {
            'format': 'bestaudio/best', # Mejor calidad de audio
            'extractaudio': True, # Extrae solo el audio
            'audioformat': 'mp3', # Formato de audio a mp3
            'outtmpl': f'{carpeta_descarga}/%(title)s.%(ext)s', # Nombre del archivo de salida
            'noplaylist': False, # No descargar listas de reproducción
            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
             }],
            'ffmpeg_location': r'C:/ffmpeg/bin/ffmpeg.exe', # Ruta al ejecutable de ffmpeg
        }

        try:
            with yt_dlp.YoutubeDL(opciones_ydl) as ydl:
                # Obtener información del video
                info = ydl.extract_info(link, download=False)
                titulo = info.get('title', 'Desconocido')
                duracion = info.get('duration', 0)
                
                print(f"📹 Título: {titulo}")
                print(f"⏱️  Duración: {duracion//60}:{duracion%60:02d}")
                print("🔄 Iniciando descarga...")
                
                # Descargar y convertir
                ydl.download([link])
                
                print(f"✅ Descarga completada: {titulo}.mp3")
                print(f"📁 Guardado en: {carpeta_descarga}")
            
        except Exception as e:
            print(f"❌ Error durante la descarga: {str(e)}")
            return False
    
        return True

    def descargar_videos(self, links, carpeta_descarga):
        """Descarga los videos de YouTube y los convierte a mp3."""
        
        if not links:
            print("❌ No se encontraron URLs válidas para descargar.")
            return
        
        print(f"🎵 Iniciando descarga de {len(links)} videos...")

        for i, link in enumerate(links, start=1):
            print(f"Descargando video {i}/{len(links)}: {link}")
            if self.convertir_videos(link, carpeta_descarga):
                print(f"✓ Video {i} descargado y convertido a mp3")
            else:
                print(f"❌ Error al descargar el video {i}: {links}")


print("🎵 Descargador de Audio de YouTube a MP3")
print("=" * 40)
documentos = Documentos()
carpeta_descarga = documentos.crear_carpeta_descarga()
archivo_links = documentos.crear_archivo_links()
convertir_descargar = ConvertirDescargar()
links = convertir_descargar.leer_links(archivo_links)
convertir_descargar.descargar_videos(links, carpeta_descarga)
print("🎉 Proceso completado.")
