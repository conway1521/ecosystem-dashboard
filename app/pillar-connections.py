from dash import html
import dash_bootstrap_components as dbc

def pillar_connections_view():
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H4("Place-based Conditions")),
                                dbc.CardBody(
                                    [
                                        html.Div("Institutional Infrastructure"),
                                        html.Div("Essential Services"),
                                        html.Div("Digital Infrastructure"),
                                    ]
                                ),
                            ],
                            className="border-primary border-3",
                        ),
                        width=4,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H4("Human & Social Capital")),
                                dbc.CardBody(
                                    [
                                        html.Div("Human Capital Development"),
                                        html.Div("Network Capital"),
                                        html.Div("Social Engagement"),
                                    ]
                                ),
                            ],
                            className="border-success border-3",
                        ),
                        width=4,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H4("Economic Activity")),
                                dbc.CardBody(
                                    [
                                        html.Div("Economic Base"),
                                        html.Div("Labour Market"),
                                        html.Div("Household Resources"),
                                    ]
                                ),
                            ],
                            className="border-danger border-3",
                        ),
                        width=4,
                    ),
                ]
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div("Institutional Infrastructure", className="text-secondary"),
                            html.Div("Human Capital Development", className="text-secondary"),
                        ],
                        className="flex justify-between items-center text-sm",
                    ),
                    html.Ul(
                        [
                            html.Li("Policy implementation", className="text-muted small"),
                            html.Li("Administrative effectiveness", className="text-muted small"),
                            html.Li("Development support", className="text-muted small"),
                        ],
                        className="mt-2 ps-3",
                    ),
                ],
                className="border-start ps-3 py-1",
            ),
            # Add more connection components as needed
        ],
        className="w-full max-w-7xl mx-auto p-4",
    )