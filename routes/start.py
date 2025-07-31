from fasthtml.common import *
from routes.mqtt_qr_handler import mqtt_publish
from routes.preload import preload_section

def start_content(post_url: str = "/mqtt/start"):
    return Div(
        Div(
            A(
                Span("arrow_back_ios", cls="material-symbols-rounded"),
                P("Back", cls="fw-bold h4 m-0 back-text"),
                href="/",
                cls="back-link",
            ),
            cls="text-start ms-5 mt-2",
        ),
        Div(
            P("Place waste into the box", cls="h1 fw-bold title-text"),
            cls="text-center mb-4",
        ),
        Div(
            Img(src="/static/how/step1.png", alt="Start Image", cls="img-fluid rounded-4 glow-img"),
            cls="text-center pb-4 pt-3",
        ),
        Div(
            P(
                "Insert your waste properly into the provided box to ensure correct sorting.",
                cls="h4 fw-normal text-center px-3 mt-5"
            ),
            cls="mb-5"
        ),
        Div(
            A(
                "Start",
                hx_post=post_url,
                hx_target="#mainContent",
                hx_swap="innerHTML",
                cls="start-btn m-4 mt-0 rounded-4 text-decoration-none py-1 px-4 h2"
            ),
            cls="d-flex justify-content-center"
        ),
        cls="start-page-content container"
    )

def start_section():
    return Div(start_content())

def start_routes(rt):
    @rt("/start")
    def start():
        return start_section()

    @rt("/mqtt/start", methods=["POST"])
    def mqtt_start():
        mqtt_publish("waste/raw", "start")
        return preload_section()