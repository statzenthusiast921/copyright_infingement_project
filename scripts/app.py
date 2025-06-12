import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash_canvas import DashCanvas
import os

# App setup
app = dash.Dash(__name__)
server = app.server

# Logo image options (you can customize this list)
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

# Canvas size (same for canvas and logo)
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
            })
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

# Run the app
if __name__ == '__main__':
    app.run()
