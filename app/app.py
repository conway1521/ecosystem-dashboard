import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
import matplotlib.colors

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Pillar data structure
pillars_data = {
    "pbc": {
        "title": "Place-based Conditions",
        "color": "primary",
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
        "color": "success",
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
        "color": "danger",
        "subjects": [
            {
                "title": "Growth & Prosperity",
                "components": [
                    {
                        "title": "Economic Base",
                        "variables": ["Size of local economy", "Living standards"]
                    },
                    {
                        "title": "Productive Efficiency",
                        "variables": ["Labor productivity", "Capital utilization"]
                    },
                    {
                        "title": "Economic Resilience",
                        "variables": ["Economic diversity"]
                    }
                ]
            },
            {
                "title": "Labour Market",
                "components": [
                    {
                        "title": "Employment Structure",
                        "variables": ["Employment levels", "Labor market slack"]
                    },
                    {
                        "title": "Job Quality",
                        "variables": ["Employment conditions", "Career progression"]
                    },
                    {
                        "title": "Labor Market Dynamics",
                        "variables": ["Job-match efficiency", "Market activity"]
                    }
                ]
            },
            {
                "title": "Household Resources",
                "components": [
                    {
                        "title": "Income Security",
                        "variables": ["Income levels", "Economic vulnerability"]
                    },
                    {
                        "title": "Wealth Structure",
                        "variables": ["Asset base", "Financial inclusion"]
                    }
                ]
            }
        ]
    }
}


def get_rgba_color(bootstrap_color, alpha=0.1):
    # Map Bootstrap colors to RGB values
    color_map = {
        'primary': (13, 110, 253),  # Bootstrap primary blue
        'success': (25, 135, 84),  # Bootstrap success green
        'danger': (220, 53, 69),  # Bootstrap danger red
    }

    if bootstrap_color in color_map:
        rgb = color_map[bootstrap_color]
        return f'rgba{(*rgb, alpha)}'
    return f'rgba(0, 0, 0, {alpha})'  # Default fallback



# Connection data structure
def create_connection_info():
    return {
        "pbc-hsc": {
            "from": "Place-based Conditions",
            "to": "Human & Social Capital",
            "examples": [
                "Institutional infrastructure enables skills development",
                "Digital infrastructure supports network formation",
                "Essential services access influences human capital",
                "Transport enables network building"
            ],
            "color": "primary"
        },
        "hsc-pbc": {
            "from": "Human & Social Capital",
            "to": "Place-based Conditions",
            "examples": [
                "Social engagement affects institutional effectiveness",
                "Network capital influences infrastructure use",
                "Human capital drives service demands",
                "Educational foundation shapes digital adoption"
            ],
            "color": "success"
        },
        "pbc-ea": {
            "from": "Place-based Conditions",
            "to": "Economic Activity",
            "examples": [
                "Infrastructure quality determines productivity",
                "Essential services enable business operations",
                "Digital infrastructure supports markets",
                "Transport affects market access"
            ],
            "color": "primary"
        },
        "ea-pbc": {
            "from": "Economic Activity",
            "to": "Place-based Conditions",
            "examples": [
                "Economic base determines infrastructure investment",
                "Market dynamics influence service provision",
                "Business environment shapes institutions",
                "Labour market affects transport demand"
            ],
            "color": "danger"
        },
        "hsc-ea": {
            "from": "Human & Social Capital",
            "to": "Economic Activity",
            "examples": [
                "Educational attainment affects productivity",
                "Network structure influences job matching",
                "Skills development shapes labour markets",
                "Social cohesion impacts economic resilience"
            ],
            "color": "success"
        },
        "ea-hsc": {
            "from": "Economic Activity",
            "to": "Human & Social Capital",
            "examples": [
                "Employment structure affects education choices",
                "Market dynamics shape network formation",
                "Income security influences social engagement",
                "Economic opportunity affects institutional trust"
            ],
            "color": "danger"
        }
    }


# Layout components
def create_component(title, variables):
    return html.Div([
        html.Div([
            html.Span(title, className="me-2 text-secondary"),
            html.I(className="fas fa-chevron-right")
        ], className="d-flex justify-content-between align-items-center"),
        html.Ul([
            html.Li(var, className="text-muted small") for var in variables
        ], className="mt-2 ps-3")
    ], className="border-start ps-3 py-1")


def create_subject(pillar_id, subject, index):
    return html.Div([
        dbc.Button(
            [
                html.Span(subject['title'], className="me-2 fw-semibold"),
                html.I(className="fas fa-chevron-right")
            ],
            id=f"{pillar_id}-subject-{index}-button",
            color="link",
            className="text-start p-0 text-decoration-none text-dark w-100 d-flex justify-content-between align-items-center"
        ),
        dbc.Collapse(
            html.Div([
                create_component(comp['title'], comp['variables'])
                for comp in subject['components']
            ], className="mt-2"),
            id=f"{pillar_id}-subject-{index}-collapse",
            is_open=False
        )
    ], className="border-start ps-3 py-2")


def create_pillar(pillar_id, data):
    return dbc.Card([
        dbc.CardBody([
            html.H4(data['title'], className="mb-4"),
            html.Div([
                create_subject(pillar_id, subject, i)
                for i, subject in enumerate(data['subjects'])
            ])
        ])
    ], className=f"border-{data['color']} border-3", style={'minWidth': '300px'})


def create_pillar_view():
    return dbc.Row([
        dbc.Col(
            create_pillar(pillar_id, data),
            width=12, lg=4, className="mb-4"
        ) for pillar_id, data in pillars_data.items()
    ], className="g-4")


def create_connections_view():
    connections = create_connection_info()

    # Define pillar positions with more space between them
    pillars = {
        "pbc": {"x": -1, "y": 0, "title": "Place-based Conditions", "color": "rgb(13, 110, 253)"},
        "hsc": {"x": 0, "y": 0, "title": "Human & Social Capital", "color": "rgb(25, 135, 84)"},
        "ea": {"x": 1, "y": 0, "title": "Economic Activity", "color": "rgb(220, 53, 69)"}
    }

    fig = go.Figure()

    # Add connections with more points for better hover detection
    for key, conn in connections.items():
        from_pillar, to_pillar = key.split('-')
        x0, y0 = pillars[from_pillar]["x"], pillars[from_pillar]["y"]
        x1, y1 = pillars[to_pillar]["x"], pillars[to_pillar]["y"]

        # Create more points along the curve for better hover detection
        curve_height = 0.5 if x0 < x1 else -0.5
        x_points = np.linspace(x0, x1, 20)
        y_points = [y0 + 4 * curve_height * ((x - x0) * (x - x1)) / ((x1 - x0) ** 2) for x in x_points]

        # Create hover text with examples
        hover_text = f"<b>{conn['from']} → {conn['to']}</b><br><br>" + "<br>• ".join(conn['examples'])

        # Add curved connection
        fig.add_trace(go.Scatter(
            x=x_points,
            y=y_points,
            mode='lines',
            line=dict(
                color=pillars[from_pillar]["color"],
                width=3
            ),
            hoverinfo='text',
            hovertext=hover_text,
            name=key,
            customdata=[key],
            hoverlabel=dict(
                bgcolor='white',
                font_size=14,
                font_family="Arial",
                bordercolor=pillars[from_pillar]["color"],
            ),
            fill='tonexty',
            fillcolor='rgba(0,0,0,0)'
        ))

    # Add pillar nodes
    for pillar_id, pillar in pillars.items():
        fig.add_trace(go.Scatter(
            x=[pillar["x"]],
            y=[pillar["y"]],
            mode="markers+text",
            name=pillar["title"],
            text=[pillar["title"]],
            textposition="middle center",
            marker=dict(
                size=50,
                color=pillar["color"],
                line=dict(color='white', width=2)
            ),
            hoverinfo="skip"
        ))

    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            range=[-1.5, 1.5],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            fixedrange=True
        ),
        yaxis=dict(
            range=[-1, 1],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            fixedrange=True
        ),
        height=500,
        margin=dict(l=20, r=20, t=20, b=20),
        hovermode='closest',
        hoverdistance=100,  # Increase hover detection radius
        uirevision=True  # Maintain state on updates
    )

    return html.Div([
        dbc.Container([
            html.H3("Pillar Interconnections", className="mb-4"),

            # Active connection info
            html.Div(
                id="active-connection-info",
                className="mb-4"
            ),

            # Graph component
            html.Div([
                dcc.Graph(
                    id='connections-graph',
                    figure=fig,
                    config={'displayModeBar': False}
                ),

                # Detailed connection card (hidden by default)
                dbc.Card(
                    id="connection-details-card",
                    className="position-absolute top-0 end-0 m-3",
                    style={"width": "300px", "display": "none"}
                )
            ], className="position-relative mb-4"),

            # Legend
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Understanding the Connections", className="mb-3"),
                            html.P([
                                "Click on any connection to see detailed information. ",
                                "The highlighting shows the direction of influence."
                            ], className="text-muted"),
                        ])
                    ], className="shadow-sm")
                ], width=12)
            ])
        ], fluid=True)
    ])


# App layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Navbar(
        dbc.Container(
            html.H3("Regional Economic Development Ecosystem", className="text-white mb-0"),
            fluid=True,
        ),
        color="dark",
        dark=True,
        className="mb-4",
    ),
    dbc.Container([
        dbc.Nav([
            dbc.NavItem(dbc.NavLink("Pillars", href="/", active="exact")),
            dbc.NavItem(dbc.NavLink("Connections", href="/connections", active="exact")),
        ], pills=True, className="mb-4"),
        html.Div(id='page-content')
    ], fluid=True),
    html.Link(
        rel='stylesheet',
        href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
    )
])


# Callbacks
@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/connections':
        return create_connections_view()
    return create_pillar_view()


@app.callback(
    [Output(f"{pillar}-subject-{i}-collapse", "is_open")
     for pillar in pillars_data.keys()
     for i in range(len(pillars_data[pillar]["subjects"]))],
    [Input(f"{pillar}-subject-{i}-button", "n_clicks")
     for pillar in pillars_data.keys()
     for i in range(len(pillars_data[pillar]["subjects"]))],
    [State(f"{pillar}-subject-{i}-collapse", "is_open")
     for pillar in pillars_data.keys()
     for i in range(len(pillars_data[pillar]["subjects"]))]
)
def toggle_collapse(*args):
    n = len(args) // 2
    clicks = args[:n]
    states = args[n:]

    ctx = dash.callback_context
    if not ctx.triggered:
        return [False] * n

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    button_ids = [f"{pillar}-subject-{i}-button"
                  for pillar in pillars_data.keys()
                  for i in range(len(pillars_data[pillar]["subjects"]))]

    try:
        index = button_ids.index(button_id)
        new_states = list(states)
        new_states[index] = not states[index]
        return new_states
    except ValueError:
        return states


@app.callback(
    [Output('connection-details-card', 'children'),
     Output('connection-details-card', 'style'),
     Output('active-connection-info', 'children'),
     Output('connections-graph', 'figure')],
    [Input('connections-graph', 'clickData')],
    [State('connections-graph', 'figure')]
)
def update_connection_details(clickData, figure):
    if not clickData:
        return None, {'display': 'none'}, None, figure

    # Get clicked trace name (connection key)
    curve_number = clickData['points'][0]['curveNumber']
    try:
        conn_key = figure['data'][curve_number]['name']
        conn_info = create_connection_info()[conn_key]
    except (KeyError, IndexError):
        return None, {'display': 'none'}, None, figure

    # Update the connection info header
    header = html.Div([
        html.H4([
            conn_info['from'],
            html.I(className="fas fa-arrow-right mx-3"),
            conn_info['to']
        ], className="text-center")
    ])

    # Create detailed card content
    card_content = dbc.CardBody([
        html.H5("Key Linkages", className="mb-3"),
        html.Ul([
            html.Li(example, className="mb-2")
            for example in conn_info['examples']
        ], className="ps-3"),
        html.Hr(),
        html.H5("Implications", className="mb-3"),
        html.P(
            "This connection represents how changes in one dimension directly influence "
            "outcomes in another, highlighting the interconnected nature of regional development.",
            className="text-muted"
        )
    ])

    # Highlight selected connection in figure
    new_figure = go.Figure(figure)
    for trace in new_figure.data:
        if isinstance(trace, go.Scatter) and trace.mode == 'lines':
            if trace.name == conn_key:
                trace.line.width = 5
                trace.fillcolor = get_rgba_color(conn_info['color'])
            else:
                trace.line.width = 2
                trace.fillcolor = 'rgba(0,0,0,0)'

    return (
        card_content,
        {
            'display': 'block',
            'backgroundColor': 'white',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
        },
        header,
        new_figure
    )

# Add CSS styles
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .connection-path {
                transition: stroke-width 0.2s ease;
                cursor: pointer;
            }
            .connection-path:hover {
                stroke-width: 4;
            }
            .pillar-node {
                fill: var(--bs-light);
                stroke: var(--bs-dark);
                stroke-width: 2;
            }
            .pillar-text {
                fill: var(--bs-dark);
                font-size: 14px;
                font-weight: 500;
            }
            .pillar-pbc .pillar-node {
                fill: var(--bs-primary);
            }
            .pillar-hsc .pillar-node {
                fill: var(--bs-success);
            }
            .pillar-ea .pillar-node {
                fill: var(--bs-danger);
            }
            .pillar-text {
                fill: white;
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

# Server
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)