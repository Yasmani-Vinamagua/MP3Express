# Genera dist\MP3Express.exe con FFmpeg e icono incluidos.
# Uso: .\build.ps1 -FFmpegBin "C:\ruta\a\ffmpeg\bin"   (carpeta con ffmpeg.exe y ffprobe.exe)
# Recomendado: build "essentials" de https://www.gyan.dev/ffmpeg/builds/ (~100 MB por exe).
param([Parameter(Mandatory)][string]$FFmpegBin)

python -m pip install -q -r requirements.txt pyinstaller
python -m PyInstaller --noconfirm --onefile --windowed --name MP3Express `
    --icon assets\icono.ico `
    --add-data "assets;assets" `
    --collect-all customtkinter `
    --add-binary "$FFmpegBin\ffmpeg.exe;." --add-binary "$FFmpegBin\ffprobe.exe;." `
    app.py
Write-Host "Listo: dist\MP3Express.exe"
