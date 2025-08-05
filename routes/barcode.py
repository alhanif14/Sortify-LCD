from fasthtml.common import *
from database.database import get_db_session
from database.models import WasteDetectionLog
from fastapi.responses import Response
import os
import time

def get_latest_qr_data():
    folder_path = os.path.join(os.path.dirname(__file__), "../static/qr-code")
    folder_path = os.path.abspath(folder_path)
    time.sleep(0.5)
    try:
        files = [f for f in os.listdir(folder_path) if f.endswith(".png")]
        files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
        if not files:
            return "barcode-placeholder.png", None
        
        latest_file = files[0]
        dispose_id = os.path.splitext(latest_file)[0]
        return latest_file, dispose_id
    except (FileNotFoundError, IndexError):
        return "barcode-placeholder.png", None

def barcode_content():
    latest_qr_filename, dispose_id = get_latest_qr_data()

    if not dispose_id:
        return Div(P("Error: Could not generate a valid QR Code. Please try again."), cls="text-center")

    return Div(
        Div(
            Div(
                Div(
                    Img(
                        src=f"/static/qr-code/{latest_qr_filename}",
                        alt="Barcode",
                        cls="img-fluid qr-code-large"
                    ),
                    cls="border rounded-4 shadow bg-light p-3"
                ),
                cls="col-lg-5 col-md-6 text-center"
            ),
            Div(
                P("Scan to Claim Your Points!", cls="display-5 fw-bold text-center"),
                P("60s", id="timer", cls="display-1 fw-bolder text-success text-center my-3"),
                P("Scan with your Sortify web before time runs out.", cls="h5 fw-normal text-center"),
                Div(
                    A(
                        "Extend Timer",
                        href="#",
                        onclick="resetTimer()",
                        cls="how-btn rounded-4 px-4 py-2 me-3 h3 text-decoration-none"
                    ),
                    A(
                        "Done",
                        href="/",
                        cls="start-btn rounded-4 px-4 py-2 h3 text-decoration-none"
                    ),
                    cls="d-flex justify-content-center pt-4 mt-3"
                ),
                cls="col-lg-5 col-md-6"
            ),
            cls="row align-items-center justify-content-center gx-5 mt-5 pt-5"
        ),
        hx_get=f"/check-qr-status/{dispose_id}",
        hx_trigger="every 2s",
        hx_swap="none",
        cls="container h-100 d-flex align-items-center"
    )

def barcode_section():
    return Div(barcode_content())

def barcode_routes(rt):
    @rt("/barcode")
    def barcode():
        time.sleep(2)
        return barcode_section()
    
    @rt("/check-qr-status/{dispose_id_str}")
    def check_qr_status(dispose_id_str: str):
        numeric_id = None
        try:
            numeric_id = int(dispose_id_str.split('_')[-1])
        except (ValueError, IndexError):
            return Response(status_code=200)

        if numeric_id is None:
            return Response(status_code=200)

        db = get_db_session()
        try:
            log_entry = db.query(WasteDetectionLog).filter(WasteDetectionLog.id == numeric_id).first()
            if log_entry and log_entry.username:
                print(f"QR {numeric_id} claimed. Redirecting LCD to home.")
                return Response(
                    status_code=200,
                    headers={"HX-Trigger": "qr-claimed"}
                )
        finally:
            db.close()
        
        return Response(status_code=200)
