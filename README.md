<p align="center"><img src="assets/logo-color.png" alt="MP3Express" width="320"></p>

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-incluido%20en%20el%20.exe-orange)](https://ffmpeg.org/)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Yasmani-Vinamagua/MP3Express)

**MP3Express** descarga el audio de videos de **YouTube** y lo convierte a **MP3**, con una interfaz gráfica simple.

## 🚀 Características

- 🖱️ Ventana simple: pega links, pulsa **Descargar**. El campo trae un texto de ayuda con un ejemplo.
- 📋 Varios links a la vez, listas de reproducción y carga desde un `.txt`.
- 📊 Barra de progreso por canción, botón **Cancelar** y mensajes de error claros.
- 🎚️ Calidad a elegir (128 / 192 / 320 kbps; por defecto 192) y carpeta de destino configurable.
- 🌗 Tema claro u oscuro según el de Windows.
- 📦 Ejecutable `.exe` con FFmpeg incluido: no hace falta instalar nada más.
- 🔧 Uso personal y educativo. Respeta los derechos de autor y los términos de YouTube.

## 📥 Instalación

### Opción A: ejecutable (Windows)

Descarga `MP3Express.exe` desde [Releases](https://github.com/Yasmani-Vinamagua/MP3Express/releases/latest) y ábrelo. Trae FFmpeg dentro (~110 MB): no necesitas instalar nada más.

### Opción B: desde el código

1. Instala [Python](https://www.python.org/downloads/) y **FFmpeg**:
   ```bash
   winget install Gyan.FFmpeg
   ```
   (Alternativa manual: copia FFmpeg a `C:\ffmpeg\bin\ffmpeg.exe`.)
2. Clona el repositorio e instala las dependencias:
   ```bash
   git clone https://github.com/Yasmani-Vinamagua/MP3Express.git
   cd MP3Express
   pip install -r requirements.txt
   ```

## 🧪 Uso

```bash
python app.py
```

1. Pega uno o varios links de YouTube (o pulsa **Pegar del portapapeles** / **Cargar .txt**).
2. Elige calidad y carpeta (por defecto `C:\Users\<tu_usuario>\YouTube_MP3`).
3. Pulsa **Descargar**. Puedes cancelar en cualquier momento.

### Modo consola (opcional)

`python youtube_script.py` lee los links de `YouTube_MP3\youtube_links.txt`.

## 🛠️ Compilar el .exe

Necesitas una carpeta con `ffmpeg.exe` y `ffprobe.exe`. Se recomienda el build *essentials* de [gyan.dev](https://www.gyan.dev/ffmpeg/builds/), que deja el `.exe` en ~110 MB (el build *full* lo lleva a ~210 MB).

```powershell
.\build.ps1 -FFmpegBin "C:\ruta\a\ffmpeg\bin"
```

El resultado queda en `dist\MP3Express.exe`.

## 🗺️ Próximos pasos

- Elegir qué videos descargar de una lista y metadatos/portada en el MP3.
