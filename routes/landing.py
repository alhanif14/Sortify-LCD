from fasthtml.common import *

def landing_title():
    return Div(
        Div(
            Img(src="static/landing/daur.png", alt="Daur", cls="landing-img-left"),
            Div(
                P("The future is cleaner"),
                Div(
                    P("when habits"),
                    P("are greener.", cls="tilted-text text-white rounded-4 px-3 pb-1 ms-4"),
                    cls="d-flex justify-content-center position-relative"
                ),
                cls="landing-text fw-bold text-center position-relative"
            ),
            Img(src="static/landing/sampah.png", alt="Sampah", cls="landing-img-right"),
            cls="d-flex justify-content-center align-items-center position-relative"
        ),
        cls="landing-title mt-5"
    )

def landing_button():
    return Div(
        Div(
            A("How?", 
              href="/how",
              hx_get="/how",
              hx_target="#mainContent",
              cls="how-btn m-4 rounded-4 text-decoration-none py-2 px-4 h1"),
            A("Start!", 
              href="/start",
              hx_get="/start",
              hx_target="#mainContent",
              cls="start-btn m-4 rounded-4 text-decoration-none py-2 px-4 h1"),
            A("Availibility", 
              href="/avail",
              hx_get="/avail",
              hx_target="#mainContent",
              cls="avail-btn m-4 rounded-4 text-decoration-none py-2 px-4 h1"),
            cls="d-flex justify-content-center"
        ),
        cls="mt-5"
    )

def landing_content():
    return Div(
        Div(
            Img(src="static/logo/logo-dark.png", alt="logo", cls="logo"),
            cls="text-center my-5"
        ),
        landing_title(),
        landing_button(),
        cls="container"
    )

def landing_section():
    return landing_content()

def landing_routes(rt):
    @rt("/landing")
    def landing():
        return landing_section()