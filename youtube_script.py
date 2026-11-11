"""Versión de consola de MP3Express (lee youtube_links.txt). Para la interfaz gráfica usa app.py."""
from pathlib import Path

import core


def main():
    print("🎵 MP3Express - YouTube a MP3")
    print("=" * 40)
    carpeta = core.CARPETA_POR_DEFECTO
    carpeta.mkdir(parents=True, exist_ok=True)
    archivo = carpeta / "youtube_links.txt"
    if not archivo.exists():
        archivo.write_text(
            "# Pega aquí las URLs de YouTube, una por línea.\n# Las líneas que empiezan con # se ignoran.\n",
            encoding="utf-8",
        )
        print(f"Se creó {archivo}. Agrega tus links y vuelve a ejecutar.")
        return

    links = core.extraer_links(archivo.read_text(encoding="utf-8"))
    if not links:
        print(f"No hay URLs válidas en {archivo}.")
        return
    if not core.buscar_ffmpeg():
        print("❌ No se encontró FFmpeg. Instálalo (winget install Gyan.FFmpeg) y reintenta.")
        return

    errores = 0
    for i, url in enumerate(links, 1):
        print(f"[{i}/{len(links)}] {url}")
        try:
            titulo, videos = core.info_url(url)
            for vurl, vtitulo in videos:
                core.descargar(vurl, carpeta, progreso=lambda p, t: print(f"\r   {t}   ", end=""))
                print(f"\n✅ {vtitulo}")
        except Exception as e:
            errores += 1
            print(f"❌ {core.traducir_error(e)} ({url})")
    print(f"🎉 Terminado. Carpeta: {carpeta}" + (f" · {errores} con error" if errores else ""))


if __name__ == "__main__":
    main()
