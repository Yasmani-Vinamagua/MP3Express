"""MP3Express - interfaz gráfica. Ejecutar: python app.py

Identidad: ver .yas/brand/ (paleta Violeta + Ámbar, icono y logo en assets/).
"""
import os
import queue
import sys
import threading
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

import core

# --- Identidad (paleta aprobada en .yas/brand/paleta/paleta.md) -----------------------
VIOLETA, VIOLETA_PROFUNDO = "#5B3FD6", "#4527B8"
AMBAR, GRAFITO, NIEBLA, BLANCO = "#F59E0B", "#1F2328", "#F4F5F3", "#FFFFFF"
GRIS = "#5F6368"
# Extensión para modo oscuro (no están en la paleta: derivados con contraste calculado ≥ 4,5:1)
SUPERFICIE_OSCURA = "#2B3038"          # tarjetas sobre Grafito
GRIS_CLARO = "#A9AFB6"                 # texto secundario en oscuro (6,0:1)
EXITO = ("#1E7B34", "#86D19A")         # claro 5,33:1 sobre blanco · oscuro 7,33:1
ERROR = ("#C62828", "#FF8A8A")         # claro 5,62:1 sobre blanco · oscuro 5,85:1
AVISO = (GRAFITO, AMBAR)               # ámbar nunca como texto sobre claro (2,15:1)
MUTED = (GRIS, GRIS_CLARO)
TEXTO = (GRAFITO, NIEBLA)
FUENTE = "Segoe UI"                    # fuente del sistema (ver tipografia/sistema-tipografico.md)

ctk.set_appearance_mode("system")


def recurso(rel):
    """Ruta de un archivo de assets, tanto en desarrollo como dentro del .exe."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    return str(base / rel)


def boton_secundario(master, **kw):
    return ctk.CTkButton(master, fg_color="transparent", border_width=1, border_color=(VIOLETA, AMBAR),
                         text_color=(VIOLETA, AMBAR), hover_color=(NIEBLA, SUPERFICIE_OSCURA),
                         font=ctk.CTkFont(FUENTE, 13), **kw)


class Fila(ctk.CTkFrame):
    """Una canción en la cola: título, estado y barra de progreso."""

    def __init__(self, master, titulo):
        super().__init__(master, fg_color=(BLANCO, SUPERFICIE_OSCURA), corner_radius=12)
        self.columnconfigure(0, weight=1)
        self.lbl = ctk.CTkLabel(self, text=titulo, anchor="w", text_color=TEXTO, font=ctk.CTkFont(FUENTE, 13, "bold"))
        self.lbl.grid(row=0, column=0, sticky="ew", padx=12, pady=(8, 0))
        self.estado = ctk.CTkLabel(self, text="En espera", anchor="e", text_color=MUTED, font=ctk.CTkFont(FUENTE, 12))
        self.estado.grid(row=0, column=1, padx=12, pady=(8, 0))
        self.barra = ctk.CTkProgressBar(self, progress_color=(VIOLETA, AMBAR), fg_color=("#E3E4E1", "#3A4048"), height=8)
        self.barra.set(0)
        self.barra.grid(row=1, column=0, columnspan=2, sticky="ew", padx=12, pady=(4, 10))

    def actualizar(self, pct, texto, color=None):
        self.barra.set(pct / 100)
        self.estado.configure(text=texto, **({"text_color": color} if color else {}))


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=(NIEBLA, GRAFITO))
        self.title("MP3Express")
        self.geometry("680x720")
        self.minsize(580, 600)
        # CTk restablece el icono tras crear la ventana: se aplica con un pequeño retardo
        self.after(250, self._icono)
        self.carpeta = core.CARPETA_POR_DEFECTO
        self.eventos = queue.Queue()
        self.cancelar = threading.Event()
        self.trabajando = False
        self._filas = {}

        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        # Cabecera: logo (imagotipo horizontal) en claro / oscuro
        try:
            from PIL import Image
            logo = ctk.CTkImage(light_image=Image.open(recurso("assets/logo-color.png")),
                                dark_image=Image.open(recurso("assets/logo-oscuro.png")), size=(204, 34))
            ctk.CTkLabel(self, text="", image=logo).grid(row=0, column=0, sticky="w", padx=24, pady=(20, 0))
        except Exception:  # sin el logo la app sigue funcionando
            ctk.CTkLabel(self, text="MP3Express", font=ctk.CTkFont(FUENTE, 24, "bold"), text_color=TEXTO
                         ).grid(row=0, column=0, sticky="w", padx=24, pady=(20, 0))
        ctk.CTkLabel(self, text="Pega uno o varios links de YouTube y descarga el audio en MP3.",
                     text_color=MUTED, font=ctk.CTkFont(FUENTE, 14)).grid(row=1, column=0, sticky="w", padx=24, pady=(6, 0))

        # Entrada de links
        caja = ctk.CTkFrame(self, fg_color="transparent")
        caja.grid(row=2, column=0, sticky="ew", padx=24, pady=14)
        caja.columnconfigure(0, weight=1)
        self.texto = ctk.CTkTextbox(caja, height=96, fg_color=(BLANCO, SUPERFICIE_OSCURA), text_color=TEXTO,
                                    border_width=1, border_color=("#CFD1CC", "#3A4048"), corner_radius=12,
                                    font=ctk.CTkFont(FUENTE, 14))
        self.texto.grid(row=0, column=0, columnspan=3, sticky="ew")
        # Texto de ayuda dentro del campo (CTkTextbox no trae placeholder): se oculta al escribir o pegar
        self.ayuda = ctk.CTkLabel(self.texto, anchor="nw", justify="left", text_color=MUTED, font=ctk.CTkFont(FUENTE, 13),
                                  text="Pega aquí tus links de YouTube, uno por línea.\n"
                                       "Ejemplo: https://www.youtube.com/watch?v=… (también sirven listas de reproducción)")
        self.ayuda.place(x=10, y=6)
        self.ayuda.bind("<Button-1>", lambda e: self.texto.focus_set())
        self.texto.bind("<KeyRelease>", lambda e: self._actualizar_ayuda())
        self.texto.bind("<<Paste>>", lambda e: self.after(10, self._actualizar_ayuda))
        self.texto.bind("<<Cut>>", lambda e: self.after(10, self._actualizar_ayuda))
        boton_secundario(caja, text="Pegar del portapapeles", width=170, command=self.pegar
                         ).grid(row=1, column=0, sticky="w", pady=(10, 0))
        boton_secundario(caja, text="Cargar .txt", width=100, command=self.cargar_txt
                         ).grid(row=1, column=1, padx=8, pady=(10, 0))
        self.btn_ir = ctk.CTkButton(caja, text="Descargar", width=140, height=36, command=self.iniciar,
                                    fg_color=VIOLETA, hover_color=VIOLETA_PROFUNDO, text_color=BLANCO,
                                    font=ctk.CTkFont(FUENTE, 14, "bold"))
        self.btn_ir.grid(row=1, column=2, pady=(10, 0))

        # Cola
        self.cola = ctk.CTkScrollableFrame(self, label_text="Descargas", label_anchor="w",
                                           label_fg_color="transparent", label_text_color=TEXTO,
                                           label_font=ctk.CTkFont(FUENTE, 14, "bold"), fg_color="transparent")
        self.cola.grid(row=3, column=0, sticky="nsew", padx=24)
        self.cola.columnconfigure(0, weight=1)
        self.vacio = ctk.CTkLabel(self.cola, text="Aquí aparecerán tus descargas.", text_color=MUTED,
                                  font=ctk.CTkFont(FUENTE, 13))
        self.vacio.grid(row=0, column=0, pady=30)

        # Opciones
        op = ctk.CTkFrame(self, fg_color="transparent")
        op.grid(row=4, column=0, sticky="ew", padx=24, pady=(12, 4))
        op.columnconfigure(2, weight=1)
        ctk.CTkLabel(op, text="Calidad:", text_color=TEXTO, font=ctk.CTkFont(FUENTE, 13)).grid(row=0, column=0)
        self.calidad = ctk.CTkOptionMenu(op, values=list(core.CALIDADES), width=170, fg_color=VIOLETA,
                                         button_color=VIOLETA_PROFUNDO, button_hover_color=VIOLETA_PROFUNDO,
                                         text_color=BLANCO, font=ctk.CTkFont(FUENTE, 13))
        self.calidad.set("Alta (192 kbps)")
        self.calidad.grid(row=0, column=1, sticky="w", padx=8)
        self.lbl_carpeta = ctk.CTkLabel(op, text="", anchor="e", text_color=MUTED, font=ctk.CTkFont(FUENTE, 12))
        self.lbl_carpeta.grid(row=0, column=2, padx=8, sticky="e")
        boton_secundario(op, text="Cambiar carpeta", width=120, command=self.elegir_carpeta).grid(row=0, column=3)
        boton_secundario(op, text="Abrir carpeta", width=110, command=self.abrir_carpeta).grid(row=0, column=4, padx=(8, 0))
        self._refrescar_carpeta()

        self.estado = ctk.CTkLabel(self, text="Pega tus links, uno por línea, y pulsa Descargar.", anchor="w",
                                   text_color=MUTED, wraplength=620, justify="left", font=ctk.CTkFont(FUENTE, 13))
        self.estado.grid(row=5, column=0, sticky="ew", padx=24, pady=(0, 4))
        ctk.CTkLabel(self, text="Úsalo solo con contenido propio o con permiso; respeta los derechos de autor.",
                     text_color=MUTED, font=ctk.CTkFont(FUENTE, 11)).grid(row=6, column=0, padx=24, pady=(0, 14), sticky="w")

        if not core.buscar_ffmpeg():
            self.estado.configure(
                text="⚠️ No se encontró FFmpeg. Instálalo con: winget install Gyan.FFmpeg y reabre la app.",
                text_color=AVISO)
        self.after(100, self._procesar_eventos)

    # ---- utilidades de interfaz
    def _icono(self):
        try:
            self.iconbitmap(recurso("assets/icono.ico"))
        except Exception:
            pass  # sin icono la app sigue funcionando

    def _refrescar_carpeta(self):
        p = self.carpeta
        txt = str(p)
        self.lbl_carpeta.configure(text=txt if len(txt) <= 20 else f"…\\{p.parent.name}\\{p.name}")

    def _actualizar_ayuda(self):
        """Muestra el texto de ayuda solo si el campo está vacío."""
        if self.texto.get("1.0", "end").strip():
            self.ayuda.place_forget()
        else:
            self.ayuda.place(x=10, y=6)

    def pegar(self):
        try:
            self.texto.insert("end", self.clipboard_get().strip() + "\n")
        except Exception:
            self.estado.configure(text="El portapapeles está vacío.", text_color=MUTED)
        self._actualizar_ayuda()

    def cargar_txt(self):
        ruta = filedialog.askopenfilename(filetypes=[("Texto", "*.txt")])
        if ruta:
            self.texto.insert("end", Path(ruta).read_text(encoding="utf-8", errors="ignore") + "\n")
            self._actualizar_ayuda()

    def elegir_carpeta(self):
        ruta = filedialog.askdirectory(initialdir=self.carpeta)
        if ruta:
            self.carpeta = Path(ruta)
            self._refrescar_carpeta()

    def abrir_carpeta(self):
        self.carpeta.mkdir(parents=True, exist_ok=True)
        os.startfile(self.carpeta)

    # ---- flujo de descarga
    def iniciar(self):
        if self.trabajando:  # el botón actúa como "Cancelar"
            self.cancelar.set()
            self.estado.configure(text="Cancelando…", text_color=MUTED)
            return
        links = core.extraer_links(self.texto.get("1.0", "end"))
        if not links:
            self.estado.configure(text="No encontré links de YouTube. Pega al menos uno.", text_color=AVISO)
            return
        if not core.buscar_ffmpeg():
            messagebox.showerror("Falta FFmpeg", "Instala FFmpeg con:\n\nwinget install Gyan.FFmpeg\n\ny reabre la app.")
            return
        self.vacio.grid_remove()
        self.cancelar.clear()
        self.trabajando = True
        # Bloqueado mientras se leen los links; se habilita como "Cancelar" al empezar la primera descarga
        self.btn_ir.configure(text="Preparando…", state="disabled")
        self.estado.configure(text="Leyendo links…", text_color=MUTED)
        threading.Thread(target=self._trabajo, args=(links, self.calidad_actual()), daemon=True).start()

    def calidad_actual(self):
        return core.CALIDADES[self.calidad.get()]

    def _trabajo(self, links, calidad):
        """Hilo de fondo: se comunica con la interfaz solo mediante la cola de eventos."""
        ok = err = 0
        for url in links:
            if self.cancelar.is_set():
                break
            try:
                titulo, videos = core.info_url(url)
            except Exception as e:
                err += 1
                self.eventos.put(("error_url", url, core.traducir_error(e)))
                continue
            if len(videos) > 1:
                self.eventos.put(("estado", f"Lista «{titulo}»: {len(videos)} videos."))
            for vurl, vtitulo in videos:
                if self.cancelar.is_set():
                    break
                fila_id = object()
                self.eventos.put(("nueva", fila_id, vtitulo))
                try:
                    core.descargar(vurl, self.carpeta, calidad,
                                   progreso=lambda p, t, f=fila_id: self.eventos.put(("prog", f, p, t)),
                                   cancelar=self.cancelar.is_set)
                    ok += 1
                    self.eventos.put(("fin", fila_id, True, "✅ Listo"))
                except core.Cancelado:
                    self.eventos.put(("fin", fila_id, False, "Cancelado"))
                except Exception as e:
                    err += 1
                    self.eventos.put(("fin", fila_id, False, "❌ " + core.traducir_error(e)))
        self.eventos.put(("terminado", ok, err))

    def _procesar_eventos(self):
        filas = self._filas
        try:
            while True:
                ev = self.eventos.get_nowait()
                tipo = ev[0]
                if tipo == "nueva":
                    f = Fila(self.cola, ev[2])
                    f.grid(sticky="ew", pady=4, padx=2)
                    filas[ev[1]] = f
                    self.btn_ir.configure(text="Cancelar", state="normal", fg_color=ERROR[0], hover_color="#A82020")
                elif tipo == "prog":
                    filas[ev[1]].actualizar(ev[2], ev[3])
                elif tipo == "fin":
                    filas[ev[1]].actualizar(100 if ev[2] else 0, ev[3], EXITO if ev[2] else ERROR)
                elif tipo == "error_url":
                    f = Fila(self.cola, ev[1][:60])
                    f.grid(sticky="ew", pady=4, padx=2)
                    f.actualizar(0, "❌ " + ev[2], ERROR)
                elif tipo == "estado":
                    self.estado.configure(text=ev[1], text_color=MUTED)
                elif tipo == "terminado":
                    self.trabajando = False
                    self.btn_ir.configure(text="Descargar", state="normal", fg_color=VIOLETA, hover_color=VIOLETA_PROFUNDO)
                    resumen = f"Terminado: {ev[1]} descargada(s)" + (f", {ev[2]} con error." if ev[2] else ".")
                    self.estado.configure(text=resumen, text_color=EXITO if not ev[2] else AVISO)
        except queue.Empty:
            pass
        self.after(100, self._procesar_eventos)


def autotest(salida):
    """Comprobación sin ventana: `MP3Express.exe --selftest resultado.txt`."""
    import tempfile
    try:
        with tempfile.TemporaryDirectory() as tmp:
            titulo = core.descargar("https://www.youtube.com/watch?v=jNQXAC9IVRw", tmp)
            mp3 = list(Path(tmp).glob("*.mp3"))
            res = (f"OK ffmpeg={core.buscar_ffmpeg()} titulo={titulo} mp3={[(m.name, m.stat().st_size) for m in mp3]} "
                   f"icono={Path(recurso('assets/icono.ico')).exists()} logo={Path(recurso('assets/logo-color.png')).exists()}")
    except Exception as e:
        res = f"FALLO {e!r}"
    Path(salida).write_text(res, encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--selftest":
        autotest(sys.argv[2])
    else:
        App().mainloop()
