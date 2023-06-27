import dash
import pymongo
from dash import callback, html, dcc, dash_table
import plotly.express as px
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from utils import *

dash.register_page(
    __name__,
    path="/assets",
    title="Assets",
    name="Assets",
    description="Displays all assets",
)

assets_df = get_collection_as_df("assets")
assets_collection = get_collection("assets")
patient_schedule_collection = get_collection("patients_schedule")
development_milestones_collection = get_collection("development_milestones")
sales_milestones_collection = get_collection("sales_milestones")
royalty_tiers_collection = get_collection("royalty_tiers")


asset_selector = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Search Database", className="card-title"),
            dcc.Dropdown(
                options=list(assets_df["name"]),
                multi=False,
                placeholder="Select an asset",
                clearable=True,
                id="asset_selector",
            ),
        ]
    )
)


asset_info_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Asset Properties"),
            html.Div(id="asset_properties_table"),
            html.H5("Market Details"),
            html.Div(id="market_details_table"),
            html.H5("Pricing"),
            html.Div(id="pricing_table"),
        ]
    )
)

patient_schedule_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H5("Patient Schedule"),
                dcc.Dropdown(
                    options=["US", "Europe", "Rest of World"],
                    multi=True,
                    placeholder="Select regions",
                    id="patient_region_selector",
                ),
                html.Div(id="patient_schedule_graph_container"),
            ]
        )
    ]
)


licensing_card = dbc.Card(
    [
        dbc.CardBody(
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
                                            style_table={'overflowX': 'scroll'},
                                            data=[{}],
                                            editable=True,
                                            style_cell={'whiteSpace': 'normal'},
                                            id="development_milestone_display_table",

                                        )
                                    ],
                                    style={'display': 'none'},
                                    id="development_milestone_display_details"
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
                                            style_table={'overflowX': 'scroll'},
                                            data=[{}],
                                            editable=True,
                                            style_cell={'whiteSpace': 'normal'},
                                            id="sales_milestone_display_table",

                                        )
                                    ],
                                    style={'display': 'none'},
                                    id="sales_milestones_display_details"
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
                                            style_table={'overflowX': 'scroll'},
                                            data=[{}],
                                            editable=True,
                                            style_cell={'whiteSpace': 'normal'},
                                            id="royalty_display_table",

                                        )
                                    ],
                                    style={'display': 'none'},
                                    id="royalty_display_details"
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


def layout():

    page = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(asset_selector),
                ]
            ),
            dbc.Row(
                [
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(patient_schedule_card, width=8),
                                    dbc.Col(asset_info_card, width=4)
                                ]
                            ),
                        ],
                        id="asset_and_patient_info",
                        style={"display": "none"},
                    ),
                ]
            ),
            dbc.Row(
                [
                    licensing_card,
                ]
            )
        ]
    )
    return page


@callback(Output('asset_properties_table', 'children'),
          Output('market_details_table', 'children'),
          Output('pricing_table', 'children'),
          Input('asset_selector', 'value'),
          config_prevent_initial_callbacks=True)
def update_asset_info_card(asset_name):
    asset_document = assets_collection.find_one({'name': asset_name})

    if asset_document:
        # Extract asset properties
        success = asset_document.get('success')
        pe_us = asset_document.get('pe_us')
        pe_eur = asset_document.get('pe_eur')
        pe_row = asset_document.get('pe_row')

        # Generate asset properties table as DataTable
        asset_properties_table = dash_table.DataTable(
            data=[
                {'Property': 'Probability for Success', 'Value': f"{success}%"},
                {'Property': 'US', 'Value': pe_us},
                {'Property': 'Europe', 'Value': pe_eur},
                {'Property': 'Rest of World', 'Value': pe_row}
            ],
            style_table={'overflowX': 'scroll'},
            columns=[
                {'name': 'Property', 'id': 'Property'},
                {'name': 'Patent Expiry', 'id': 'Value'}
            ]
        )

        # Extract market details
        pp_us = asset_document.get('pp_us')
        pp_eur = asset_document.get('pp_eur')
        pp_row = asset_document.get('pp_row')

        # Generate market details table as DataTable
        market_details_table = dash_table.DataTable(
            data=[
                {'Region': 'US', 'Patient Population': pp_us},
                {'Region': 'Europe', 'Patient Population': pp_eur},
                {'Region': 'Rest of World', 'Patient Population': pp_row}
            ],
            style_table={'overflowX': 'scroll'},
            columns=[
                {'name': 'Region', 'id': 'Region'},
                {'name': 'Patient Population', 'id': 'Patient Population'}
            ]
        )

        # Extract pricing details
        pricing_us = asset_document.get('pricing_us')
        pricing_eur = asset_document.get('pricing_eur')
        pricing_row = asset_document.get('pricing_row')

        # Generate pricing table as DataTable
        pricing_table = dash_table.DataTable(
            data=[
                {'Region': 'US', 'Pricing': pricing_us},
                {'Region': 'Europe', 'Pricing': pricing_eur},
                {'Region': 'Rest of World', 'Pricing': pricing_row}
            ],
            style_table={'overflowX': 'scroll'},
            columns=[
                {'name': 'Region', 'id': 'Region'},
                {'name': 'Pricing', 'id': 'Pricing', "type": 'numeric', "format": money}
            ]
        )

        return asset_properties_table, market_details_table, pricing_table

    return None, None, None


@callback(Output('asset_and_patient_info', 'style'),
          Input('asset_selector', 'value'))
def display_asset_patient_info(asset_name):
    if asset_name is not None:
        return {"display": "block"}
    else:
        return {'display': 'none'}


@callback(Output('patient_schedule_graph_container', 'children'),
          Input('patient_region_selector', 'value'),
          Input('asset_selector', 'value'))
def update_patient_schedule_graph(regions, asset_name):
    asset = assets_collection.find_one({'name': asset_name})
    if not regions:
        return None

    if asset:
        asset_id = asset['_id']
        patients_by_year = {}
        for region in regions:
            patients = patient_schedule_collection.find({'AssetID': asset_id, 'Region': region})
            for patient in patients:
                for year, patient_count in patient.items():
                    if year != '_id' and year != 'AssetID' and year != 'Region':
                        year = int(year)
                        patient_count = int(patient_count)

                        if year in patients_by_year:
                            patients_by_year[year] += patient_count
                        else:
                            patients_by_year[year] = patient_count

        years = sorted(patients_by_year.keys())
        patients_total = [patients_by_year[year] for year in years]

        data = pd.DataFrame({'Year': years, 'Patients': patients_total}).set_index("Year")
        fig = px.line(data)
        fig.update_layout(
            title="Total Patients by Year and Region",
            xaxis_title="Year",
            yaxis_title="Total Patients"
        )

        return dcc.Graph(figure=fig)

    return dash.no_update


@callback(Output('development_milestone_display_table', 'data'),
          Output('sales_milestone_display_table', 'data'),
          Output('royalty_display_table', 'data'),
          Output('development_milestone_display_details', 'style'),
          Output('sales_milestones_display_details', 'style'),
          Output('royalty_display_details', 'style'),
          Input('asset_selector', 'value'),
          )
def update_licensing_details(asset_name):
    asset_data = assets_collection.find_one({"name": asset_name})

    if asset_name is None:
        return [{}], [{}], [{}], dash.no_update, dash.no_update, dash.no_update

    asset_id = asset_data["_id"]

    dm_table = development_milestones_collection.find({"AssetID": asset_id})
    sm_table = sales_milestones_collection.find({"AssetID": asset_id})
    r_table = royalty_tiers_collection.find({"AssetID": asset_id})

    dm_data = [{col: record[col] for col in record if col not in ["AssetID", "_id"]} for record in dm_table]
    sm_data = [{col: record[col] for col in record if col not in ["AssetID", "_id"]} for record in sm_table]
    r_data = [{col: record[col] for col in record if col not in ["AssetID", "_id"]} for record in r_table]

    print(r_table)

    return dm_data, sm_data, r_data, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}
