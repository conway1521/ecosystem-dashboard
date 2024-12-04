import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Add custom CSS for transitions
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .pillar-container {
                transition: all 0.7s ease-in-out;
            }
            .pillar-zoom {
                transform: scale(1.5);
                z-index: 100;
            }
            .pillar-fade {
                opacity: 0.2;
                transform: scale(0.75);
            }
            .ecosystem-circle {
                position: relative;
                width: 600px;
                height: 600px;
                margin: auto;
                border: 2px solid #eee;
                border-radius: 50%;
            }
            .pillar-position-pbc {
                transform: translateY(-50%);
            }
            .pillar-position-hsc {
                transform: translate(-50%, 50%);
            }
            .pillar-position-ea {
                transform: translate(50%, 50%);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

def create_zoom_controls(pillar_id):
    return html.Div([
        dbc.Button(
            "Back to Overview",
            id=f"{pillar_id}-zoom-out",
            className="mr-2 d-none",
            color="light",
        ),
    ])

def create_pillar_box(pillar_id, data, position_class):
    return html.Div(
        [
            create_zoom_controls(pillar_id),
            dbc.Card(
                [
                    # Previous pillar box content
                    # [Same as before]
                ],
                id=f"{pillar_id}-card",
                className=f"pillar-container {position_class}"
            )
        ],
        id=f"{pillar_id}-container",
    )

app.layout = html.Div([
    # Navigation bar [Same as before]
    
    dbc.Container([
        html.Div([
            html.Div(
                [
                    create_pillar_box("pbc", pillars_data["pbc"], "pillar-position-pbc"),
                    create_pillar_box("hsc", pillars_data["hsc"], "pillar-position-hsc"),
                    create_pillar_box("ea", pillars_data["ea"], "pillar-position-ea"),
                ],
                className="ecosystem-circle",
                id="ecosystem-container"
            )
        ],
        className="position-relative h-100 d-flex align-items-center justify-content-center"
        )
    ],
    fluid=True,
    className="h-100"
    ),
    
    # Store for tracking zoom state
    dcc.Store(id="zoom-state", data=None)
])

# Callback for zoom functionality
@app.callback(
    [Output(f"{pid}-container", "className") for pid in ["pbc", "hsc", "ea"]] +
    [Output("zoom-state", "data")],
    [Input(f"{pid}-card", "n_clicks") for pid in ["pbc", "hsc", "ea"]] +
    [Input(f"{pid}-zoom-out", "n_clicks") for pid in ["pbc", "hsc", "ea"]],
    [State("zoom-state", "data")],
)
def handle_zoom(*args):
    clicks = args[:3]
    zoom_outs = args[3:6]
    current_state = args[-1]
    
    ctx = dash.callback_context
    if not ctx.triggered:
        return [""] * 3 + [None]
        
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    # Handle zoom out
    if "zoom-out" in trigger_id:
        return [""] * 3 + [None]
    
    # Handle zoom in
    pillar_id = trigger_id.split("-")[0]
    if current_state is None:
        classes = []
        for pid in ["pbc", "hsc", "ea"]:
            if pid == pillar_id:
                classes.append("pillar-zoom")
            else:
                classes.append("pillar-fade")
        return classes + [pillar_id]
    
    return [""] * 3 + [None]


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
