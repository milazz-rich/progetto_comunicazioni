import cv2
from ultralytics import YOLO

CONFIDANCE = 0.5
YOUTUBE_URL = "https://youtu.be/YzcawvDGe4Y?si=XZj0cIKXfSYj9KeT"

model = YOLO("yolo26n.pt")

results = model.predict(
    source=YOUTUBE_URL,
    conf=CONFIDANCE,
    classes=[0],
    verbose=False,
    stream=True
)

for frame_index, result in enumerate(results):
    numero_persone = len(result.boxes)
    frame_annotato = result.plot()
    testo = f"Persone rilevate: {numero_persone}"
    x, y = 30, 50
    font = cv2.FONT_HERSHEY_SIMPLEX
    scala = 1.2
    spessore = 3
    (text_width, text_height), baseline = cv2.getTextSize(
        testo,
        font,
        scala,
        spessore
    )
    cv2.rectangle(
        frame_annotato,
        (x - 10, y - text_height - 10),
        (x + text_width + 10, y + baseline + 10),
        (255, 255, 255),
        -1
    )
    cv2.putText(
        frame_annotato,
        testo,
        (x, y),
        font,
        scala,
        (0, 0, 0),
        spessore,
        cv2.LINE_AA
    )
    cv2.imshow("YOLO - Conteggio persone", frame_annotato)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cv2.destroyAllWindows()