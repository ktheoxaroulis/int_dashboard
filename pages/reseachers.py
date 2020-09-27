import sys
sys.path.insert(0, '../')
import os
import dash_html_components as html
from utils import Header, make_dash_table
import dash_bootstrap_components as dbc
from db import df_finalorders
import dash_pivottable
from dash.dependencies import Input, Output


def create_layout(app):
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            # html.Div(
            #     [
            #     dash_pivottable.PivotTable(
            #     id="pvtable",
            #     data=df_finalorders,
            #     # cols=['OrderId'],
            #     # colOrder="key_a_to_z",
            #     # rows=['Division'],
            #     # rowOrder="key_a_to_z",
            #     # rendererName="Grouped Column Chart",
            #     # aggregatorName="Average",
            #     # vals=["AfterOrderDiscountValue"],
            #     # valueFilter={"Store": {"ΦΡΟΥΡΙΟ": True}},
            #
            #     # dash_pivottable.PivotTable(
            #     # id="table",
            #     # data=data,
            #     # cols=["Day of Week"],
            #     # colOrder="key_a_to_z",
            #     # rows=["Party Size"],
            #     # rowOrder="key_a_to_z",
            #     # rendererName="Grouped Column Chart",
            #     # aggregatorName="Average",
            #     # vals=["Total Bill"],
            #     # valueFilter={"Day of Week": {"Thursday": False}},
            # ),
            #
            #
            #         html.Div(id="pvoutput"),
            #   ],
            #className="sub-page", id="sub-page"
            # ),

            # html.Div(
            #      [
            #                  dash_pivottable.PivotTable(
            #                      id="pvtable",
            #                      data=df_finalorders,
            #                      cols=['OrderId'],
            #                      colOrder="key_a_to_z",
            #                      rows=['Division'],
            #                      rowOrder="key_a_to_z",
            #                      rendererName="Grouped Column Chart",
            #                      aggregatorName="Average",
            #                      vals=["AfterOrderDiscountValue"],
            #                      valueFilter={"Store": {"ΦΡΟΥΡΙΟ": True}},
            #                  ),
            #                 html.Div(id="pvoutput"),
            #     ],
            #     className="sub-page", id="sub-page"
            # ),
        ],
        className="page"
    )


