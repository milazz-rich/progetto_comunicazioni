import cv2
from ultralytics import YOLO

CONFIDANCE = 0.5

def getPrediction(frame):
  model = YOLO("yolo26n.pt")
  results = model.predict(
      source=frame,
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
      return frame_annotato