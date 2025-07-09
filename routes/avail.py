from fasthtml.common import *

# Function to create progress bar box
def progress_box(id_num, label, color_class, icon_name, value):
    return Div(
        Div(
            Div(  # progress-wrapper
                Div(  # progress-container
                    Span(icon_name, cls="material-symbols-rounded icon-inside-trash"),
                    Div(id=f"{id_num}-fill", cls=f"progress-fill " + color_class),
                    cls="progress-container position-relative"
                ),
                Div(id=f"{id_num}-number", cls="countup-number mt-3 fw-bold mb-2", **{"data-value": value}),
                cls="progress-wrapper"
            ),
            P(label, cls="progress-label mt-2"),
            cls="progress-content text-center"
        ),
        cls="progress-box shadow p-3 rounded-4 bg-white d-flex flex-column align-items-center mt-4"
    )


# Main content
def avail_content():
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
            P("Trash Availibility", cls="h1 fw-bold"),
            cls="text-center mb-5",
        ),
        Div(
            Div(
                progress_box("count1", "Organic", "bg-success", "compost", 100),
                progress_box("count2", "Plactic", "bg-primary", "recycling", 60),
                progress_box("count3", "Paper", "bg-info", "description", 45),
                progress_box("count4", "Others", "bg-warning", "category", 30),
                cls="d-flex justify-content-center flex-wrap gap-4"
            ),
            cls="container text-center",
        ),
        cls="avail-page-content",
    )

# Full page
def avail_section():
    return Div(avail_content())

# Route
def avail_routes(rt):
    @rt("/avail")
    def avail():
        return avail_section()
