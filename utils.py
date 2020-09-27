import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

def Header(app):
   return html.Div([get_header(app), get_menu()])

def Footer(app):
   return html.Div([get_footer(app)])

def get_header(app):
    header = html.Div(
        [
            html.Div(
                id="header",
                className="header margrow row",
                children=[
                    html.Img( src=app.get_asset_url("logo.png" ),className="logo"),
                    html.A(id="controls", children=[
                        html.Button("Print PDF", className="mbutton button no-print print", id="las-print"),
                    ],
                           ),
                  ],
            ),
        ],
    )
    return header

def get_menu():
    menu = dbc.Navbar(
                id="tabs",
                className="row all-tabs",
            #     children=[
            #         dbc.NavItem( dcc.Link("OVERVIEW", href="/report/overview",className="tab first")),
            #         dbc.NavItem( dcc.Link("FOOD", href="/report/food",className="tab")),
            #         dbc.NavItem( dcc.Link("BEVERAGE", href="/report/beverage",className="tab")),
            #         dbc.NavItem( dcc.Link("RESEARCH", href="/report/reseachers",className="tab")),
            #     ],
             )
    return menu

def get_footer(app):
    header =  html.Div(
                        [
                            html.H5("Dashboard Summary",className = "footerTitle"),
                            html.Br([]),
                            html.P( "This Dashboard is an web-app to provide insights for JWBF group",className = "footerTxt"),
                            html.Button("Learn More", className="lbutton button no-print print", id="las-learn"),
                            html.Div(id="las-learn2", children=[html.P( "The Data collected for this Dashboard  are a combination of :",className = "footerTitle2"), html.P("1) InOrder data ",className = "footerTitle2"), html.P("2) Weather web data",className = "footerTitle2"), html.P("3) Company's calendar events",className = "footerTitle2") ,
                            html.P("The dashboard is organized in 3 distinct categories, namely:" ,className = "footerTitle2"),
                            html.Div([html.P("1. Overview of sales:",style={"font-weight": "600"}), html.P("1"),
                            html.P("2. Data related to Food:",style={"font-weight": "600"}),html.P(" 2 "),
                            html.P(" 3. Data related to Beverage: ",style={"font-weight": "600"}), html.P("3")
                                    ],className="footerTxt2",)
                                                                ])
                        ],
                        className="footer",
                    )

    return header

def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table
