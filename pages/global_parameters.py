import dash
from utils import *
from dash import callback, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from bson.objectid import ObjectId

import settings

dash.register_page(
    __name__,
    path="/parameters",
    title="Global Parameters",
    name="Global Parameters",
    description="Displays global parameters affecting all assets",
)


def global_param_card():

    card = dbc.Card(
        dbc.CardBody(
            [
                html.P(id='placeholder'),
                html.H5("Display Parameters", className="card-title"),
                dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),
                html.Div(
                    [
                        html.Label("Base currency"),
                        dcc.Dropdown(
                            options=["AUD", "USD"],
                            multi=False,
                            placeholder="Select a base currency",
                            clearable=False,
                            id="base_currency",
                        ),
                    ],
                ),
                html.Div(
                    [
                        html.Label("Display currency"),
                        dcc.Dropdown(
                            options=["AUD", "USD"],
                            multi=False,
                            placeholder="Select a base currency",
                            clearable=False,
                            id="display_currency",
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("Alternate Bear Case (%)"),
                                dbc.Input(
                                    type="number",
                                    min=0,
                                    max=100,
                                    id="bear_case",
                                ),
                                dbc.FormFeedback("", type="valid"),
                                dbc.FormFeedback(
                                    f"it should be an integer number ≤ 100", type="invalid"
                                ),
                            ],
                        ),
                        dbc.Col(
                            [
                                html.Label("Alternate Bull Case (%)"),
                                dbc.Input(
                                    type="number",
                                    min=0,
                                    max=100,
                                    id="bull_case",
                                ),
                                dbc.FormFeedback("", type="valid"),
                                dbc.FormFeedback(
                                    f"it should be an integer number ≤ 100", type="invalid"
                                ),
                            ],
                        ),
                    ]
                ),
                dbc.Row(html.H5(children="Market Parameters")),
                dbc.Row(
                    [
                        # html.Hr(),
                        dbc.Label(
                            [
                                "Discount Rate (%)",
                                html.I(
                                    className="bi bi-info-square ms-2",
                                    id="discount_rate_i",
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.Input(
                                    type="number",
                                    min=0,
                                    max=100,
                                    id="discount_rate",
                                ),
                                dbc.FormFeedback("", type="valid"),
                                dbc.FormFeedback(
                                    f"it should be an integer number ≤ 100", type="invalid"
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Tooltip(
                            settings.discount_rate_tt,
                            target="discount_rate_i",
                        ),
                    ],
                    className="p-1",
                ),
                dbc.Row(
                    [
                        # html.Hr(),
                        dbc.Label(
                            [
                                "Tax Rate (%)",
                                html.I(
                                    className="bi bi-info-square ms-2",
                                    id="tax_rate_i",
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.Input(
                                    type="number",
                                    min=1,
                                    max=100,
                                    id="tax_rate",
                                ),
                                dbc.FormFeedback("", type="valid"),
                                dbc.FormFeedback(
                                    f"it should be an integer number ≤ 100", type="invalid"
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Tooltip(
                            settings.tax_rate_tt,
                            target="tax_rate_i",
                        ),
                    ],
                    className="p-1",
                ),
                dbc.Row(html.H5(children="Asset Parameters")),
                dbc.Row(
                    [
                        # html.Hr(),
                        dbc.Label(
                            [
                                "Generics Discount (%)",
                                html.I(
                                    className="bi bi-info-square ms-2",
                                    id="generics_discount_i",
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.Input(
                                    type="number",
                                    min=0,
                                    max=100,
                                    id="generics_discount",
                                ),
                                dbc.FormFeedback("", type="valid"),
                                dbc.FormFeedback(
                                    f"it should be an integer number ≤ 100", type="invalid"
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Tooltip(
                            settings.generics_discount_tt,
                            target="generics_discount_i",
                        ),
                    ],
                    className="p-1",
                ),
                dbc.Row(
                    [
                        # html.Hr(),
                        dbc.Label(
                            [
                                "Sales Margin (%)",
                                html.I(
                                    className="bi bi-info-square ms-2",
                                    id="sales_margin_i",
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.Input(
                                    type="number",
                                    min=0,
                                    max=100,
                                    id="sales_margin",
                                ),
                                dbc.FormFeedback("", type="valid"),
                                dbc.FormFeedback(
                                    f"it should be an integer number ≤ 100", type="invalid"
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Tooltip(
                            settings.sales_margin_tt,
                            target="sales_margin_i",
                        ),
                    ],
                    className="p-1",
                ),
            ]
        )
    )
    return card


def layout():
    page = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(global_param_card(), lg=7),
                ]
            ),
        ],
        class_name="mt-2",
        fluid="md",
    )
    return page


#  add all global params as outputs
@callback(Output('base_currency', component_property='value'),
          Output('display_currency', component_property='value'),
          Output('discount_rate', component_property='value'),
          Output('tax_rate', component_property='value'),
          Output('generics_discount', component_property='value'),
          Output('sales_margin', component_property='value'),
          Output('bear_case', component_property='value'),
          Output('bull_case', component_property='value'),
          Input('interval_db', component_property='n_intervals')
          )
def populate_global_params(n_intervals):
    df = pd.DataFrame(list(get_collection("global_params").find()))
    df['_id'] = df['_id'].astype(str)
    return df["base_currency"][0], df["display_currency"][0], df["discount_rate"][0], df["tax_rate"][0], \
        df["generics_discount"][0], df["sales_margin"][0], df["bear_scenario"][0], df["bull_scenario"][0]


@callback(Output('placeholder', component_property='n_clicks'),
          Input('base_currency', component_property='value'),
          Input('display_currency', component_property='value'),
          Input('discount_rate', component_property='value'),
          Input('tax_rate', component_property='value'),
          Input('generics_discount', component_property='value'),
          Input('sales_margin', component_property='value'),
          Input('bear_case', component_property='value'),
          Input('bull_case', component_property='value')
          )
def update_db(b_curr, d_curr, dr, tr, gd, sm, bear, bull):
    df = pd.DataFrame(list(get_collection("global_params").find()))
    df['_id'] = df['_id'].astype(str)
    id = df['_id'][0]
    print(b_curr, d_curr, dr, tr, gd, sm)
    get_collection("global_params").update_one(
        {"_id": ObjectId(id)},
        {"$set": {"base_currency": b_curr,
                  "display_currency": d_curr,
                  "discount_rate": dr, "tax_rate": tr,
                  "generics_discount": gd,
                  "sales_margin": sm,
                  "bear_scenario": bear,
                  "bull_scenario": bull,
                  }
         }
    )
    return None
