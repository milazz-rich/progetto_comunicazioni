from yolo import getPrediction
from dash import Dash, html

app = Dash(name = "progettoComunicazioni")

app.layout = html.Div(children = ["Hello World!"])  

if __name__ == "__main__":
    app.run(debug = True)

