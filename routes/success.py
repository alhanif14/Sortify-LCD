from fasthtml.common import *
from routes.mqtt_qr_handler import mqtt_publish
from routes.preload import preload_section
from routes.barcode import barcode_section

def success_content():
    return Div(
        # Title
        Div(
            P("Your waste has been successfully disposed!", cls="h1 fw-bold title-text"),
            cls="text-center my-5 pb-5"
        ),
        # Animasi Ceklis di Tengah
        Div(
            Span("check_circle", cls="material-symbols-rounded text-success animate-check"),
            cls="d-flex justify-content-center align-items-center my-5 py-5"
        ),
        # Dua Tombol di Bawah
        Div(
            A(
                "Scan Another One",
                hx_post="/mqtt/insert",
                hx_target="#mainContent",
                hx_swap="innerHTML",
                cls="how-btn rounded-4 px-4 py-2 me-3 h2 text-decoration-none"
            ),
            A(
                "Finish",
                hx_post="/mqtt/stop",
                hx_target="#mainContent",
                hx_swap="innerHTML",
                cls="start-btn rounded-4 px-4 py-2 h2 text-decoration-none"
            ),
            cls="d-flex justify-content-center pt-5 mt-5"
        ),
        cls="success-page-content container"
    )

def success_section():
    return Div(success_content())

def success_routes(rt):
    @rt("/success")
    def success():
        return success_section()
    @rt("/mqtt/insert", methods=["POST"])
    def mqtt_insert():
        mqtt_publish("waste/raw", "insert again")
        return preload_section()

    @rt("/mqtt/stop", methods=["POST"])
    def mqtt_stop():
        mqtt_publish("waste/raw", "stop")
        return barcode_section()
