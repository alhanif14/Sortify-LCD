from fasthtml.common import *

# Komponen gambar + teks
def step_item(img_src, title, description):
    return Div(
        Div(
            Img(src=img_src, cls="img-fluid rounded-circle"),  # 👉 img bulat
            cls="step-image overflow-hidden rounded-circle d-flex justify-content-center align-items-center shadow"
        ),
        Div(
            P(title, cls="step-title"),  # 👉 teks besar
            P(description, cls="step-desc"),  # 👉 teks kecil
            cls="text-center mt-3"
        ),
        cls="d-flex flex-column align-items-center"
    )

def how_content():
    return Div(
        # Tombol Back
        Div(
            A(
                Span("arrow_back_ios", cls="material-symbols-rounded"),
                P("Back", cls="fw-bold h4 m-0 back-text"),
                href="/",
                cls="back-link",
            ),
            cls="text-start ms-5 mt-2",
        ),
        # Judul
        Div(
            P("How to use Sortify", cls="h1 fw-bold"),
            cls="text-center mb-5",
        ),
        # Steps
        Div(
            step_item("/static/how/step1.png", "DISPOSE", "Throw your waste into the Sortify smart bin."),
            step_item("/static/how/step2.png", "SCAN", "Scan the barcode shown on the machine for claiming points."),
            step_item("/static/how/step3.png", "REDEEM", "Redeem points for exciting rewards in Sortify app."),
            cls="d-flex justify-content-center flex-wrap gap-5 mt-5"
        ),
        Div(
            A("Start!", 
              href="/start",
              hx_get="/start",
              hx_target="#mainContent",
              cls="start-btn m-4 rounded-4 text-decoration-none py-2 px-4 h1"),
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
