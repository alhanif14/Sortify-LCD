from fasthtml.common import *
from fastcore.xtras import NotStr
from routes.mqtt_client import get_last_mqtt_result, reset_last_mqtt_result

def preload_content():
    return Div(
        P("Sortify is sorting", cls="h1 text-center text-success my-5 fw-bold pb-5"),
        Div(
            NotStr('''
<svg class="animated-logo" width="374" height="370" viewBox="0 0 374 370" xmlns="http://www.w3.org/2000/svg">
    <path class="animated-path path-1" d="M338.234 0V66.252H163.887C138.316 66.252 84.3841 80.1998 73.2259 135.991C62.0676 191.782 98.7968 231.301 118.556 244.086H45.3303C32.5448 240.599 0.000103159 195.269 0 135.991C-0.000121364 66.252 62.765 0 132.504 0H338.234Z" fill="#19400F"/>
    
    <path class="animated-path path-2" d="M34.869 369.616V303.364H209.217C234.787 303.364 288.719 289.417 299.877 233.625C311.035 177.834 274.306 138.316 254.547 125.53H327.773C340.558 129.017 373.103 174.347 373.103 233.625C373.103 303.364 310.338 369.616 240.599 369.616H34.869Z" fill="#A1CF9B"/>
    
    <path class="animated-path path-3" d="M134.601 120.151L166.519 152.07V120.151H134.601Z" fill="#4F6A18"/>
    <path class="animated-path path-3" d="M187.798 120.151V174.235L207.304 194.627V126.357L187.798 120.151Z" fill="#4F6A18"/>
    <path class="animated-path path-3" d="M229.469 215.02V141.43C244.364 153.488 251.044 173.053 252.521 181.328V238.072L229.469 215.02Z" fill="#4F6A18"/>
    <path class="animated-path path-3" d="M122.188 134.337L154.106 166.256L122.188 166.256V134.337Z" fill="#4F6A18"/>
    <path class="animated-path path-3" d="M122.188 187.534L176.272 187.534L196.664 207.04H128.394L122.188 187.534Z" fill="#4F6A18"/>
    <path class="animated-path path-3" d="M217.056 229.206H143.467C155.525 244.101 175.089 250.78 183.365 252.258H240.108L217.056 229.206Z" fill="#4F6A18"/>
</svg>
            '''),
            cls="text-center py-3"
        ),
        P("Please wait a moment...", cls="text-center h3 text-muted mt-5 pt-5"),
        Div(
            "",
            id="mqtt-poll",
            hx_get="/mqtt/result",
            hx_trigger="every 2s",
            hx_target="#mqtt-poll",
            hx_swap="outerHTML"
        ),
        cls="container preload-page"
    )

def preload_section():
    return Div(preload_content())

def preload_routes(rt):
    @rt("/preload")
    def preload():
        return preload_section()

    @rt("/mqtt/result")
    def mqtt_result():
        # Cek entri terbaru dari tabel waste_detection_log
        cur.execute("SELECT waste_type FROM waste_detection_log ORDER BY timestamp DESC LIMIT 1")
        row = cur.fetchone()
        
        if row:
            latest_result = row[0]
            print(f"🧪 Result from DB: {latest_result}")
            if any(w in latest_result for w in ("plastic", "paper", "organic", "other")):
                return Div(
                    Script('htmx.trigger(document.body, "go-success")')
                )
        
        return Div("Waiting for result...", cls="text-center text-muted small")


