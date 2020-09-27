# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import os
import plotly.express as px

import db
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc


# external JavaScript files
external_scripts = [
"https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css",
"https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js",
"https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"
]

from pages import (
    overview,
    food,
    beverage,
    reseachers,
)

app = dash.Dash(
    __name__, external_scripts=external_scripts,external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
app.config.suppress_callback_exceptions = True

app.title = 'JWBF Dashboard'
server = app.server


# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")] )
#
# Update page
@app.callback(Output("tabs", "children"), [Input("url", "pathname")])
def display_menustyle(pathname):
    tabs = [
        dcc.Link("OVERVIEW", href="/report/overview",className="tab first"),
        dcc.Link("FOOD", href="/report/food",className="tab"),
        dcc.Link("BEVERAGE", href="/report/beverage",className="tab"),
        dcc.Link("RESEARCH", href="/report/reseachers",className="tab"),

    ]

    if pathname == "/report/food":
        tabs[1] = dcc.Link(
            dcc.Markdown("**&#9632 FOOD**"),
            href="/report/food",className="tab"
        )
        return tabs
    elif pathname == "/report/beverage":
        tabs[2] = dcc.Link(
            dcc.Markdown("**&#9632 BEVERAGE**"),
            href="/report/beverage",className="tab"
        )
        return tabs
    elif pathname == "/report/reseachers":
        tabs[3] = dcc.Link(
            dcc.Markdown("**&#9632 RESEARCH**"),
            href="/report/reseachers",className="tab"
        )
        return tabs
    else:
        tabs[0] = dcc.Link(
            dcc.Markdown("**&#9632 OVERVIEW**"),
            href="/report/Overview",className="tab first"
        )
        return tabs

# Update page
@app.callback(Output("page-content", "children") , [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/report/food":
        return food.create_layout(app)
    elif pathname == "/report/beverage":
        return beverage.create_layout(app)
    elif pathname == "/report/reseachers":
        return reseachers.create_layout(app)
    else:
        return overview.create_layout(app)


def get_all_file_paths(directory):
    # initializing empty file paths list
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    return file_paths

@app.callback( Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("bclose", "n_clicks"), Input("bclose2", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, n3, is_open):
    if n1 or n2 or  n3:
        return not is_open
    return is_open



@app.callback(Output('las-learn2', 'style'),[Input('las-learn', 'n_clicks')])
def update_style(click):
    if click==None:
       return {'display': 'none'}
    if click%2==0:
       return {'display': 'none'}
    else:
        return {'display': 'block'}


@app.callback(
    Output("pvoutput", "children"),
    [
        Input("pvtable", "cols"),
        Input("pvtable", "rows"),
        Input("pvtable", "rowOrder"),
        Input("pvtable", "colOrder"),
        Input("pvtable", "aggregatorName"),
        Input("pvtable", "rendererName"),
    ],
)
def display_props(cols, rows, row_order, col_order, aggregator, renderer):
    return [
        html.P(str(cols), id="columns"),
        html.P(str(rows), id="rows"),
        html.P(str(row_order), id="row_order"),
        html.P(str(col_order), id="col_order"),
        html.P(str(aggregator), id="aggregator"),
        html.P(str(renderer), id="renderer"),
    ]


# Radio -> multi
@app.callback(
    Output("store_statues", "value"), [Input("store_selector", "value")]
)
def display_status(selector):
    if selector == "all":
        return list(db.getunique('Store'))
    elif selector == "custom":
        return []



# Selectors -> orders
@app.callback(
    Output("orders", "children"),
    [
    Input("store_statues", "value"),
    dash.dependencies.Input('my-date-picker-range', 'start_date'),
    dash.dependencies.Input('my-date-picker-range', 'end_date')
    ],
)
def update_orders(store_statues,start_date,end_date):
    return db.filter_dataframe(db.return_orders(),store_statues,start_date, end_date)["orders"].sum()

# Selectors -> sales
@app.callback(
    Output("sales", "children"),
    [
    Input("store_statues", "value"),
    dash.dependencies.Input('my-date-picker-range', 'start_date'),
    dash.dependencies.Input('my-date-picker-range', 'end_date')
    ],
)
def update_sales(store_statues,start_date,end_date):
    return "{:0,.2f}".format(db.filter_dataframe(db.return_sales(),store_statues,start_date, end_date)["sales"].sum())


# Selectors -> quantity
@app.callback(
    Output("quantity", "children"),
    [
    Input("store_statues", "value"),
    dash.dependencies.Input('my-date-picker-range', 'start_date'),
    dash.dependencies.Input('my-date-picker-range', 'end_date')
    ],
)
def update_quantity(store_statues,start_date,end_date):
    return db.filter_dataframe(db.return_quantity(),store_statues,start_date, end_date)["quantity"].sum()

# Selectors -> salescweek
@app.callback(
    Output("salescweek", "children"),
    [
    Input("store_statues", "value"),
    ],
)
def update_salescweek(store_statues):
    return "{:0,.2f}".format(db.filter_dataframe(db.return_sales(),store_statues,db.startweeks, db.endweeks)["sales"].sum())

# Selectors -> saleslweek
@app.callback(
    Output("saleslweek", "children"),
    [
    Input("store_statues", "value"),
    ],
)
def update_saleslweek(store_statues):
    return "{:0,.2f}".format(db.filter_dataframe(db.return_sales(),store_statues,db.startlweeks, db.ltoday.strftime('%Y-%m-%d'))["sales"].sum())


# Selectors -> salescmonth
@app.callback(
    Output("salescmonth", "children"),
    [
    Input("store_statues", "value"),
    ],
)
def update_salescmonth(store_statues):
    return "{:0,.2f}".format(db.filter_dataframe(db.return_sales(),store_statues,db.first_day_of_month, db.last_day_of_month)["sales"].sum())

# Selectors -> salesclonth
@app.callback(
    Output("saleslmonth", "children"),
    [
    Input("store_statues", "value"),
    ],
)
def update_saleslmonth(store_statues):
    return "{:0,.2f}".format(db.filter_dataframe(db.return_sales(),store_statues,db.first_day_of_lmonth, db.ltoday.strftime('%Y-%m-%d'))["sales"].sum())


# Selectors -> salescquarter
@app.callback(
    Output("salescquarter", "children"),
    [
    Input("store_statues", "value"),
    ],
)
def update_salescquarter(store_statues):
    return "{:0,.2f}".format(db.filter_dataframe(db.return_sales(),store_statues,db.first_day_of_the_quarter, db.last_day_of_the_quarter)["sales"].sum())

# Selectors -> saleslquarter
@app.callback(
    Output("saleslquarter", "children"),
    [
    Input("store_statues", "value"),
    ],
)
def update_saleslquarter(store_statues):
    return "{:0,.2f}".format(db.filter_dataframe(db.return_sales(),store_statues,db.first_day_of_the_lquarter,  db.ltoday.strftime('%Y-%m-%d'))["sales"].sum())


# Selectors -> salescyear
@app.callback(
    Output("salescyear", "children"),
    [
    Input("store_statues", "value"),
    ],
)
def update_salescyear(store_statues):
    return "{:0,.2f}".format(db.filter_dataframe(db.return_sales(),store_statues,db.starting_day_of_cyear, db.ending_day_of_cyear)["sales"].sum())

# Selectors -> saleslyear
@app.callback(
    Output("saleslyear", "children"),
    [
    Input("store_statues", "value"),
    ],
)
def update_saleslyear(store_statues):
    return "{:0,.2f}".format(db.filter_dataframe(db.return_sales(),store_statues,db.starting_day_of_lyear, db.ltoday.strftime('%Y-%m-%d'))["sales"].sum())



@app.callback(
    dash.dependencies.Output('main_graph', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     Input("store_statues", "value"),
     ])
def update_y_timeseries(xaxis_column_name,store_statues):
    df = db.return_meltdf(store_statues)
    fig = px.line(df[df['variable'] == xaxis_column_name], x='WeekofYear', y='value', color='Year',line_group='Year')
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(type='linear')
    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text="title")
    fig.update_layout(height=500, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})
    return fig



if __name__ == "__main__":
    app.run_server(debug=False)