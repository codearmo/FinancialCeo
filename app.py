import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd

# Read the data from CSV
data = pd.read_csv("financial_database.csv")

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define some placeholder KPI cards
def generate_kpi_card(title, value, id, color):
    return dbc.Card([
        dbc.CardBody([
            html.H4(title, className="card-title"),
            html.H2(value, id=id, className="card-text")
        ])
    ], color=color, inverse=True, className="mb-4")


app.layout = dbc.Container([
    dcc.Store(id='data', data=data.to_dict('records')),  # Store the data
    dbc.Row([
        dbc.Col(html.H1("Financial CEO Dashboard", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col(generate_kpi_card("Total Revenue", "$0", "kpi-total-revenue", "primary"), width=3),
        dbc.Col(generate_kpi_card("Total Profit", "$0", "kpi-total-profit", "success"), width=3),
        dbc.Col(generate_kpi_card("Expenses", "$0", "kpi-expenses", "danger"), width=3),
        dbc.Col(generate_kpi_card("Cash Flow", "$0", "kpi-cash-flow", "info"), width=3),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='chart-1', style={"height": "400px"}), width=6),
        dbc.Col(dcc.Graph(id='chart-2', style={"height": "400px"}), width=6),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='chart-3', style={"height": "400px"}), width=6),
        dbc.Col(dcc.Graph(id='chart-4', style={"height": "400px"}), width=6),
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='data-table'), width=12)
    ])
], fluid=True)

# Define callbacks to update KPI cards with data
@app.callback(
    Output('kpi-total-revenue', 'children'),
    Input('data', 'data')
)
def update_kpi_total_revenue(data):
    df = pd.DataFrame(data)
    total_revenue = df['Revenue'].sum()
    return f"${total_revenue:,.2f}"

@app.callback(
    Output('kpi-total-profit', 'children'),
    Input('data', 'data')
)
def update_kpi_total_profit(data):
    df = pd.DataFrame(data)
    total_profit = df['Profit'].sum()
    return f"${total_profit:,.2f}"

@app.callback(
    Output('kpi-expenses', 'children'),
    Input('data', 'data')
)
def update_kpi_expenses(data):
    df = pd.DataFrame(data)
    total_expenses = df.filter(like='Expense', axis=1).sum(axis=0).sum()
    return f"${total_expenses:,.2f}"

@app.callback(
    Output('kpi-cash-flow', 'children'),
    Input('data', 'data')
)
def update_kpi_cash_flow(data):
    df = pd.DataFrame(data)
    cash_flow = (df['Cash Inflow'] - df['Cash Outflow'] ).sum()
    return f"${cash_flow:,.2f}"

@app.callback(
    Output('chart-1', 'figure'),
    Input('data', 'data')
)
def update_chart_1(data):
    df = pd.DataFrame(data)
    df['Cumulative 12 Month Revenue'] = df.Revenue.rolling(30).sum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Cumulative 12 Month Revenue'], mode='lines', name='Revenue'))
    fig.update_layout(title="Rolling 12 Month Revenue", template="plotly_dark", title_x=0.5)
    return fig

@app.callback(
    Output('chart-2', 'figure'),
    Input('data', 'data')
)
def update_chart_2(data):
    df = pd.DataFrame(data)
    fig = go.Figure()
    df['Cumulative rolling 30 Day Profit'] = df.Profit.rolling(30).sum()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Cumulative rolling 30 Day Profit'], mode='lines', name='Profit'))
    fig.update_layout(title="Profit Over Time", template="plotly_dark")
    return fig

@app.callback(
    Output('chart-3', 'figure'),
    Input('data', 'data')
)
def update_chart_3(data):
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index(df['Date'], inplace=True)
    monthly_profit = df.groupby(df.index.month)['Profit'].sum()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    fig = go.Figure([go.Bar(x=months, y=monthly_profit)])
    fig.update_layout(title="Monthly Profit", template="plotly_dark")
    return fig

@app.callback(
    Output('chart-4', 'figure'),
    Input('data', 'data')
)
def update_chart_4(data):
    df = pd.DataFrame(data)
    expenses = df.filter(like='Expense', axis=1).sum()
    fig = go.Figure(data=[go.Pie(labels=expenses.index, values=expenses)])
    fig.update_layout(title="Expense Distribution", template="plotly_dark")
    return fig


@app.callback(
    Output('data-table', 'children'),
    Input('data', 'data')
)
def update_data_table(data):
    df = pd.DataFrame(data)[::-1]
    table_header = [
        html.Thead(html.Tr([html.Th(col) for col in df.columns]))
    ]
    rows = []
    for _, row in df.head(12).iterrows():
        rows.append(html.Tr([html.Td(val) for val in row]))
    table_body = [html.Tbody(rows)]
    table = dbc.Table(table_header + table_body, bordered=True, dark=True, hover=True, striped=True)
    return table

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
