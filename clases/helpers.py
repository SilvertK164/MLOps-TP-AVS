"""Utilidades de las clases interactivas: verificación de ejercicios y rutas.

Las celdas de verificación nunca cortan el notebook: si el ejercicio todavía no está
resuelto, muestran una pista y siguen. Así podés ejecutar todo de corrido y volver a los
ejercicios cuando quieras.
"""

import sys
from pathlib import Path

from IPython.display import Markdown, display

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "clases" / "_salidas"  # todo lo que generan las clases (ignorado por git)
OUT.mkdir(exist_ok=True)

# Hace importable el paquete del TP aunque no se haya instalado con `pip install -e .`
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))


def check(name: str, ok: bool, hint: str) -> bool:
    """Muestra ✅ si ``ok`` es verdadero; si no, ⏳ con una pista."""
    if ok:
        display(Markdown(f"✅ **{name}**: ¡correcto!"))
    else:
        display(Markdown(f"⏳ **{name}**: todavía no. *Pista:* {hint}"))
    return ok


def safe_check(name: str, fn, hint: str) -> bool:
    """Como :func:`check`, pero evalúa ``fn()`` y trata cualquier error como no resuelto."""
    try:
        ok = bool(fn())
    except Exception as e:  # noqa: BLE001 - el ejercicio puede fallar de cualquier forma
        ok = False
        hint = f"{hint} (error: `{type(e).__name__}: {e}`)"
    return check(name, ok, hint)


def quiz(question: str, options: list[str], answer: int, explanation: str):
    """Pregunta de opción múltiple con botones (ipywidgets)."""
    import ipywidgets as widgets

    buttons = widgets.ToggleButtons(options=options, value=None, style={"button_width": "auto"})
    out = widgets.Output()

    def on_change(change):
        out.clear_output()
        with out:
            if change["new"] == options[answer]:
                display(Markdown(f"✅ ¡Bien! {explanation}"))
            else:
                display(Markdown("❌ No es esa. Pensalo de nuevo."))

    buttons.observe(on_change, names="value")
    display(Markdown(f"**{question}**"), buttons, out)


def _html(texto: str) -> str:
    """Markdown en línea mínimo (`código` y **negrita**) a HTML, para los widgets."""
    import html
    import re

    texto = html.escape(texto, quote=False)
    texto = re.sub(r"`([^`]+)`", r"<code>\1</code>", texto)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", texto)


def _plano(texto: str) -> str:
    """Saca las marcas de markdown (las opciones de los RadioButtons son texto plano)."""
    return texto.replace("`", "").replace("**", "")


def _banco():
    import banco  # clases/banco.py: está en el mismo directorio que este archivo

    return banco


def tarjetas(clave: str | list[str]):
    """Tarjetas de repaso: frente → «Mostrar» → dorso; marcá cuáles sabías y cuáles repasar.

    ``clave`` es una clase (``"C3"``) o una lista de clases (``["C1", "C2"]``).
    """
    import random

    import ipywidgets as widgets

    banco = _banco()
    claves = [clave] if isinstance(clave, str) else list(clave)
    mazo = [(k, f, d) for k in claves for f, d in banco.TARJETAS[k]]
    estado = {"i": 0, "repasar": set(), "sabidas": set()}

    frente = widgets.HTML()
    dorso = widgets.Output()
    progreso = widgets.HTML()
    b_mostrar = widgets.Button(description="Mostrar respuesta", icon="eye")
    b_sabia = widgets.Button(description="La sabía", button_style="success", icon="check")
    b_repasar = widgets.Button(description="A repasar", button_style="warning", icon="refresh")
    b_mezclar = widgets.Button(description="Mezclar", icon="random")
    final = widgets.Output()

    def dibujar():
        dorso.clear_output()
        i = estado["i"]
        if i >= len(mazo):
            frente.value = "<h4>🎉 ¡Terminaste el mazo!</h4>"
            progreso.value = ""
            final.clear_output()
            with final:
                pendientes = [mazo[j][1] for j in sorted(estado["repasar"])]
                display(Markdown(
                    f"Sabías **{len(estado['sabidas'])} de {len(mazo)}**."
                    + ("\n\nPara repasar:\n" + "\n".join(f"- {p}" for p in pendientes) if pendientes else
                       " ¡Todas! 💪")
                    + "\n\nApretá **Mezclar** para empezar otra vuelta."
                ))
            return
        k, f, _ = mazo[i]
        frente.value = f"<div style='font-size:1.15em;padding:.6em 0'><b>{_html(f)}</b></div>"
        progreso.value = f"<small>Tarjeta {i + 1} de {len(mazo)} · {banco.NOMBRES[k]}</small>"

    def mostrar(_):
        if estado["i"] < len(mazo):
            dorso.clear_output()
            with dorso:
                display(Markdown(mazo[estado["i"]][2]))

    def marcar(conjunto):
        def _f(_):
            if estado["i"] < len(mazo):
                estado[conjunto].add(estado["i"])
                estado["i"] += 1
                dibujar()
        return _f

    def mezclar(_):
        random.shuffle(mazo)
        estado.update(i=0, repasar=set(), sabidas=set())
        final.clear_output()
        dibujar()

    b_mostrar.on_click(mostrar)
    b_sabia.on_click(marcar("sabidas"))
    b_repasar.on_click(marcar("repasar"))
    b_mezclar.on_click(mezclar)
    dibujar()
    display(widgets.VBox([progreso, frente, dorso, widgets.HBox([b_mostrar, b_sabia, b_repasar, b_mezclar]),
                          final]))


def cuestionario(
    clave: str | list[str], n: int | None = None, mezclar: bool = False, semilla: int | None = None
):
    """Cuestionario con puntaje: respondé todas y apretá «Corregir».

    ``clave`` es una clase o una lista de clases. Con ``n`` se toman solo ``n`` preguntas
    (al azar si ``mezclar=True``).
    """
    import random

    import ipywidgets as widgets

    banco = _banco()
    claves = [clave] if isinstance(clave, str) else list(clave)
    preguntas = [(k, *p) for k in claves for p in banco.PREGUNTAS[k]]
    if mezclar:
        random.Random(semilla).shuffle(preguntas)
    preguntas = preguntas[:n] if n else preguntas

    filas, radios, salidas = [], [], []
    for num, (k, texto, opciones, _, _) in enumerate(preguntas, 1):
        radio = widgets.RadioButtons(
            options=[_plano(o) for o in opciones], value=None, layout=widgets.Layout(width="auto")
        )
        salida = widgets.Output()
        origen = f" <small style='opacity:.6'>({banco.NOMBRES[k]})</small>" if len(claves) > 1 else ""
        filas += [widgets.HTML(f"<b>{num}. {_html(texto)}</b>{origen}"), radio, salida]
        radios.append(radio)
        salidas.append(salida)

    corregir = widgets.Button(description="Corregir", button_style="primary", icon="check-square")
    reiniciar = widgets.Button(description="Empezar de nuevo", icon="undo")
    resultado = widgets.Output()

    def on_corregir(_):
        aciertos = 0
        for pregunta, radio, salida in zip(preguntas, radios, salidas, strict=True):
            _, _, opciones, correcta, explicacion = pregunta
            salida.clear_output()
            with salida:
                if radio.value is None:
                    display(Markdown("⚪ *Sin responder.*"))
                elif radio.value == _plano(opciones[correcta]):
                    aciertos += 1
                    display(Markdown(f"✅ {explicacion}"))
                else:
                    display(Markdown(f"❌ La correcta es **{opciones[correcta]}**. {explicacion}"))
        nota = aciertos / len(preguntas)
        mensaje = ("🏆 ¡Excelente, dominás el tema!" if nota >= 0.9 else
                   "👍 Bien. Repasá las que fallaste." if nota >= 0.6 else
                   "📚 Conviene volver a leer la teoría y las tarjetas.")
        resultado.clear_output()
        with resultado:
            display(Markdown(f"### Puntaje: {aciertos} / {len(preguntas)} ({nota:.0%})\n{mensaje}"))

    def on_reiniciar(_):
        for radio, salida in zip(radios, salidas, strict=True):
            radio.value = None
            salida.clear_output()
        resultado.clear_output()

    corregir.on_click(on_corregir)
    reiniciar.on_click(on_reiniciar)
    display(widgets.VBox([*filas, widgets.HBox([corregir, reiniciar]), resultado]))
