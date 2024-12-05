"""
Regional Economic Development Ecosystem Dashboard
----------------------------------------------
A Dash application that visualizes the relationships between different pillars
of regional economic development: Place-based Conditions, Human & Social Capital,
and Economic Activity.

The app features two main views:
1. Pillar view: Shows detailed breakdown of each pillar's components
2. Connections view: Interactive visualization of relationships between pillars
"""

# --- Imports ---
import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc  # UI components
import plotly.graph_objects as go  # Interactive plotting
import numpy as np  # Numerical operations
import pandas as pd
from dash import dash_table

# --- App Initialization ---
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True  # Needed for dynamic components
)


# --- Helper Functions ---
def get_rgba_color(bootstrap_color, alpha=0.1):
    """Convert Bootstrap color names to RGBA values."""
    color_map = {
        'primary': (13, 110, 253),  # Bootstrap blue
        'success': (25, 135, 84),  # Bootstrap green
        'danger': (220, 53, 69),  # Bootstrap red
    }

    if bootstrap_color in color_map:
        rgb = color_map[bootstrap_color]
        return f'rgba{(*rgb, alpha)}'
    return f'rgba(0, 0, 0, {alpha})'  # Default fallback


# Add this with the other layout component functions
def create_data_tables_view():
    """Create the data tables view layout."""
    return html.Div([
        dbc.Container([
            # Title
            html.H3("Data Availability Matrices", className="mb-4"),

            # Dropdown selector
            dbc.Row([
                dbc.Col([
                    dbc.Select(
                        id="table-selector",
                        options=[
                            {"label": "Place-based Conditions", "value": "pbc"},
                            {"label": "Human & Social Capital", "value": "hsc"},
                            {"label": "Economic Activity", "value": "ea"}
                        ],
                        value="pbc",
                        className="mb-3"
                    )
                ], width=12, md=6, lg=4)
            ]),

            # Table display area
            dbc.Row([
                dbc.Col([
                    html.Div(id="data-table-container")
                ])
            ])
        ], fluid=True)
    ])

# --- Data Structures ---
# Pillar data defines the hierarchical structure of each pillar
pillars_data = {
    "pbc": {  # Place-based Conditions
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
    "hsc": {  # Human & Social Capital
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
    "ea": {  # Economic Activity
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


def create_connection_info():
    """Define the relationships between pillars and their descriptions."""
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


# --- Layout Components ---
def create_component(title, variables):
    """Create a collapsible component showing variables."""
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
    """Create a collapsible subject section containing components."""
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
    """Create a pillar card containing subjects."""
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
    """Create the main pillar view layout."""
    return dbc.Row([
        dbc.Col(
            create_pillar(pillar_id, data),
            width=12, lg=4, className="mb-4"
        ) for pillar_id, data in pillars_data.items()
    ], className="g-4")


def create_connections_view():
    """Create the interactive connections visualization."""
    connections = create_connection_info()

    # Define pillar positions
    pillars = {
        "pbc": {"x": -1, "y": 0, "title": "PbC", "color": "rgb(13, 110, 253)"},
        "hsc": {"x": 0, "y": 0, "title": "HSC", "color": "rgb(25, 135, 84)"},
        "ea": {"x": 1, "y": 0, "title": "EA", "color": "rgb(220, 53, 69)"}
    }

    # Create figure
    fig = go.Figure()

    # Add connections
    # Add connections with proper hover text formatting
    for key, conn in connections.items():
        from_pillar, to_pillar = key.split('-')
        x0, y0 = pillars[from_pillar]["x"], pillars[from_pillar]["y"]
        x1, y1 = pillars[to_pillar]["x"], pillars[to_pillar]["y"]

        # Create more points along the curve for better hover detection
        curve_height = 0.5 if x0 < x1 else -0.5
        x_points = np.linspace(x0, x1, 20)
        y_points = [y0 + 4 * curve_height * ((x - x0) * (x - x1)) / ((x1 - x0) ** 2) for x in x_points]

        # Fix hover text formatting - ensure all examples have bullets
        hover_text = (
                f"<b>{conn['from']} → {conn['to']}</b><br><br>• " +
                "<br>• ".join(conn['examples'])
        )
        # Add connection trace
        fig.add_trace(go.Scatter(
            x=x_points,
            y=y_points,
            mode='lines',
            line=dict(
                color=pillars[from_pillar]["color"],
                width=1.5
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

    # Update layout
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
        hoverdistance=100,
        uirevision=True
    )

    # Create layout
    # Create reorganized layout
    return html.Div([
        dbc.Container([
            # Title
            html.H3("Pillar Interconnections", className="mb-4"),

            # Understanding Connections card - now at the top
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
            ], className="mb-4"),

            # Graph in full width
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='connections-graph',
                        figure=fig,
                        config={'displayModeBar': False}
                    ),
                ], width=12),
            ], className="mb-4"),

            # Active connection info and details card - now below the graph
            dbc.Row([
                dbc.Col([
                    # Active connection info
                    html.Div(
                        id="active-connection-info",
                        className="mb-3"
                    ),
                    # Detailed connection card
                    html.Div(
                        id="connection-details-card",
                        style={"display": "none"}
                    )
                ], width=12),
            ])
        ], fluid=True)
    ])

# --- App Layout ---
app.layout = html.Div([
    # URL location component
    dcc.Location(id='url', refresh=False),

    # Navigation bar
    dbc.Navbar(
        dbc.Container(
            html.H3("Regional Economic Development Ecosystem", className="text-white mb-0"),
            fluid=True,
        ),
        color="dark",
        dark=True,
        className="mb-4",
    ),

    # Main container
    dbc.Container([
        # Navigation pills
        dbc.Nav([
            dbc.NavItem(dbc.NavLink("Pillars", href="/", active="exact")),
            dbc.NavItem(dbc.NavLink("Connections", href="/connections", active="exact")),
            dbc.NavItem(dbc.NavLink("Data Tables", href="/tables", active="exact")),
        ], pills=True, className="mb-4"),

        # Main content area
        html.Div(id='page-content')
    ], fluid=True),

    # Font Awesome CSS
    html.Link(
        rel='stylesheet',
        href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
    )
])


# --- Callbacks ---
@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    """Route to correct view based on URL pathname."""
    if pathname == '/connections':
        return create_connections_view()
    elif pathname == '/tables':
        return create_data_tables_view()
    return create_pillar_view()


@app.callback(
    # Dynamic outputs for all possible subject collapses
    [Output(f"{pillar}-subject-{i}-collapse", "is_open")
     for pillar in pillars_data.keys()
     for i in range(len(pillars_data[pillar]["subjects"]))],
    # Dynamic inputs for all possible subject buttons
    [Input(f"{pillar}-subject-{i}-button", "n_clicks")
     for pillar in pillars_data.keys()
     for i in range(len(pillars_data[pillar]["subjects"]))],
    # Dynamic states for all possible subject collapses
    [State(f"{pillar}-subject-{i}-collapse", "is_open")
     for pillar in pillars_data.keys()
     for i in range(len(pillars_data[pillar]["subjects"]))]
)
def toggle_collapse(*args):
    """Handle collapse toggling for pillar subjects."""
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
    """Update connection details when a connection is clicked."""
    if not clickData:
        # Reset everything when no connection is selected
        return None, {'display': 'none'}, None, figure

    # Get clicked connection information
    curve_number = clickData['points'][0]['curveNumber']
    try:
        conn_key = figure['data'][curve_number]['name']
        conn_info = create_connection_info()[conn_key]
    except (KeyError, IndexError):
        return None, {'display': 'none'}, None, figure

    # Create header
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

@callback(
    Output('data-table-container', 'children'),
    Input('table-selector', 'value')
)
def update_table(selected_table):
    """Update the displayed table based on selection."""
    # Define file paths
    table_files = {
        'pbc': '/Users/ali/Dropbox/PhD/Webapp/ecosystem-dashboard/app/components/pbc.csv',
        'hsc': '/Users/ali/Dropbox/PhD/Webapp/ecosystem-dashboard/app/components/hsc.csv',
        'ea': '/Users/ali/Dropbox/PhD/Webapp/ecosystem-dashboard/app/components/ea.csv'
    }

    if selected_table not in table_files:
        return html.P("Please select a table to view.", className="text-muted")

    # Read the selected CSV file directly into a DataFrame
    df = pd.read_csv(table_files[selected_table])

    # Display the table using dash_table.DataTable
    return dbc.Table(
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': col, 'id': col} for col in df.columns],
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'left',
                'minWidth': '180px',
                'width': '180px',
                'maxWidth': '180px',
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'lineHeight': '15px'
            },
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            }
        ),
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        className='table-sm'
    )

# --- Custom CSS ---
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
                        fill: white;
                        font-size: 14px;
                        font-weight: 500;
                    }
                    .table td, .table th {
                        white-space: normal !important;
                        vertical-align: middle !important;
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




# --- Server Configuration ---
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
