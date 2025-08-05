from fasthtml.common import *

def step_item(img_src, title, description):
    return Div(
        Div(
            Img(src=img_src, cls="img-fluid rounded-circle"),
            cls="step-image overflow-hidden rounded-circle d-flex justify-content-center align-items-center shadow"
        ),
        Div(
            P(title, cls="step-title"),
            P(description, cls="step-desc"),
            cls="text-center mt-3"
        ),
        cls="d-flex flex-column align-items-center"
    )

def how_content():
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
            P("How to use Sortify", cls="h1 fw-bold"),
            cls="text-center mb-5",
        ),
        Div(
            step_item("/static/how/step1.png", "DISPOSE", "Throw your waste into the Sortify smart bin."),
            step_item("/static/how/step2.png", "SCAN", "Scan the barcode shown on the machine for claiming points."),
            step_item("/static/how/step3.png", "REDEEM", "Redeem points for exciting rewards in Sortify app."),
            cls="d-flex justify-content-center flex-wrap gap-5 mt-5"
        ),
        Div(
            A("Start!", 
              href="/preload",
              hx_get="/preload",
              hx_target="#mainContent",
              cls="start-btn m-4 mt-0 rounded-4 text-decoration-none py-1 px-3 h2"),
              cls="d-flex justify-content-end"
        ),
        cls="how-page-content container"
    )

def how_section():
    return Div(how_content())

def how_routes(rt):
    @rt("/how")
    def how():
        return how_section()
