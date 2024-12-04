import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the pillars_data
pillars_data = {
    "pbc": {
        "title": "Place-based Conditions",
        "subjects": [
            {
                "title": "Basic Needs",
                "components": [
                    {
                        "title": "Environmental Quality",
                        "variables": ["Air quality", "Water quality", "Pollution exposure"]
                    },
                    {
                        "title": "Living Conditions",
                        "variables": ["Housing availability", "Housing affordability", "Neighborhood quality"]
                    },
                    {
                        "title": "Core Mobility",
                        "variables": ["Public transport coverage", "Road network quality", "Transport affordability"]
                    }
                ]
            },
            {
                "title": "Access",
                "components": [
                    {
                        "title": "Essential Services",
                        "variables": ["Healthcare access", "Education access", "Financial services"]
                    },
                    {
                        "title": "Digital Infrastructure",
                        "variables": ["Broadband coverage", "Digital service access", "Network quality"]
                    },
                    {
                        "title": "Institutional Infrastructure",
                        "variables": ["Policy implementation", "Administrative effectiveness", "Development support"]
                    }
                ]
            }
        ]
    },
    "hsc": {
        "title": "Human & Social Capital",
        "subjects": [
            {
                "title": "Human Capital Development",
                "components": [
                    {
                        "title": "Educational Foundation",
                        "variables": ["Educational attainment", "Early development", "Skills acquisition"]
                    },
                    {
                        "title": "Development Pathways",
                        "variables": ["Transition effectiveness", "Opportunity access", "Career progression"]
                    }
                ]
            },
            {
                "title": "Network Capital",
                "components": [
                    {
                        "title": "Network Structure",
                        "variables": ["Within-sector connectivity", "Cross-sector mobility"]
                    },
                    {
                        "title": "Network Effectiveness",
                        "variables": ["Job search outcomes", "Resource access", "Knowledge diffusion"]
                    }
                ]
            },
            {
                "title": "Social Engagement",
                "components": [
                    {
                        "title": "Institutional Engagement",
                        "variables": ["Behavioral trust", "Participation patterns"]
                    },
                    {
                        "title": "Social Cohesion",
                        "variables": ["Support networks", "Community belonging", "Social trust"]
                    }
                ]
            }
        ]
    },
    "ea": {
        "title": "Economic Activity",
        "subjects": [
            {
                "title": "Growth & Prosperity",
                "components": [
                    {
                        "title": "Economic Base",
                        "variables": ["GDP size", "Growth trends", "Living standards"]
                    },
                    {
                        "title": "Productive Efficiency",
                        "variables": ["Labor productivity", "Capital utilization", "Resource efficiency"]
                    }
                ]
            },
            {
                "title": "Labour Market",
                "components": [
                    {
                        "title": "Employment Structure",
                        "variables": ["Employment levels", "Labor market slack", "Job quality"]
                    },
                    {
                        "title": "Market Dynamics",
                        "variables": ["Job-match efficiency", "Market activity", "Career progression"]
                    }
                ]
            },
            {
                "title": "Household Resources",
                "components": [
                    {
                        "title": "Income Security",
                        "variables": ["Income levels", "Economic vulnerability", "Financial stability"]
                    },
                    {
                        "title": "Wealth Structure",
                        "variables": ["Asset base", "Financial inclusion", "Wealth mobility"]
                    }
                ]
            }
        ]
    }
}

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
                    dbc.CardHeader(
                        dbc.Button(
                            subject['title'],
                            id=f'{pillar_id}-{i}-subject-toggle',
                            color='link',
                            className='text-left w-100'
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(
                            [
                                html.Div([
                                    html.H6(component['title']),
                                    html.Ul([
                                        html.Li(var) for var in component['variables']
                                    ])
                                ]) for component in subject['components']
                            ]
                        ),
                        id=f'{pillar_id}-{i}-subject-collapse',
                    )
                ] for i, subject in enumerate(data)
            ),
            id="{}-card".format(pillar_id),
            className=f"pillar-container {position_class}"
        ],
        id=f"{pillar_id}-container",
    )

app.layout = html.Div([
    # Navigation bar
    dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.H3("Regional Economic Development Ecosystem")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="/",
                    style={"textDecoration": "none"},
                )
            ]
        ),
        color="dark",
        dark=True,
        className="mb-4",
    ),
    
    # Main content
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
