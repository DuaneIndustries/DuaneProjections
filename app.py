import dash
import dash_bootstrap_components.themes
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import pandas as pd
import plotly
import plotly.express as px
import dash_bootstrap_components as dbc


exp = pd.read_csv("https://raw.githubusercontent.com/DuaneIndustries/DuaneProjections/main/Expense2022ForGraphs.csv")
rev = pd.read_csv("https://raw.githubusercontent.com/DuaneIndustries/DuaneProjections/main/revTT2.csv")
PJ = pd.read_csv("https://raw.githubusercontent.com/DuaneIndustries/DuaneProjections/main/ProjectHours2.csv")
print(PJ.head(5))



rev['Revenue'] = rev['Revenue'].astype('float')
rev['Expenses'] = rev['Expenses'].astype('float')
rev['Purchases/Debts'] = rev['Purchases/Debts'].astype('float')
rev['Income available to Shareholders'] = rev['Income available to Shareholders'].astype('float')
exp['Total'] = exp['Total'].astype('float')

PJ['Techs'] = PJ['Techs'].astype('int')
PJ['avg Tech rate'] = PJ['avg Tech rate'].astype('float')

PJ['Billable Hours Per week'] = PJ['Billable Hours Per week'].astype('float')
PJ['Annual Rev Proj.'] = PJ['Annual Rev Proj.'].astype('float')
PJ['Project Hours - YTD'] = PJ['Project Hours - YTD'].astype('float')


app = dash.Dash(__name__,external_stylesheets=[dash_bootstrap_components.themes.SANDSTONE],
              meta_tags=[{'name':'viewport',
                          'content': 'width=device-width, intial-scale=1.0'}]
                )

server = app.server

# LAYOUT
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Duane & Company 2022-2023 Projections',
                        className='text-center, mb-4'),
                width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='my-dpdn', multi=True, value =['2022-ACT','2023-PROJ','2023-YTD'],
                     options=[{'label': x, 'value': x}
                            for x in rev['Year'].unique()]),
            dcc.Graph(id='rev-fig',figure={})
        ], width={'size' : 12}),
    # dbc.Col([
    #     dcc.Dropdown(id='my-dpdn2', multi=True, value =['AMZN', 'TSLA'],
    #                  options=[{'label': x, 'value': x}
    #                           for x in sorted(df['Symbols'].unique())]),
    #     dcc.Graph(id='line-fig2', figure={})
    #
    # ], width={'size' : 6})
]),
    dbc.Row([
        dbc.Col([
            dcc.Checklist(id='my-checklist', value=['COGS','Labor','Meals','Travel','Addtl Exp','Bad Debt','Rent','Vehicle','Net Income'],
                inline=True,
                className="mx-1",
                options=[{'label': x, 'value': x}
                            for x in exp['ExpenseCat'].unique()]),
            dcc.Graph(id='pie-fig',figure={})
        ], width={'size' : 6}),
        dbc.Col([
            html.Br(),
            html.Label(['Number of Techs'], style={'font-weight': 'bold'}),
             dcc.Dropdown(
                id='x-axis-dropdown',
                options=[{'label': i, 'value': i} for i in PJ['Techs'].unique()],
                value=PJ['Techs'].iloc[0]),
        dcc.Graph(id='hours-bar',figure={})
        ], width = {'size': 6})

# dcc.Dropdown(id='my-dpdn3', multi=False, value =['Techs'],
#                      options=[{'label': x, 'value': x}
#                             for x in PJ['Techs'].unique()]),
#             dcc.Graph(id='hours-bar',figure={})
#         ], width={'size' : 6}),
            # dcc.Dropdown(
            #     id='x-axis-dropdown',
            #     options=[{'label': i, 'value': i} for i in PJ.columns],
            #     value='Techs'),
            # # dcc.Dropdown(id='x-axis-dropdown', multi=False, value=[4],
            # #              options=[{'label': x, 'value': x}
            # #                       for x in PJ['Techs'].unique()]),
            # dcc.Dropdown(
            #     id='y-axis-dropdown',
            #     options=[{'label': i, 'value': i} for i in PJ.columns if i != 'Techs'],
            #     value='Billable Hours Per week'),

            # dcc.Dropdown(id='y-axis-dropdown', multi=False, value=[96],
            #              options=[{'label': x, 'value': x}
            #                       for x in PJ['avg Tech rate'].unique()]),
            # dcc.Graph(id='hours-bar',figure={})
        # ], width={'size' : 6}),
]),
])

# Callback section: connecting the components
# ************************************************************************
# Line chart - Single
@app.callback(
    Output('rev-fig', 'figure'),
    Input('my-dpdn', 'value')
)
def update_graph(year_slctd):
    dff = rev[rev["Year"]==year_slctd]
    barchart=px.bar(
            data_frame=dff,
            x=["Expenses","Purchases/Debts","Income available to Shareholders"],
            y="Year",
            title='Revenue Projections',
            orientation='h',
            barmode='stack',
            )
    return (barchart)

# Pie Chart - Expense
@app.callback(
    Output('pie-fig', 'figure'),
    Input('my-checklist', 'value')
)
def update_graph(cat_slctd):
    dff = exp[exp['ExpenseCat'].isin(cat_slctd)]
    pie1 = px.pie(dff, values='Total', names='ExpenseSubCat', title='Expenses 2022' )
    return (pie1)


# PROJECT HOURS BAR
@app.callback(
    Output('hours-bar', 'figure'),
    Input('x-axis-dropdown', 'value')
)

def update_figure(selected_x_value):
    filtered_df = PJ[PJ['Techs'] == selected_x_value]
    fig = px.bar(filtered_df, x='Techs', y=['Billable Hours Per week','Project Hours - YTD'],facet_col_spacing=1, title='2023 Project Hours Needed vs. YTD', barmode='overlay', hover_data=["Annual Rev Proj."])
    return fig


# def update_graph(Techs_slctd):
#     dff = PJ[PJ["Techs"]==Techs_slctd]
#     barchart=px.bar(
#             data_frame=dff,
#             x="Techs",
#             y=["Billable Hours Per week"],
#             title='Revenue Projections',
#             orientation='v',
#             barmode='stack',
#             )
#     return (barchart)

if __name__ == '__main__' :
    app.run_server(debug=True)
