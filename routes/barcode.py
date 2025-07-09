from fasthtml.common import *
import os
import time

def get_latest_qr_code_filename():
    folder_path = os.path.join(os.path.dirname(__file__), "../static/qr-code")
    folder_path = os.path.abspath(folder_path)

    time.sleep(0.5)
    try:
        files = [f for f in os.listdir(folder_path) if f.endswith(".png")]
        files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
        return files[0] if files else "barcode-placeholder.png"
    except FileNotFoundError:
        return "barcode-placeholder.png"

def barcode_content():
    latest_qr = get_latest_qr_code_filename()
    return Div(
        Div(
            P("Scan the barcode to claim your points!", cls="h1 fw-bold"),
            cls="text-center mb-4"
        ),
        Div(
            Div(
                Img(src=f"/static/qr-code/{latest_qr}", alt="Barcode", cls="img-fluid qr-code-image"),
                cls="border rounded-4 shadow text-center bg-light"
            ),
            cls="d-flex justify-content-center mb-4"
        ),
        Div(
            P("60s", id="timer", cls="display-4 fw-bold text-center text-success"),
            cls="mb-4"
        ),
        Div(
            P("Scan the barcode using your Sortify app to claim your points and redeem exciting rewards.", 
              cls="h4 text-center mb-4"),
        ),
        Div(
            P("Hurry up! Don't let the time run out or your points will be lost!", 
              cls="h5 text-center text-success mb-3"),
        ),
        Div(
            A("Extend Timer",
              href="#",
              onclick="resetTimer()",
              cls="how-btn rounded-4 px-4 py-2 me-3 h3 text-decoration-none"),
            A("Done",
              href="/",
              hx_get="/",
              hx_target="#mainContent",
              cls="start-btn rounded-4 px-4 py-2 h3 text-decoration-none"),
            cls="d-flex justify-content-center pt-4 mt-4"
        ),
        cls="barcode-page-content container"
    )

def barcode_section():
    return Div(barcode_content())

def barcode_routes(rt):
    @rt("/barcode")
    def barcode():
        time.sleep(2)
        return barcode_section()
