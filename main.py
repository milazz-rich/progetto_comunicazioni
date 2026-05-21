import base64
import os
import tempfile

import cv2
import numpy as np
from dash import Dash, Input, Output, State, dcc, html

from yolo import getPrediction

app = Dash(name="progettoComunicazioni")

WEBCAM = cv2.VideoCapture(0)
VIDEO_CAPTURE = None
VIDEO_PATH = None
VIDEO_KEY = None
VIDEO_FRAME_STEP = 3


def frame_to_data_url(frame):
    ok, buffer = cv2.imencode(".jpg", frame)
    if not ok:
        return ""
    image_b64 = base64.b64encode(buffer).decode("utf-8")
    return f"data:image/jpeg;base64,{image_b64}"


def decode_image_upload(contents):
    _, content_string = contents.split(",", 1)
    image_bytes = base64.b64decode(content_string)
    np_array = np.frombuffer(image_bytes, dtype=np.uint8)
    return cv2.imdecode(np_array, cv2.IMREAD_COLOR)


def prepare_video_capture(contents, filename):
    _, content_string = contents.split(",", 1)
    video_bytes = base64.b64decode(content_string)
    suffix = os.path.splitext(filename or "")[1] or ".mp4"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(video_bytes)
        return temp_file.name


app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "padding": "40px 20px",
        "background": "linear-gradient(130deg, #f4f6fb 0%, #e3ecff 100%)",
        "fontFamily": "Segoe UI, sans-serif",
    },
    children=[
        html.Div(
            style={
                "maxWidth": "900px",
                "margin": "0 auto",
                "background": "rgba(255, 255, 255, 0.9)",
                "borderRadius": "20px",
                "padding": "28px",
                "boxShadow": "0 16px 40px rgba(24, 39, 75, 0.12)",
            },
            children=[
                html.H1(
                    "Rilevamento Persone",
                    style={"marginTop": "0", "color": "#12213f"},
                ),
                dcc.RadioItems(
                    id="mode-switch",
                    options=[
                        {"label": "Live", "value": "live"},
                        {"label": "Video", "value": "video"},
                        {"label": "Immagine", "value": "immagine"},
                    ],
                    value="live",
                    inline=True,
                    style={"marginBottom": "18px"},
                    inputStyle={"marginRight": "8px", "marginLeft": "14px"},
                    labelStyle={"fontWeight": "600", "color": "#203354"},
                ),
                html.Div(id="mode-note", style={"marginBottom": "12px", "color": "#28436f"}),
                dcc.Upload(
                    id="file-upload",
                    children=html.Div("Carica un file (trascina o clicca)"),
                    multiple=False,
                    accept="image/*",
                    style={
                        "padding": "18px",
                        "border": "2px dashed #7f9ad6",
                        "borderRadius": "14px",
                        "background": "#f8fbff",
                        "fontWeight": "600",
                        "color": "#1d355d",
                        "textAlign": "center",
                        "display": "none",
                    },
                ),
                dcc.Interval(id="live-interval", interval=900, n_intervals=0, disabled=False),
                html.Div(
                    style={
                        "marginTop": "24px",
                        "background": "#0f172a",
                        "borderRadius": "14px",
                        "padding": "10px",
                        "textAlign": "center",
                    },
                    children=html.Img(
                        id="result-image",
                        style={
                            "width": "100%",
                            "maxHeight": "560px",
                            "objectFit": "contain",
                            "borderRadius": "10px",
                        },
                    ),
                ),
            ],
        )
    ],
)


@app.callback(
    Output("mode-note", "children"),
    Output("file-upload", "children"),
    Output("file-upload", "accept"),
    Output("file-upload", "style"),
    Output("live-interval", "disabled"),
    Input("mode-switch", "value"),
)
def render_upload(mode):
    upload_style = {
        "padding": "18px",
        "border": "2px dashed #7f9ad6",
        "borderRadius": "14px",
        "background": "#f8fbff",
        "fontWeight": "600",
        "color": "#1d355d",
        "textAlign": "center",
    }

    if mode == "live":
        return "Modalita live attiva: uso webcam locale.", "", "image/*", {
            **upload_style,
            "display": "none",
        }, False

    accept = "video/*" if mode == "video" else "image/*"
    label = "Carica un video" if mode == "video" else "Carica un'immagine"
    interval_disabled = mode != "video"
    return "", html.Div([label, " (trascina o clicca)"]), accept, upload_style, interval_disabled


@app.callback(
    Output("result-image", "src"),
    Input("live-interval", "n_intervals"),
    Input("file-upload", "contents"),
    Input("mode-switch", "value"),
    State("file-upload", "filename"),
)
def update_preview(_, upload_contents, mode, upload_filename):
    global VIDEO_CAPTURE, VIDEO_PATH, VIDEO_KEY
    try:
        if mode == "live":
            ok, frame = WEBCAM.read()
            if not ok:
                return ""
            predicted = getPrediction(frame)
            return frame_to_data_url(predicted)

        if not upload_contents:
            return ""

        if mode == "immagine":
            frame = decode_image_upload(upload_contents)
        else:
            current_key = f"{upload_filename}:{len(upload_contents)}"
            if current_key != VIDEO_KEY:
                if VIDEO_CAPTURE is not None:
                    VIDEO_CAPTURE.release()
                    VIDEO_CAPTURE = None
                if VIDEO_PATH and os.path.exists(VIDEO_PATH):
                    os.remove(VIDEO_PATH)
                VIDEO_PATH = prepare_video_capture(upload_contents, upload_filename)
                VIDEO_CAPTURE = cv2.VideoCapture(VIDEO_PATH)
                VIDEO_KEY = current_key

            if VIDEO_CAPTURE is None:
                return ""

            ok, frame = VIDEO_CAPTURE.read()
            if not ok:
                VIDEO_CAPTURE.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ok, frame = VIDEO_CAPTURE.read()
                if not ok:
                    return ""

            for _ in range(VIDEO_FRAME_STEP - 1):
                ok = VIDEO_CAPTURE.grab()
                if not ok:
                    VIDEO_CAPTURE.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    break

        if frame is None:
            return ""

        predicted = getPrediction(frame)
        return frame_to_data_url(predicted)
    except Exception:
        return ""


if __name__ == "__main__":
    app.run(debug=True)
