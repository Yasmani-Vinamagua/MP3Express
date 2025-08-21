# 🎵 MP3Express  

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue)](https://www.python.org/) 
[![FFmpeg](https://img.shields.io/badge/FFmpeg-required-orange)](https://ffmpeg.org/)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Yasmani-Vinamagua/MP3Express)

**MP3Express** es una herramienta en Python que permite descargar y convertir videos de **YouTube** a **MP3** de forma rápida y sencilla.


---

## 🚀 Características

- 🎵 Descarga y conversión de videos de YouTube a MP3.  
- 📋 Manejo automático de múltiples enlaces desde un archivo de texto.  
- 💻 Compatible con Windows y configuraciones personalizables.  
- 🔧 Recomendado para uso personal y educativo.  

---

## 📥 Instalación Básica

1. Descarga **FFmpeg** desde: https://ffmpeg.org/download.html o directamente https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-7.0.2-essentials_build.zip
2. Extrae el contenido
3. Cambia el nombre de la carpeta a "**`ffmpeg`**"
4. Pega la carpeta en tu disco local, por ejemplo: `C:\ffmpeg`
5. Descarga el archivo **`mp3express.exe`** desde la sección de Releases.

---

## 🧪 Uso

1. Ejecuta el archivo **`mp3express.exe`** (esto creará la carpeta y archivo necesario para funcionar la primera vez).
2. Se creará una carpeta de nombre **`YouTube_MP3`** por ejemplo: `C:\Users\nombre_usuario\YouTube_MP3`
3. Dentro de la carpeta existirá un archivo de nombre **`youtube_links.txt`**
4. En el archivo, ingresar los links de los videos (en caso de ser una lista de reporduccion, colocar unicamente el link de la lista).
5. Ejecuta nuevamente el archivo **`mp3express.exe`**
   
**Nota:** Antes de ejecutar el archivo **`mp3express.exe`** por segunda vez, asegurese de que la lista de links en **`youtube_links.txt`** es la correcta.

---
## 🛠️ Instalación Avanzada

1. Clona el repositorio:

```bash
git clone https://github.com/Yasmani-Vinamagua/MP3Express.git
cd MP3Express
```
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```
3. Puedes modificar la ruta de descarga editando la variable en el script principal:
```python
class Documentos:
  def __init__(self):
    self.download_folder = Path.home() / "YouTube_MP3" #Crea la carpeta de descarga
    self.links_file = Path.home() / "YouTube_MP3" / "youtube_links.txt" #Crea el archivo de links
```
4. Descarga **FFmpeg** desde: https://ffmpeg.org/download.html o directamente https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-7.0.2-essentials_build.zip
5. En el script se define la ruta al ejecutable de FFmpeg en la función `convertir_videos`:
```python
'ffmpeg_location': r'C:/ffmpeg/bin/ffmpeg.exe', # Ruta al ejecutable de ffmpeg
```

