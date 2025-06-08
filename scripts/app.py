import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash_canvas import DashCanvas

# App initialization
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Drawing Canvas with Color Picker"),

    html.Div([
        html.Label("Choose Brush Color:"),
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
    ], style={'width': '300px', 'margin': '10px'}),

    DashCanvas(
        id='drawing-canvas',
        width=600,
        height=400,
        lineColor='black',
        lineWidth=3,
        hide_buttons=['zoom', 'pan', 'reset']
    )
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

# Run app
if __name__ == '__main__':
    app.run()
