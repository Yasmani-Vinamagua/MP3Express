<p align="center"><img src="assets/logo-color.png" alt="MP3Express" width="320"></p>

# 🎧 MP3Express

**Descarga y convierte audio de YouTube a MP3 de manera sencilla.**

MP3Express es una aplicación de escritorio para Windows desarrollada con **Python y CustomTkinter**, que permite convertir videos y listas de reproducción de YouTube a archivos MP3 mediante una interfaz intuitiva.

Sin comandos complicados. Solo pega el enlace, selecciona la calidad y descarga.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-5B3FD6)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Incluido-F59E0B)

**[📥 Descargar para Windows](https://github.com/Yasmani-Vinamagua/MP3Express/releases/latest)** · **[🐛 Reportar un problema](https://github.com/Yasmani-Vinamagua/MP3Express/issues)**

---

## 🎬 Mira MP3Express en acción

[![Demostración de MP3Express](assets/brag.jpg)](assets/brag.mp4)

Una demostración rápida de cómo descargar audio en MP3.

*Música de Sascha Ende, ende.app (CC BY 4.0).*

## ✨ Características

- **Descargas individuales y múltiples:** procesa varios enlaces en una misma operación.
- **Listas de reproducción:** descarga el audio de playlists de YouTube.
- **Importación de enlaces:** carga archivos `.txt` con múltiples URLs.
- **Calidad configurable:** selecciona entre 128, 192 y 320 kbps.
- **Progreso individual:** visualiza el estado de cada descarga.
- **Cancelación:** detén el proceso cuando lo necesites.
- **Carpeta personalizada:** elige dónde guardar tus archivos.
- **Tema automático:** interfaz clara u oscura según Windows.
- **Ejecutable independiente:** FFmpeg está incluido en la versión `.exe`.

## 🚀 Cómo utilizarlo

1. Descarga y abre **MP3Express.exe**.
2. Pega uno o varios enlaces de YouTube.
3. Selecciona la calidad del audio.
4. Escoge la carpeta de destino.
5. Haz clic en **Descargar**.

Por defecto, los archivos se guardan en `YouTube_MP3` dentro de tu carpeta de usuario.

## 💻 Instalación desde el código

### Requisitos

- Windows
- Python 3.9 o superior
- FFmpeg

### 1. Clonar el repositorio

```bash
git clone https://github.com/Yasmani-Vinamagua/MP3Express.git
cd MP3Express
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Instalar FFmpeg

```powershell
winget install Gyan.FFmpeg
```

### 4. Ejecutar la aplicación

```bash
python app.py
```

## 🛠️ Tecnologías utilizadas

| Tecnología | Función |
|---|---|
| Python | Lógica y desarrollo de la aplicación |
| CustomTkinter | Interfaz gráfica |
| yt-dlp | Obtención y descarga del contenido |
| FFmpeg | Extracción y conversión de audio |
| PyInstaller | Generación del ejecutable Windows |

## 📦 Compilar el ejecutable

Para generar `MP3Express.exe`, necesitas `ffmpeg.exe` y `ffprobe.exe`.

```powershell
.\build.ps1 -FFmpegBin "C:\ruta\a\ffmpeg\bin"
```

El archivo generado estará disponible en:

`dist\MP3Express.exe`

## 🤝 Contribuciones

¿Tienes una sugerencia o encontraste un error?

Puedes abrir un [Issue](https://github.com/Yasmani-Vinamagua/MP3Express/issues) para reportarlo o proponer una mejora.

## ⚖️ Uso responsable

MP3Express está destinado al uso personal y educativo con contenido propio o para el que tengas autorización.

Respeta los derechos de autor y los términos de servicio de las plataformas.

---

Desarrollado por [Yasmani Vinamagua](https://github.com/Yasmani-Vinamagua).
