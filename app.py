from fasthtml.common import *
from routes.landing import landing_section, landing_routes
from routes.start import start_routes
from routes.how import how_routes
from routes.avail import avail_routes
from routes.success import success_routes
from routes.barcode import barcode_routes
from routes.preload import preload_routes
import uvicorn

app, rt = fast_app(live=True, pico=False)
landing_routes(rt)
start_routes(rt)
how_routes(rt)
avail_routes(rt)
success_routes(rt)
barcode_routes(rt)
preload_routes(rt)

def main_content():
    return Div(
        landing_section(),
          cls="main pt-4",
          id="mainContent",
    )

@rt("/")
def landing():
    return Html(
        Head(
            Title("Sortify"),
            Link(href="/static/css/style.css", rel="stylesheet"),
            Link(href="/static/css/landing.css", rel="stylesheet"),
            Link(href="/static/css/avail.css", rel="stylesheet"),
            Link(href="/static/css/how.css", rel="stylesheet"),
            Link(href="/static/css/start.css", rel="stylesheet"),
            Link(href="/static/css/success.css", rel="stylesheet"),
            Link(href="/static/css/barcode.css", rel="stylesheet"),
            Link(href="/static/css/preload.css", rel="stylesheet"),
            Link(href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Poppins:wght@300;600&display=swap", rel="stylesheet"),
            Link(href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css", rel="stylesheet"),
            Script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"),
            Link(href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded", rel="stylesheet"),
            Script(type="module", src="/static/js/countUp.min.js"),
            Script(type="module", src="/static/js/initCountUp.js"),
            Script(src="/static/js/paho-mqtt.js", defer=True),
            Script(src="/static/js/mqtt.js", defer=True),
            Script("""
 if (!window.Paho || !window.Paho.MQTT) {
      console.error("Paho MQTT belum dimuat");
    } else {
      console.log("Paho MQTT sudah dimuat");
    }
"""),
            Script(type="module", src="/static/js/script.js"),
            Script(src="https://unpkg.com/htmx.org@1.9.12", defer=True),
        ),
        Body(
        main_content(),
        ),
    )

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port="8001")