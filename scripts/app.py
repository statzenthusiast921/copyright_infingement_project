import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash_canvas import DashCanvas
import os
import base64
import numpy as np
from PIL import Image, ImageDraw
from io import BytesIO
from skimage.metrics import structural_similarity as ssim
import json

# App setup
app = dash.Dash(__name__)
server = app.server

# Logo image options
LOGO_FOLDER = "assets/logos"
TEAM_OPTIONS = [
    {"label": "Washington Nationals", "value": "washington_nationals.png"},
    {"label": "7-11", "value": "seven_eleven.png"},
    {"label": "Target", "value": "target.png"},
    {"label": "Walgreens", "value": "walgreens.png"},
    {"label": "McDonalds", "value": "mcdonalds.png"},
    {"label": "Spotify", "value": "spotify.png"},
    {"label": "BMW", "value": "bmw.png"},
    {"label": "Facebook", "value": "facebook.png"}
]

# Canvas size
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400

# Layout
app.layout = html.Div([
    html.H1("Copyright", style={'textAlign': 'center'}),

    html.Div([
        # Drawing Panel
        html.Div([
            html.Label("Choose Color:"),
            dcc.Dropdown(
                id='color-dropdown',
                options=[
                    {'label': 'Black', 'value': 'black'},
                    {'label': 'Red', 'value': 'red'},
                    {'label': 'Blue', 'value': 'blue'},
                    {'label': 'Green', 'value': 'green'},
                    {'label': 'Yellow', 'value': 'yellow'},
                    {'label': 'White (Eraser)', 'value': 'white'}
                ],
                value='black',
                clearable=False
            ),
            html.Br(),
            html.Label("Brush Size:"),
            dcc.Slider(
                id='brush-size-slider',
                min=1,
                max=20,
                step=1,
                value=3,
                marks={i: str(i) for i in range(1, 21, 2)}
            ),
            html.Br(),
            DashCanvas(
                id='drawing-canvas',
                width=CANVAS_WIDTH,
                height=CANVAS_HEIGHT,
                lineColor='black',
                lineWidth=3,
                hide_buttons=['zoom', 'pan', 'reset']
            ),
        ], style={'flex': '1', 'padding': '20px'}),

        # Logo Panel
        html.Div([
            html.Label("Select a Logo:"),
            dcc.Dropdown(
                id='team-logo-dropdown',
                options=TEAM_OPTIONS,
                value='washington_nationals.png',
                clearable=False
            ),
            html.Br(),
            html.Img(id='team-logo-img', style={
                'width': f"{CANVAS_WIDTH}px",
                'height': f"{CANVAS_HEIGHT}px",
                'border': '1px solid black'
            }),
            html.Br(),
            html.Button("Compare Images", id='compare-button', n_clicks=0),
            html.Div(id='comparison-result', style={'marginTop': '20px', 'fontWeight': 'bold'})
        ], style={'flex': '1', 'padding': '20px'})
    ], style={'display': 'flex'})
])

# Callbacks
@app.callback(
    Output('drawing-canvas', 'lineColor'),
    Input('color-dropdown', 'value')
)
def update_color(color):
    return color

@app.callback(
    Output('drawing-canvas', 'lineWidth'),
    Input('brush-size-slider', 'value')
)
def update_brush_size(size):
    return size

@app.callback(
    Output('team-logo-img', 'src'),
    Input('team-logo-dropdown', 'value')
)
def update_logo_image(filename):
    if filename:
        return f"/assets/logos/{filename}"
    return ""

# Helper to convert canvas JSON to image
def parse_json_to_image(json_data, width, height):
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    if json_data and 'objects' in json_data:
        for obj in json_data['objects']:
            if obj['type'] == 'path':
                path = obj['path']
                stroke = obj.get('stroke', 'black')
                stroke_width = int(obj.get('strokeWidth', 1))
                for i in range(len(path) - 1):
                    try:
                        p1 = tuple(map(float, path[i]))
                        p2 = tuple(map(float, path[i + 1]))
                        draw.line([p1, p2], fill=stroke, width=stroke_width)
                    except Exception:
                        continue  # skip malformed lines
    return image

# Helper to compute similarity
def calculate_similarity(img1, img2):
    img1 = img1.resize((300, 200)).convert("L")
    img2 = img2.resize((300, 200)).convert("L")
    arr1 = np.array(img1)
    arr2 = np.array(img2)
    similarity, _ = ssim(arr1, arr2, full=True)
    return similarity

# Callback for image comparison
@app.callback(
    Output('comparison-result', 'children'),
    Input('compare-button', 'n_clicks'),
    Input('drawing-canvas', 'json_data'),  # keep this as Input so we always get latest
    State('team-logo-dropdown', 'value')
)
def compare_images(n_clicks, json_data, logo_filename):
    if not n_clicks or not json_data or not logo_filename:
        return ""

    import json
    try:
        parsed_json = json.loads(json_data)
        drawing_img = parse_json_to_image(parsed_json, CANVAS_WIDTH, CANVAS_HEIGHT)

        logo_path = os.path.join(LOGO_FOLDER, logo_filename)
        logo_img = Image.open(logo_path)

        similarity = calculate_similarity(drawing_img, logo_img)
        return f"Similarity Score: {similarity:.2f}"

    except Exception as e:
        return f"Error comparing images: {str(e)}"

# Run the app
if __name__ == '__main__':
    app.run()
