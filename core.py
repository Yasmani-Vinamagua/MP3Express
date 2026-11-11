"""Lógica de MP3Express: sin interfaz, reutilizable por la GUI y la consola."""
import re
import shutil
import sys
from pathlib import Path

import yt_dlp

CARPETA_POR_DEFECTO = Path.home() / "YouTube_MP3"
CALIDADES = {"Estándar (128 kbps)": "128", "Alta (192 kbps)": "192", "Máxima (320 kbps)": "320"}
_PATRON_URL = re.compile(r"https?://(?:www\.|m\.|music\.)?(?:youtube\.com|youtu\.be)/\S+", re.I)


class Cancelado(Exception):
    pass


def buscar_ffmpeg():
    """Devuelve la ruta de ffmpeg (junto al programa, en el PATH o en C:/ffmpeg) o None."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    for candidato in (base / "ffmpeg" / "bin" / "ffmpeg.exe", base / "ffmpeg.exe", Path("C:/ffmpeg/bin/ffmpeg.exe")):
        if candidato.exists():
            return str(candidato)
    return shutil.which("ffmpeg")


def extraer_links(texto):
    """Saca todas las URLs de YouTube de un texto (acepta comentarios con # y líneas sueltas)."""
    vistos, links = set(), []
    for linea in texto.splitlines():
        if linea.strip().startswith("#"):
            continue
        for url in _PATRON_URL.findall(linea):
            if url not in vistos:
                vistos.add(url)
                links.append(url)
    return links


def es_lista(url):
    return "list=" in url and "watch?v=" not in url or "/playlist" in url


def traducir_error(e):
    """Convierte errores técnicos en mensajes comprensibles."""
    t = str(e).lower()
    if "private" in t:
        return "El video es privado."
    if "unavailable" in t or "not available" in t:
        return "El video no está disponible (borrado o bloqueado en tu país)."
    if "sign in" in t or "age" in t:
        return "El video requiere iniciar sesión o verificar la edad."
    if "ffmpeg" in t or "ffprobe" in t:
        return "No se encontró FFmpeg. Instálalo y vuelve a intentar."
    if "urlopen" in t or "network" in t or "getaddrinfo" in t or "timed out" in t:
        return "Sin conexión a internet."
    if "copyright" in t:
        return "El video está bloqueado por derechos de autor."
    return "No se pudo descargar. Prueba actualizando yt-dlp (pip install -U yt-dlp)."


def info_url(url):
    """Devuelve (titulo, [(url, titulo), ...]) sin descargar. Para listas devuelve cada video."""
    opts = {"quiet": True, "no_warnings": True, "extract_flat": "in_playlist", "skip_download": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    if info.get("_type") == "playlist":
        items = []
        for e in info.get("entries") or []:
            if e and e.get("id"):
                items.append((f"https://www.youtube.com/watch?v={e['id']}", e.get("title") or e["id"]))
        return info.get("title") or "Lista", items
    return info.get("title") or url, [(url, info.get("title") or url)]


def descargar(url, carpeta, calidad="192", progreso=None, cancelar=None):
    """Descarga un video como MP3. `progreso(porcentaje, texto)`; `cancelar()` -> True para abortar.

    Devuelve el título. Lanza Cancelado o Exception (usa traducir_error para mostrarla).
    """
    def hook(d):
        if cancelar and cancelar():
            raise Cancelado()
        if progreso and d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            pct = d.get("downloaded_bytes", 0) / total * 100 if total else 0
            progreso(min(pct, 99), f"Descargando… {pct:.0f}%")
        elif progreso and d["status"] == "finished":
            progreso(99, "Convirtiendo a MP3…")

    opts = {
        "format": "bestaudio/best",
        "outtmpl": str(Path(carpeta) / "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "noprogress": True,
        "no_warnings": True,
        "progress_hooks": [hook],
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": calidad}],
    }
    ffmpeg = buscar_ffmpeg()
    if ffmpeg:
        opts["ffmpeg_location"] = ffmpeg
    Path(carpeta).mkdir(parents=True, exist_ok=True)
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
    if progreso:
        progreso(100, "Listo")
    return info.get("title", "")
