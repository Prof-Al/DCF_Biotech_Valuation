import dash
import pandas as pd
import pymongo
import dash_daq as daq
import plotly.express as px
from dash import callback, html, dcc, dash_table, no_update
from dash.dash_table import FormatTemplate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from bson.objectid import ObjectId

import settings
from utils import *

dash.register_page(
    __name__,
    path="/add_asset",
    title="Add Asset",
    name="Add Asset",
    description="Adds a new asset",
)

assets_collection = get_collection("assets")
patient_schedule_collection = get_collection("patients_schedule")
development_milestones_collection = get_collection("development_milestones")
sales_milestones_collection = get_collection("sales_milestones")
royalty_tiers_collection = get_collection("royalty_tiers")


refresh_persists = False


def asset_details_card():
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Asset Details", className="card-title"),
                html.Div(
                    dbc.Row(
                        [
                            dbc.Label(
                                [
                                    "Asset Name",
                                ],
                                width=2,
                            ),
                            dbc.Col(
                                [
                                    dbc.Input(
                                        type="text",
                                        id="asset_name",
                                        persistence=refresh_persists,
                                    ),
                                ],
                                width=4,
                            ),
                            dbc.Col(
                                [
                                    dbc.RadioItems(
                                        options=[
                                            {"label": "Phase 1", "value": "phase_1"},
                                            {"label": "Phase 2", "value": "phase_2"},
                                            {"label": "Phase 3", "value": "phase_3"},
                                            {"label": "FDA Submission", "value": "fda_submission"},
                                            {"label": "Commercialization", "value": "commercialization"},
                                        ],
                                        id="phase_picker",
                                        inline=True,
                                        persistence=refresh_persists,
                                    )
                                ],
                                width=6
                            ),
                        ],
                        className="p-1",
                    ),
                ),
                dbc.Row(
                    [
                        # html.Hr(),
                        dbc.Label(
                            [
                                "Probability of Success (%)",
                                html.I(
                                    className="bi bi-info-square ms-2",
                                    id="success_probability_i",
                                ),
                            ],
                            width="auto",
                        ),
                        dbc.Col(
                            [
                                dbc.Input(
                                    type="number",
                                    min=1,
                                    max=100,
                                    id="success_probability",
                                    persistence=refresh_persists,
                                ),
                                dbc.FormFeedback("", type="valid"),
                                dbc.FormFeedback(
                                    f"it should be an integer number ≤ 100", type="invalid"
                                ),
                            ],
                            width=3,
                        ),
                        dbc.Tooltip(
                            settings.success_probability_tt,
                            target="success_probability_i",
                        ),
                    ],
                    className="p-1",
                ),
                html.Div(
                    dbc.Row(
                        [
                            dbc.Label(
                                [
                                    "Patent Expiry (US)",
                                ],
                                width="auto",
                            ),
                            dbc.Col(
                                [
                                    dbc.Input(
                                        type="number",
                                        min=2022,
                                        max=2050,
                                        id="patent_expiry_us",
                                        persistence=refresh_persists,
                                    ),
                                    dbc.FormFeedback("", type="valid"),
                                    dbc.FormFeedback(
                                        f"it should be an integer number between 2022 and 2050", type="invalid"
                                    ),
                                ],
                                width=1,
                            ),
                            dbc.Label(
                                [
                                    "Patent Expiry (Europe)",
                                ],
                                width="auto",
                            ),
                            dbc.Col(
                                [
                                    dbc.Input(
                                        type="number",
                                        min=2022,
                                        max=2050,
                                        id="patent_expiry_eur",
                                        persistence=refresh_persists,
                                    ),
                                    dbc.FormFeedback("", type="valid"),
                                    dbc.FormFeedback(
                                        f"it should be an integer number between 2022 and 2050", type="invalid"
                                    ),
                                ],
                                width=1,
                            ),
                            dbc.Label(
                                [
                                    "Patent Expiry (ROW)",
                                ],
                                width="auto",
                            ),
                            dbc.Col(
                                [
                                    dbc.Input(
                                        type="number",
                                        min=2022,
                                        max=2050,
                                        id="patent_expiry_row",
                                        persistence=refresh_persists,
                                    ),
                                    dbc.FormFeedback("", type="valid"),
                                    dbc.FormFeedback(
                                        f"it should be an integer number between 2022 and 2050", type="invalid"
                                    ),
                                ],
                                width=1,
                            ),
                        ],
                        className="p-1",
                        justify="center"
                    ),

                ),
            ]
        )
    )
    return card


def market_details_card():
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Market Details", className="card-title"),
                html.Div(
                    dbc.Row(
                        [
                            dbc.Label(
                                [
                                    "Market Entry (US)",
                                ],
                                width="auto",
                            ),
                            dbc.Col(
                                [
                                    dbc.Input(
                                        type="number",
                                        min=2022,
                                        max=2050,
                                        id="market_entry_us",
                                        persistence=refresh_persists,
                                    ),
                                    dbc.FormFeedback("", type="valid"),
                                    dbc.FormFeedback(
                                        f"it should be an integer number between 2022 and 2050", type="invalid"
                                    ),
                                ],
                                width=1,
                            ),
                            dbc.Label(
                                [
                                    "Market Entry (Europe)",
                                ],
                                width="auto",
                            ),
                            dbc.Col(
                                [
                                    dbc.Input(
                                        type="number",
                                        min=2022,
                                        max=2050,
                                        id="market_entry_eur",
                                        persistence=refresh_persists,
                                    ),
                                    dbc.FormFeedback("", type="valid"),
                                    dbc.FormFeedback(
                                        f"it should be an integer number between 2022 and 2050", type="invalid"
                                    ),
                                ],
                                width=1,
                            ),
                            dbc.Label(
                                [
                                    "Market Entry (ROW)",
                                ],
                                width="auto",
                            ),
                            dbc.Col(
                                [
                                    dbc.Input(
                                        type="number",
                                        min=2022,
                                        max=2050,
                                        id="market_entry_row",
                                        persistence=refresh_persists,
                                    ),
                                    dbc.FormFeedback("", type="valid"),
                                    dbc.FormFeedback(
                                        f"it should be an integer number between 2022 and 2050", type="invalid"
                                    ),
                                ],
                                width=1,
                            ),
                        ],
                        className="p-1",
                        justify="center"
                    ),

                ),
                html.Div(
                    dbc.Row(
                        [
                            dbc.Label(
                                [
                                    "Patient Population (US)",
                                ],
                                width="auto",
                            ),
                            dbc.Col(
                                [
                                    dbc.Input(
                                        type="number",
                                        min=0,
                                        id="patient_population_us",
                                        persistence=refresh_persists,
                                    ),
                                    dbc.FormFeedback("", type="valid"),
                                    dbc.FormFeedback(
                                        f"it should be an integer number greater than 0", type="invalid"
                                    ),
                                ],
                                width=2,
                            ),
                            dbc.Label(
                                [
                                    "Patient Population (Europe)",
                                ],
                                width="auto",
                            ),
                            dbc.Col(
                                [
                                    dbc.Input(
                                        type="number",
                                        min=0,
                                        id="patient_population_eur",
                                        persistence=refresh_persists,
                                    ),
                                    dbc.FormFeedback("", type="valid"),
                                    dbc.FormFeedback(
                                        f"it should be an integer number greater than 0", type="invalid"
                                    ),
                                ],
                                width=2,
                            ),
                            dbc.Label(
                                [
                                    "Patient Population (ROW)",
                                ],
                                width="auto",
                            ),
                            dbc.Col(
                                [
                                    dbc.Input(
                                        type="number",
                                        min=0,
                                        id="patient_population_row",
                                        persistence=refresh_persists,
                                    ),
                                    dbc.FormFeedback("", type="valid"),
                                    dbc.FormFeedback(
                                        f"it should be an integer number greater than 0", type="invalid"
                                    ),
                                ],
                                width=2,
                            ),
                        ],
                        className="p-1",
                        justify="center"
                    ),

                ),

            ]
        )
    )
    return card


def pricing_details_card():
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Pricing Details", className="card-title"),
                html.Div(
                    dbc.Row(
                        [
                            dbc.Label(
                                [
                                    "Annual Pricing $ (US)",
                                ],
                                width="auto",
                            ),
                            dbc.Col(
                                [
                                    dbc.Input(
                                        type="number",
                                        min=0,
                                        id="pricing_us",
                                        persistence=refresh_persists,
                                    ),
                                    dbc.FormFeedback("", type="valid"),
                                    dbc.FormFeedback(
                                        f"it should be an integer number greater than 0", type="invalid"
                                    ),
                                ],
                                width=2,
                            ),
                            dbc.Label(
                                [
                                    "Annual Pricing $ (Europe)",
                                ],
                                width="auto",
                            ),
                            dbc.Col(
                                [
                                    dbc.Input(
                                        type="number",
                                        min=0,
                                        id="pricing_eur",
                                        persistence=refresh_persists,
                                    ),
                                    dbc.FormFeedback("", type="valid"),
                                    dbc.FormFeedback(
                                        f"it should be an integer number greater than 0", type="invalid"
                                    ),
                                ],
                                width=2,
                            ),
                            dbc.Label(
                                [
                                    "Annual Pricing $ (ROW)",
                                ],
                                width="auto",
                            ),
                            dbc.Col(
                                [
                                    dbc.Input(
                                        type="number",
                                        min=0,
                                        id="pricing_row",
                                        persistence=refresh_persists,
                                    ),
                                    dbc.FormFeedback("", type="valid"),
                                    dbc.FormFeedback(
                                        f"it should be an integer number greater than 0", type="invalid"
                                    ),
                                ],
                                width=2,
                            ),
                        ],
                        className="p-1",
                        justify="center"
                    ),

                ),
            ]
        )
    )
    return card


def patient_details_card():
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Patient Details", className="card-title"),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.RadioItems(
                                    options=[
                                        {"label": "Linear", "value": "linear"},
                                        {"label": "Logarithmic", "value": "logarithmic"},
                                        {"label": "Custom", "value": "custom"},
                                    ],
                                    id="patient_adoption_rate_picker",
                                    inline=True,
                                    persistence=refresh_persists,
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Label(
                                    [
                                        "First Year Adoption",
                                    ],
                                    id="first_year_adoption_label",
                                    hidden=True
                                ),
                            ],
                            width="auto",
                        ),
                        dbc.Col(
                            [
                                dbc.Input(
                                    type="number",
                                    style={"display": "none"},
                                    min=0,
                                    id="first_year_adoption",
                                    persistence=refresh_persists,
                                ),
                            ],
                            width=2,
                        ),
                        dbc.Col(
                            [
                                dbc.Label(
                                    [
                                        "Long Term Adoption Rate (%)",
                                    ],
                                    width="auto",
                                    id="long_term_adoption_rate_label",
                                    hidden=True
                                ),
                            ],
                            width="auto",
                        ),
                        dbc.Col(
                            [
                                dbc.Input(
                                    type="number",
                                    style={"display": "none"},
                                    min=0,
                                    max=100,
                                    id="long_term_adoption_rate",
                                    persistence=refresh_persists,
                                ),
                            ],
                            width=2,
                        ),
                    ]
                ),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H6("US", className="class-subtitle"),
                                    ],
                                    width=1
                                ),
                                dbc.Col(
                                    [
                                        html.Button('Toggle Graph', id='toggle_patient_schedule_us', n_clicks=0),
                                    ]
                                ),
                            ]
                        ),

                        dbc.Row(
                            [
                                dbc.Label(
                                    [
                                        "Market Penetration (%)",
                                    ],
                                    width="auto",
                                ),
                                dbc.Col(
                                    [
                                        dbc.Input(
                                            type="number",
                                            min=0,
                                            max=100,
                                            id="market_penetration_us",
                                            persistence=refresh_persists,
                                        ),
                                        dbc.FormFeedback("", type="valid"),
                                        dbc.FormFeedback(
                                            f"it should be an integer number between 0 and 100", type="invalid"
                                        ),
                                    ],
                                    width=2,
                                ),
                                dbc.Label(
                                    [
                                        "Net Market Size Increase (p.a)",
                                    ],
                                    width="auto",
                                ),
                                dbc.Col(
                                    [
                                        dbc.Input(
                                            type="number",
                                            value=0,
                                            id="market_size_increase_us",
                                            persistence=refresh_persists,
                                        ),
                                        dbc.FormFeedback("", type="valid"),
                                        dbc.FormFeedback(
                                            f"it should be an integer number", type="invalid"
                                        ),
                                    ],
                                    width=2,
                                ),
                                dbc.Label(
                                    [
                                        "Year of Peak Sales",
                                    ],
                                    width="auto",
                                    id="peak_sales_year_us_label"
                                ),
                                dbc.Col(
                                    [
                                        dbc.Input(
                                            type="number",
                                            min=2022,
                                            max=2050,
                                            id="peak_sales_year_us",
                                            persistence=refresh_persists,
                                        ),
                                        dbc.FormFeedback("", type="valid"),
                                        dbc.FormFeedback(
                                            f"it should be an integer number between 2022 and 2050", type="invalid"
                                        ),
                                    ],
                                    width=2,
                                ),
                                html.Br(),
                                dash_table.DataTable(
                                    id="patient_schedule_us",
                                ),
                                html.Br(),
                                html.Div(id='patient_schedule_us_chart_container', style={'display': 'none'}),
                            ],
                            className="p-1",
                            justify="center"
                        ),
                    ]
                ),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H6("Europe", className="class-subtitle"),
                                    ],
                                    width=1
                                ),
                                dbc.Col(
                                    [
                                        html.Button('Toggle Graph', id='toggle_patient_schedule_eur', n_clicks=0),
                                    ]
                                ),
                            ]
                        ),

                        dbc.Row(
                            [
                                dbc.Label(
                                    [
                                        "Market Penetration (%)",
                                    ],
                                    width="auto",
                                ),
                                dbc.Col(
                                    [
                                        dbc.Input(
                                            type="number",
                                            min=0,
                                            max=100,
                                            id="market_penetration_eur",
                                            persistence=refresh_persists,
                                        ),
                                        dbc.FormFeedback("", type="valid"),
                                        dbc.FormFeedback(
                                            f"it should be an integer number between 0 and 100", type="invalid"
                                        ),
                                    ],
                                    width=2,
                                ),
                                dbc.Label(
                                    [
                                        "Net Market Size Increase (p.a)",
                                    ],
                                    width="auto",
                                ),
                                dbc.Col(
                                    [
                                        dbc.Input(
                                            type="number",
                                            value=0,
                                            id="market_size_increase_eur",
                                            persistence=refresh_persists,
                                        ),
                                        dbc.FormFeedback("", type="valid"),
                                        dbc.FormFeedback(
                                            f"it should be an integer number", type="invalid"
                                        ),
                                    ],
                                    width=2,
                                ),
                                dbc.Label(
                                    [
                                        "Year of Peak Sales",
                                    ],
                                    width="auto",
                                    id="peak_sales_year_eur_label"
                                ),
                                dbc.Col(
                                    [
                                        dbc.Input(
                                            type="number",
                                            min=2022,
                                            max=2050,
                                            id="peak_sales_year_eur",
                                            persistence=refresh_persists,
                                        ),
                                        dbc.FormFeedback("", type="valid"),
                                        dbc.FormFeedback(
                                            f"it should be an integer number between 2022 and 2050", type="invalid"
                                        ),
                                    ],
                                    width=2,
                                ),
                                html.Br(),
                                dash_table.DataTable(
                                    id="patient_schedule_eur",
                                ),
                                html.Br(),
                                html.Div(id='patient_schedule_eur_chart_container', style={'display': 'none'}),
                            ],
                            className="p-1",
                            justify="center"
                        ),
                    ]
                ),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H6("ROW", className="class-subtitle"),
                                    ],
                                    width=1
                                ),
                                dbc.Col(
                                    [
                                        html.Button('Toggle Graph', id='toggle_patient_schedule_row', n_clicks=0),
                                    ]
                                ),
                            ]
                        ),

                        dbc.Row(
                            [
                                dbc.Label(
                                    [
                                        "Market Penetration (%)",
                                    ],
                                    width="auto",
                                ),
                                dbc.Col(
                                    [
                                        dbc.Input(
                                            type="number",
                                            min=0,
                                            max=100,
                                            id="market_penetration_row",
                                            persistence=refresh_persists,
                                        ),
                                        dbc.FormFeedback("", type="valid"),
                                        dbc.FormFeedback(
                                            f"it should be an integer number between 0 and 100", type="invalid"
                                        ),
                                    ],
                                    width=2,
                                ),
                                dbc.Label(
                                    [
                                        "Net Market Size Increase (p.a)",
                                    ],
                                    width="auto",
                                ),
                                dbc.Col(
                                    [
                                        dbc.Input(
                                            type="number",
                                            value=0,
                                            id="market_size_increase_row",
                                            persistence=refresh_persists,
                                        ),
                                        dbc.FormFeedback("", type="valid"),
                                        dbc.FormFeedback(
                                            f"it should be an integer number", type="invalid"
                                        ),
                                    ],
                                    width=2,
                                ),
                                dbc.Label(
                                    [
                                        "Year of Peak Sales",
                                    ],
                                    width="auto",
                                    id="peak_sales_year_row_label"
                                ),
                                dbc.Col(
                                    [
                                        dbc.Input(
                                            type="number",
                                            min=2022,
                                            max=2050,
                                            id="peak_sales_year_row",
                                            persistence=refresh_persists,
                                        ),
                                        dbc.FormFeedback("", type="valid"),
                                        dbc.FormFeedback(
                                            f"it should be an integer number between 2022 and 2050", type="invalid"
                                        ),
                                    ],
                                    width=2,
                                ),
                                html.Br(),
                                dash_table.DataTable(
                                    id="patient_schedule_row",
                                ),
                                html.Br(),
                                html.Div(id='patient_schedule_row_chart_container', style={'display': 'none'}),
                            ],
                            className="p-1",
                            justify="center"
                        ),
                    ]
                )
            ]
        )
    )
    return card


def licensing_details_card():
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Licensing Details", className="card-title"),
                daq.BooleanSwitch(
                    on=True,
                    label="Is this asset licensed to a separate company?",
                    labelPosition="top",
                    id="licensed_switch",
                ),
                dbc.Row(
                    [
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                daq.BooleanSwitch(
                                                    on=False,
                                                    label="Development Milestone Payments",
                                                    labelPosition="top",
                                                    id="development_milestone_switch",
                                                ),
                                                html.Button('Add Milestone', id='add_development_milestone_row', n_clicks=0, hidden=True),
                                            ]
                                        ),
                                        dbc.Col(
                                            [
                                                daq.BooleanSwitch(
                                                    on=False,
                                                    label="Sales Milestone Payments",
                                                    labelPosition="top",
                                                    id="sales_milestone_switch",
                                                ),
                                                html.Button('Add Milestone', id='add_sales_milestone_row', n_clicks=0, hidden=True),
                                            ]
                                        ),
                                        dbc.Col(
                                            [
                                                daq.BooleanSwitch(
                                                    on=False,
                                                    label="Royalty Payments",
                                                    labelPosition="top",
                                                    id="royalty_switch",
                                                ),
                                                html.Button('Add Tier', id='add_royalty_row', n_clicks=0, hidden=True),
                                            ]
                                        ),
                                    ]
                                ),
                            ],
                            style={'display': 'none'},
                            id="licensing_switches"
                        ),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.Div(
                                                    [
                                                        dash_table.DataTable(
                                                            columns=[
                                                                dict(id='milestone', name="Milestone"),
                                                                dict(id='amount',
                                                                     name="Amount ($)", type='numeric', format=money),
                                                                dict(id='achievement_year',
                                                                     name="(Est) Year of Achievement", type='numeric'),
                                                            ],
                                                            row_deletable=True,
                                                            data=[{}],
                                                            editable=True,
                                                            style_cell={'whiteSpace': 'normal'},
                                                            id="development_milestone_table",

                                                        )
                                                    ],
                                                    style={'display': 'none'},
                                                    id="development_milestone_details"
                                                ),
                                            ]
                                        ),
                                        dbc.Col(
                                            [
                                                html.Div(
                                                    [
                                                        dash_table.DataTable(
                                                            columns=[
                                                                dict(id='sales_exceeding', name="Sales Exceeding ($)",
                                                                     type='numeric', format=money),
                                                                dict(id='amount',
                                                                     name="Amount ($)", type='numeric', format=money)
                                                            ],
                                                            row_deletable=True,
                                                            data=[{}],
                                                            editable=True,
                                                            style_cell={'whiteSpace': 'normal'},
                                                            id="sales_milestone_table",

                                                        )
                                                    ],
                                                    style={'display': 'none'},
                                                    id="sales_milestone_details"
                                                ),
                                            ]
                                        ),
                                        dbc.Col(
                                            [
                                                html.Div(
                                                    [
                                                        dash_table.DataTable(
                                                            columns=[
                                                                dict(id='upto_royalty', name="Upto ($)", type='numeric', format=money),
                                                                dict(id='royalty_percent', name="Royalty (%)", type='numeric', format=percentage)
                                                                ],
                                                            row_deletable=True,
                                                            data=[{}],
                                                            editable=True,
                                                            style_cell={'whiteSpace': 'normal'},
                                                            id="royalty_table",

                                                        )
                                                    ],
                                                    style={'display': 'none'},
                                                    id="royalty_details"
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                html.Button('Add Asset', id='add_asset', n_clicks=0),
                dbc.Toast(
                    children=html.P(id="add_asset_toast_message"),
                    id="add_asset_toast",
                    header="Asset Added",
                    is_open=False,
                    dismissable=True,
                    icon="primary",
                    duration=4000,
                    style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                ),
            ]
        )
    )
    return card


def layout():
    print("layoutttttttttttttttttttttttttt")

    page = dbc.Container(
        [
            dbc.Col(asset_details_card()),
            dbc.Col(market_details_card()),
            dbc.Col(pricing_details_card()),
            dbc.Col(patient_details_card()),
            dbc.Col(licensing_details_card()),

        ]
    )
    print("returnedddd")
    return page


@callback(Output('licensing_switches', 'style'),
          Input('licensed_switch', 'on'))
def is_licensed(switch):
    if switch is False:
        return {'display': 'none'}
    else:
        return {'display': 'block'}


@callback(Output('development_milestone_details', 'style'),
          Output('add_development_milestone_row', 'hidden'),
          Input('development_milestone_switch', 'on'))
def is_development_milestone(switch):
    if switch is False:
        return {'display': 'none'}, True
    else:
        return {'display': 'block'}, False


@callback(Output('sales_milestone_details', 'style'),
          Output('add_sales_milestone_row', 'hidden'),
          Input('sales_milestone_switch', 'on'))
def is_sales_milestone(switch):
    if switch is False:
        return {'display': 'none'}, True
    else:
        return {'display': 'block'}, False


@callback(Output('royalty_details', 'style'),
          Output('add_royalty_row', 'hidden'),
          Input('royalty_switch', 'on'))
def is_royalty_milestone(switch):
    if switch is False:
        return {'display': 'none'}, True
    else:
        return {'display': 'block'}, False


@callback(Output('development_milestone_table', 'data'),
          Input('add_development_milestone_row', 'n_clicks'),
          State('development_milestone_table', 'data'),
          State('development_milestone_table', 'columns'))
def add_development_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


@callback(Output('sales_milestone_table', 'data'),
          Input('add_sales_milestone_row', 'n_clicks'),
          State('sales_milestone_table', 'data'),
          State('sales_milestone_table', 'columns'))
def add_sales_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


@callback(Output('royalty_table', 'data'),
          Input('add_royalty_row', 'n_clicks'),
          State('royalty_table', 'data'),
          State('royalty_table', 'columns'))
def add_royalty_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


@callback(Output('success_probability', component_property='value', allow_duplicate=True),
          Input('phase_picker', component_property='value'),
          prevent_initial_call=True
          )
def success_probability(phase):
    if phase == "phase_1":
        return 10
    elif phase == "phase_2":
        return 25
    elif phase == "phase_3":
        return 50
    elif phase == "fda_submission":
        return 90
    elif phase == "commercialization":
        return 100


@callback(Output('patient_schedule_us', component_property='columns'),
          Output('patient_schedule_us', component_property='data'),
          Output('patient_schedule_us', component_property='editable'),
          Input('market_entry_us', 'value'),
          Input('patent_expiry_us', component_property='value'),
          Input('patient_population_us', component_property='value'),
          Input('market_penetration_us', component_property='value'),
          Input('market_size_increase_us', component_property='value'),
          Input('peak_sales_year_us', component_property='value'),
          Input('patient_adoption_rate_picker', component_property='value'),
          Input('first_year_adoption', 'value'),
          Input('long_term_adoption_rate', 'value'),
          Input('patient_schedule_us', component_property='data'))
def patient_schedule_size_us(me, pe, pp, mp, nmi, psy, par, fya, ltar, data):
    if None in (me, pe):
        return [], [], False
    me, pe = int(me), int(pe)
    if (me < 2022 or me > 2050 or pe < 2022 or pe > 2050) and me >= pe:
        return [], [], False
    elif None in (pp, mp, nmi, par):
        df = pd.DataFrame()
        for i in range(me, pe + 1):
            df = df.join(pd.DataFrame({}))
        return [{"name": str(i), "id": str(i)} for i in range(me, pe + 1)], [], False
    elif par == "linear":
        if psy is None:
            return [{"name": str(i), "id": str(i)} for i in range(me, pe + 1)], [], False
        schedule = []
        current_pop = pp
        current_patients = 0
        for cy in range(me, pe + 1):
            current_pop += nmi
            max_patients = current_pop * (mp/100)
            if psy >= cy:
                patient_increase = round((max_patients - current_patients) / (psy - cy + 1), 0)
            else:
                patient_increase = round(nmi * (mp/100), 0)
            current_patients += patient_increase
            schedule.append(current_patients)
        df = pd.DataFrame(schedule).transpose()
        df.columns = [i for i in range(me, pe + 1)]
        return [{"name": str(i), "id": str(i)} for i in df.columns], df.to_dict('records'), False
    elif par == "logarithmic":
        if None in (fya, ltar):
            return [{"name": str(i), "id": str(i)} for i in range(me, pe + 1)], [], False
        schedule = []
        current_pop = pp
        current_patients = fya
        schedule.append(current_patients)

        for i, cy in enumerate(range(me + 1, pe + 1)):
            current_pop += nmi
            max_patients = current_pop * (mp/100)
            current_patients = round(min(max_patients, schedule[i] * (1 + (ltar/100))), 0)
            schedule.append(current_patients)
        df = pd.DataFrame(schedule).transpose()
        df.columns = [i for i in range(me, pe + 1)]
        return [{"name": str(i), "id": str(i)} for i in df.columns], df.to_dict('records'), False

    elif par == "custom":

        return [{"name": str(i), "id": str(i)} for i in range(me, pe + 1)], data, True


@callback(Output('patient_schedule_eur', component_property='columns'),
          Output('patient_schedule_eur', component_property='data'),
          Output('patient_schedule_eur', component_property='editable'),
          Input('market_entry_eur', 'value'),
          Input('patent_expiry_eur', component_property='value'),
          Input('patient_population_eur', component_property='value'),
          Input('market_penetration_eur', component_property='value'),
          Input('market_size_increase_eur', component_property='value'),
          Input('peak_sales_year_eur', component_property='value'),
          Input('patient_adoption_rate_picker', component_property='value'),
          Input('first_year_adoption', 'value'),
          Input('long_term_adoption_rate', 'value'),
          Input('patient_schedule_eur', component_property='data'))
def patient_schedule_size_eur(me, pe, pp, mp, nmi, psy, par, fya, ltar, data):
    if None in (me, pe):
        return [], [], False
    me, pe = int(me), int(pe)
    if (me < 2022 or me > 2050 or pe < 2022 or pe > 2050) and me >= pe:
        return [], [], False
    elif None in (pp, mp, nmi, par):
        df = pd.DataFrame()
        for i in range(me, pe + 1):
            df = df.join(pd.DataFrame({}))
        return [{"name": str(i), "id": str(i)} for i in range(me, pe + 1)], [], False
    elif par == "linear":
        if psy is None:
            return [{"name": str(i), "id": str(i)} for i in range(me, pe + 1)], [], False
        schedule = []
        current_pop = pp
        current_patients = 0
        for cy in range(me, pe + 1):
            current_pop += nmi
            max_patients = current_pop * (mp/100)
            if psy >= cy:
                patient_increase = round((max_patients - current_patients) / (psy - cy + 1), 0)
            else:
                patient_increase = round(nmi * (mp/100), 0)
            current_patients += patient_increase
            schedule.append(current_patients)
        df = pd.DataFrame(schedule).transpose()
        df.columns = [i for i in range(me, pe + 1)]
        return [{"name": str(i), "id": str(i)} for i in df.columns], df.to_dict('records'), False
    elif par == "logarithmic":
        if None in (fya, ltar):
            return [{"name": str(i), "id": str(i)} for i in range(me, pe + 1)], [], False
        schedule = []
        current_pop = pp
        current_patients = fya
        schedule.append(current_patients)

        for i, cy in enumerate(range(me + 1, pe + 1)):
            current_pop += nmi
            max_patients = current_pop * (mp/100)
            current_patients = round(min(max_patients, schedule[i] * (1 + (ltar/100))), 0)
            schedule.append(current_patients)
        df = pd.DataFrame(schedule).transpose()
        df.columns = [i for i in range(me, pe + 1)]
        return [{"name": str(i), "id": str(i)} for i in df.columns], df.to_dict('records'), False

    elif par == "custom":

        return [{"name": str(i), "id": str(i)} for i in range(me, pe + 1)], data, True


@callback(Output('patient_schedule_row', component_property='columns'),
          Output('patient_schedule_row', component_property='data'),
          Output('patient_schedule_row', component_property='editable'),
          Input('market_entry_row', 'value'),
          Input('patent_expiry_row', component_property='value'),
          Input('patient_population_row', component_property='value'),
          Input('market_penetration_row', component_property='value'),
          Input('market_size_increase_row', component_property='value'),
          Input('peak_sales_year_row', component_property='value'),
          Input('patient_adoption_rate_picker', component_property='value'),
          Input('first_year_adoption', 'value'),
          Input('long_term_adoption_rate', 'value'),
          Input('patient_schedule_eur', component_property='data'))
def patient_schedule_size_row(me, pe, pp, mp, nmi, psy, par, fya, ltar, data):
    if None in (me, pe) or "" in (me, pe):
        return [], [], False
    me, pe = int(me), int(pe)
    if (me < 2022 or me > 2050 or pe < 2022 or pe > 2050) and me >= pe:
        return [], [], False
    elif None in (pp, mp, nmi, par):
        df = pd.DataFrame()
        for i in range(me, pe + 1):
            df = df.join(pd.DataFrame({}))
        return [{"name": str(i), "id": str(i)} for i in range(me, pe + 1)], [], False
    elif par == "linear":
        if psy is None:
            return [{"name": str(i), "id": str(i)} for i in range(me, pe + 1)], [], False
        schedule = []
        current_pop = pp
        current_patients = 0
        for cy in range(me, pe + 1):
            current_pop += nmi
            max_patients = current_pop * (mp/100)
            if psy >= cy:
                patient_increase = round((max_patients - current_patients) / (psy - cy + 1), 0)
            else:
                patient_increase = round(nmi * (mp/100), 0)
            current_patients += patient_increase
            schedule.append(current_patients)
        df = pd.DataFrame(schedule).transpose()
        df.columns = [i for i in range(me, pe + 1)]
        return [{"name": str(i), "id": str(i)} for i in df.columns], df.to_dict('records'), False
    elif par == "logarithmic":
        if None in (fya, ltar):
            return [{"name": str(i), "id": str(i)} for i in range(me, pe + 1)], [], False
        schedule = []
        current_pop = pp
        current_patients = fya
        schedule.append(current_patients)

        for i, cy in enumerate(range(me + 1, pe + 1)):
            current_pop += nmi
            max_patients = current_pop * (mp/100)
            current_patients = round(min(max_patients, schedule[i] * (1 + (ltar/100))), 0)
            schedule.append(current_patients)
        df = pd.DataFrame(schedule).transpose()
        df.columns = [i for i in range(me, pe + 1)]
        return [{"name": str(i), "id": str(i)} for i in df.columns], df.to_dict('records'), False

    elif par == "custom":

        return [{"name": str(i), "id": str(i)} for i in range(me, pe + 1)], data, True


@callback(Output('first_year_adoption', 'style'),
          Output('first_year_adoption_label', 'hidden'),
          Output('long_term_adoption_rate', 'style'),
          Output('long_term_adoption_rate_label', 'hidden'),
          Output('peak_sales_year_us', 'style'),
          Output('peak_sales_year_us_label', 'hidden'),
          Output('peak_sales_year_eur', 'style'),
          Output('peak_sales_year_eur_label', 'hidden'),
          Output('peak_sales_year_row', 'style'),
          Output('peak_sales_year_row_label', 'hidden'),
          Input('patient_adoption_rate_picker', 'value'))
def enable_logarithmic_patient(adoption_schedule):
    if adoption_schedule == "logarithmic":
        return {'display': 'block'}, False, {'display': 'block'}, False, \
            {'display': 'none'}, True, {'display': 'none'}, True, \
            {'display': 'none'}, True
    elif adoption_schedule == "linear":
        return {'display': 'none'}, True, {'display': 'none'}, True, \
            {'display': 'block'}, False, {'disp lay': 'block'}, False, \
            {'display': 'block'}, False
    else:
        return {'display': 'none'}, True, {'display': 'none'}, True, \
            {'display': 'none'}, True, {'display': 'none'}, True, \
            {'display': 'none'}, True


@callback(Output('patient_schedule_us_chart_container', component_property='children'),
          Output('patient_schedule_us_chart_container', 'style'),
          Input('patient_schedule_us', 'data'),
          Input('toggle_patient_schedule_us', 'n_clicks'))
def update_patient_chart_us(data, clicks):
    df = pd.DataFrame(data).transpose()
    if df.empty or clicks % 2 == 0:
        return None, {'display': 'none'}

    fig = px.line(df)
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Patients'
    )
    return dcc.Graph(figure=fig), {'display': 'block'}


@callback(Output('patient_schedule_eur_chart_container', component_property='children'),
          Output('patient_schedule_eur_chart_container', 'style'),
          Input('patient_schedule_eur', 'data'),
          Input('toggle_patient_schedule_eur', 'n_clicks'))
def update_patient_chart_eur(data, clicks):
    df = pd.DataFrame(data).transpose()
    if df.empty or clicks % 2 == 0:
        return None, {'display': 'none'}

    fig = px.line(df)
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Patients'
    )
    return dcc.Graph(figure=fig), {'display': 'block'}


@callback(Output('patient_schedule_row_chart_container', component_property='children'),
          Output('patient_schedule_row_chart_container', 'style'),
          Input('patient_schedule_row', 'data'),
          Input('toggle_patient_schedule_row', 'n_clicks'))
def update_patient_chart_row(data, clicks):
    df = pd.DataFrame(data).transpose()
    if df.empty or clicks % 2 == 0:
        return None, {'display': 'none'}

    fig = px.line(df)
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Patients'
    )
    return dcc.Graph(figure=fig), {'display': 'block'}


# @callback(Output('add_asset_toast', 'is_open'),
#           Input('add_asset', 'n_clicks'))
# def open_toast(n):
#     if n == 1:
#         return True
#     return no_update


@callback(Output('add_asset_toast', 'is_open'),
          Output('add_asset_toast', 'header'),
          Output('add_asset_toast', 'children'),
          Output('add_asset_toast', 'icon'),
          Output('asset_name', 'value'),
          Output('success_probability', 'value'),
          Output('patent_expiry_us', 'value'),
          Output('patent_expiry_eur', 'value'),
          Output('patent_expiry_row', 'value'),
          Output('patient_population_us', 'value'),
          Output('patient_population_eur', 'value'),
          Output('patient_population_row', 'value'),
          Output('pricing_us', 'value'),
          Output('pricing_eur', 'value'),
          Output('pricing_row', 'value'),
          Output('market_entry_us', 'value'),
          Output('market_entry_eur', 'value'),
          Output('market_entry_row', 'value'),
          Output('phase_picker', 'value'),
          Output('patient_adoption_rate_picker', 'value'),
          Output('first_year_adoption', 'value'),
          Output('long_term_adoption_rate', 'value'),
          Output('market_penetration_us', 'value'),
          Output('market_penetration_eur', 'value'),
          Output('market_penetration_row', 'value'),
          Output('market_size_increase_us', 'value'),
          Output('market_size_increase_eur', 'value'),
          Output('market_size_increase_row', 'value'),
          Output('peak_sales_year_us', 'value'),
          Output('peak_sales_year_eur', 'value'),
          Output('peak_sales_year_row', 'value'),
          Output('development_milestone_table', 'data', allow_duplicate=True),
          Output('sales_milestone_table', 'data', allow_duplicate=True),
          Output('royalty_table', 'data', allow_duplicate=True),
          Input('add_asset', 'n_clicks'),
          State('asset_name', 'value'),
          State('success_probability', 'value'),
          State('patent_expiry_us', 'value'),
          State('patent_expiry_eur', 'value'),
          State('patent_expiry_row', 'value'),
          State('patient_population_us', 'value'),
          State('patient_population_eur', 'value'),
          State('patient_population_row', 'value'),
          State('pricing_us', 'value'),
          State('pricing_eur', 'value'),
          State('pricing_row', 'value'),
          State('patient_schedule_us', 'data'),
          State('patient_schedule_eur', 'data'),
          State('patient_schedule_row', 'data'),
          State('development_milestone_table', 'data'),
          State('sales_milestone_table', 'data'),
          State('royalty_table', 'data'),
          prevent_initial_call=True)
def add_asset(clicks, name, success, pe_us, pe_eur, pe_row, pp_us, pp_eur, pp_row,
              pricing_us, pricing_eur, pricing_row, ps_us, ps_eur, ps_row, dm, sm, r):
    print(name, success, pe_us, pe_eur, pe_row, pp_us, pp_eur, pp_row, pricing_us, pricing_eur, pricing_row)
    if None in [name, success, pe_us, pe_eur, pe_row, pp_us, pp_eur, pp_row, pricing_us, pricing_eur, pricing_row]:
        return True, "Missing Values", html.P("Please fill all data fields."), "danger", *([no_update] * 30)
    main_data = {
        'name': name,
        'success': success,
        'pe_us': pe_us,
        'pe_eur': pe_eur,
        'pe_row': pe_row,
        'pp_us': pp_us,
        'pp_eur': pp_eur,
        'pp_row': pp_row,
        'pricing_us': pricing_us,
        'pricing_eur': pricing_eur,
        'pricing_row': pricing_row,
    }
    main_table_id = assets_collection.insert_one(main_data).inserted_id

    patient_schedule_data = []
    for region, patient_schedule in [('US', ps_us), ('Europe', ps_eur), ('Rest of World', ps_row)]:
        region_data = patient_schedule
        for record in patient_schedule:
            record['AssetID'] = ObjectId(main_table_id)
            record['Region'] = region
        patient_schedule_data.extend(region_data)
    print(patient_schedule_data)
    patient_schedule_collection.insert_many(patient_schedule_data)

    dm_data = dm
    for record in dm_data:
        record['AssetID'] = ObjectId(main_table_id)
    print(dm_data)
    development_milestones_collection.insert_many(dm_data)

    sm_data = sm
    for record in sm_data:
        record['AssetID'] = ObjectId(main_table_id)
    print(sm_data)
    sales_milestones_collection.insert_many(sm_data)

    r_data = r
    for record in r_data:
        record['AssetID'] = ObjectId(main_table_id)
    print(r_data)
    royalty_tiers_collection.insert_many(r_data)

    return True, "Asset Added", html.P(f"Asset '{name}' has been successfully added to the database."), \
        "primary", *([""] * 27), *([[{}]] * 3)

