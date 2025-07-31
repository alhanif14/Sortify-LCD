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
            Div(
                Div(
                    Div(
                        Img(src=f"/static/qr-code/{latest_qr}", alt="Barcode", cls="img-fluid qr-code-large"),
                        cls="border rounded-4 shadow bg-light p-3"
                    ),
                    cls="col-lg-5 col-md-6 text-center"
                ),

                Div(
                    P("Scan to Claim Your Points!", cls="display-5 fw-bold text-center"),
                    P("60s", id="timer", cls="display-1 fw-bolder text-success text-center my-3"),
                    P("Scan with your Sortify web before time runs out.", cls="h5 fw-normal text-center"),

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
                        cls="d-flex justify-content-center pt-4 mt-3"
                    ),
                    cls="col-lg-5 col-md-6"
                ),
                cls="row align-items-center justify-content-center gx-5 mt-5 pt-5"
            ),
            cls="container h-100 d-flex"
        )
    )

def barcode_section():
    return Div(barcode_content())

def barcode_routes(rt):
    @rt("/barcode")
    def barcode():
        time.sleep(2)
        return barcode_section()
