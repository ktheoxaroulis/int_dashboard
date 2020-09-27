import sys
sys.path.insert(0, '../')

import dash_core_components as dcc
import dash_html_components as html
from utils import Header,Footer
import db
from datetime import timedelta

def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [

                html.Div(
                    [
                        dcc.DatePickerRange(
                            id='my-date-picker-range',
                            min_date_allowed=min(db.df_finalorders['OrderDate']),
                            max_date_allowed=(db.today + timedelta(days=+1)).strftime('%Y-%m-%d'),
                            initial_visible_month=max(db.df_finalorders['OrderDate']),
                            start_date=max(db.df_finalorders['OrderDate']),
                            end_date= max(db.df_finalorders['OrderDate']) ,
                            display_format='DD MM YYYY',
                            minimum_nights=0,
                            first_day_of_week=1,
                            calendar_orientation ='vertical',
                        ),

                        html.P("Store:", className="control_label"),
                        dcc.RadioItems(
                            id="store_selector",
                            options=[
                                {"label": "All ", "value": "all"},
                                {"label": "Customize ", "value": "custom"},
                            ],
                            value="all",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        dcc.Dropdown(
                            id="store_statues",
                            options=[{'label': i, 'value': i} for i in db.getunique('Store')],
                            multi=True,
                            value=list(db.getunique('Store')),
                            className="dcc_control",
                        ),
                        ],
                    className="pretty_container two columns no-print",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="orders"),
                                     html.P("No. of Orders")],
                                    id="orders",
                                    className="mini_container"
                                ),
                                html.Div(
                                    [html.H6(id="sales"),
                                     html.P("Sales")],
                                    id="sales",
                                    className="mini_container"
                                ),
                                html.Div(
                                    [
                                    html.H6(id="quantity" ),
                                    html.P("Quantity")],
                                    id="quantity",
                                    className="mini_container",
                                ),

                            ],
                            id="info-container",
                            className="row container-display", style = {"justify-content": "space-between"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="salescweek"), html.P("Current Week Sales"),html.H6(id="saleslweek"),html.P("vs Last Year Sales")],
                                    id="salescweek",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="salescmonth"), html.P("Current Month Sales"),html.H6(id="saleslmonth"),html.P("vs Last YearSales")],
                                    id="salescmonth",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="salescquarter"), html.P("Current Quarter Sales"),html.H6(id="saleslquarter"),html.P("vs Last YearSales")],
                                    id="salescquarter",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="salescyear"), html.P("Current Year Sales"),html.H6(id="saleslyear"),html.P("vs Last YearSales")],
                                    id="salescyear",
                                    className="mini_container",
                                ),

                            ],
                            id="info-container2",
                            className="row container-display", style={"justify-content": "space-between"},
                        ),
                    ],
                    id="right-column",
                    className="ten columns",
                ),



        ],
            className="row flex-display indicators",
            ),

            html.Div(
                [
                    html.Div([
                        dcc.Dropdown(
                            id='crossfilter-xaxis-column',
                            options=[{'label': i, 'value': i} for i in ['Sales', 'Orders', 'Quantity', 'Avg Sales per Order', 'Avg Item per Order', 'Avg Sales per Item']],
                            value='Sales'
                        ),
                        dcc.Graph(id="main_graph")],
                        className="pretty_container seven columns",
                    ),
                    html.Div(
                        [dcc.Graph(id="individual_graph1"),
                         dcc.Graph(id="individual_graph2")],
                        className="pretty_container five columns",
                    ),
                ],
                className="row flex-display",
            ),
            html.Div([Footer(app)]),

        ],
        className="page",
    )


