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
