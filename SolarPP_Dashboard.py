import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the CSV data into a DataFrame
data_path = '/Users/carloscarvalho/Downloads/first_dashboard.csv'
df = pd.read_csv(data_path)

# Convert the 'data' column to datetime
df['data'] = pd.to_datetime(df['data'])

# Extract the month and year from the 'data' column
df['month_year'] = df['data'].dt.to_period('M')

# cleaning '%', 'R$',',' and converting to float
df['cota_energia'] = df['cota_energia'].str.replace('%','').astype(float)
df['valor_pago'] = df['valor_pago'].str.replace('R$','').str.replace(',','.').astype(float)
df['custo_kWh'] = df['custo_kWh'].str.replace('R$','').str.replace(',','.').astype(float)

# creating column Economia:
df['economia'] = df['energia_inj'] * df['custo_kWh']
# print(df)
# df.info()

# Initialize the Dash application
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Interactive Dashboard with Plotly and Dash"),

    # Date range filter with custom display format (month and year)
    dcc.DatePickerRange(
        id='date-range',
        start_date=df['data'].min(),
        end_date=df['data'].max(),
        display_format='MMM YYYY',
    ),

    # Container for charts and filter (in a separate row)
    html.Div([
        # Container for the charts (in the same row)

            # Combined area and bar chart to display 'energia_gerada' as an area and 'consumo' as bars
            dcc.Graph(id='combined-chart', style={'display': 'inline-block', 'width': '49%'}),
            # Doughnut chart to display the relationship between 'unidade' and 'consumo'
            dcc.Graph(id='doughnut-chart', style={'display': 'inline-block', 'width': '49%'}),
        ]),

        # Container for scoreboards
        html.Div([
            # Scoreboard box to display the average of the sum of 'consumo' by month
            html.Div([
                html.P("Average Monthly Consumo:"),
                html.H2(id='average-box-consumo', className='box')
            ], style={'text-align': 'center', 'display': 'inline-block', 'width': '49%'}),

            # Scoreboard box to display the average of the sum of 'energia_gerada' by month
            html.Div([
                html.P("Average Monthly Energia Gerada:"),
                html.H2(id='average-box-energia', className='box')
            ], style={'text-align': 'center', 'display': 'inline-block', 'width': '49%'}),
        ]),

        # Container for area and donut charts (in the same row)
        html.Div([
            # Container for the new area chart
            dcc.Graph(id='saldo-credito-chart', style={'display': 'inline-block', 'width': '49%'}),
            # Container for the new donut chart
            dcc.Graph(id='donut-chart-credito-mes', style={'display': 'inline-block', 'width': '49%'}),
        ]),
        # Container for 2 bars charts (in the same row)
        html.Div([
            # Container for the Despesa bar chart
            dcc.Graph(id='gasto-energia-chart', style={'display': 'inline-block', 'width': '49%'}),
            # Container for the Economia bar chart
            dcc.Graph(id='economia-chart', style={'display': 'inline-block', 'width': '49%'}),
        ]),
        # Container for cards medias de gasto , economia
        html.Div([
            # Scoreboard box to display the average of the sum of 'gasto' by month
            html.Div([
                html.P("Gasto Mensal Médio:"),
                html.H2(id='average-box-gasto', className='box')
            ], style={'text-align': 'center', 'display': 'inline-block', 'width': '49%'}),

            # Scoreboard box to display the average of the sum of 'economia' by month
            html.Div([
                html.P("Economia Mensal Média:"),
                html.H2(id='average-box-economia', className='box')
            ], style={'text-align': 'center', 'display': 'inline-block', 'width': '49%'}),
        ]),

        # Container for cards medias de gasto , economia POR UNIDADE
        html.Div([
            # Scoreboard box to display the average of the sum of 'gasto' by month by 'Unidade'
            html.Div([
                html.P("Carlos:"),
                html.H2(id='average-box-gasto-unid-0', className='box'),
            ], style={'text-align': 'center', 'display': 'inline-block', 'width': '12%'}),
            html.Div([
                html.P("Ju & Rafael:"),
                html.H2(id='average-box-gasto-unid-1', className='box'),
            ], style={'text-align': 'center', 'display': 'inline-block', 'width': '12%'}),
            html.Div([
                html.P("Luciana:"),
                html.H2(id='average-box-gasto-unid-2', className='box'),
            ], style={'text-align': 'center', 'display': 'inline-block', 'width': '12%'}),
            html.Div([
                html.P("Valdione"),
                html.H2(id='average-box-gasto-unid-3', className='box'),
            ], style={'text-align': 'center', 'display': 'inline-block', 'width': '12%'}),

            # Scoreboard box to display the average of the sum of 'economia' by month by 'Unidade'
            html.Div([
                html.P("Carlos:"),
                html.H2(id='average-box-economia-unid-0', className='box')
            ], style={'text-align': 'center', 'display': 'inline-block', 'width': '12%'}),
            html.Div([
                html.P("Ju & Rafael:"),
                html.H2(id='average-box-economia-unid-1', className='box')
            ], style={'text-align': 'center', 'display': 'inline-block', 'width': '12%'}),
            html.Div([
                html.P("Luciana:"),
                html.H2(id='average-box-economia-unid-2', className='box')
            ], style={'text-align': 'center', 'display': 'inline-block', 'width': '12%'}),
            html.Div([
                html.P("Valdione:"),
                html.H2(id='average-box-economia-unid-3', className='box')
            ], style={'text-align': 'center', 'display': 'inline-block', 'width': '12%'}),
        ]),


])


# Define a callback to update the combined chart, doughnut chart, average boxes, the new area chart, and the Cards (scoreboards) based on the selected date range
@app.callback(
    [Output('combined-chart', 'figure'), Output('doughnut-chart', 'figure'),
     Output('average-box-consumo', 'children'), Output('average-box-energia', 'children'),
     Output('saldo-credito-chart', 'figure'), Output('donut-chart-credito-mes', 'figure'),
     Output('gasto-energia-chart', 'figure'), Output('economia-chart', 'figure'),Output('average-box-gasto', 'children'),
     Output('average-box-economia', 'children'),
     Output('average-box-gasto-unid-0', 'children'),Output('average-box-gasto-unid-1', 'children'),Output('average-box-gasto-unid-2', 'children'),Output('average-box-gasto-unid-3', 'children'),
     Output('average-box-economia-unid-0', 'children'),Output('average-box-economia-unid-1', 'children'),Output('average-box-economia-unid-2', 'children'),Output('average-box-economia-unid-3', 'children'),
     ],
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_charts(start_date, end_date):
    filtered_df = df[(df['data'] >= start_date) & (df['data'] <= end_date)]

    # Create a figure with 'energia_gerada' as an area and 'consumo' as bars
    combined_fig = go.Figure()

    # Add 'energia_gerada' as an area
    combined_fig.add_trace(go.Scatter(x=filtered_df['data'], y=filtered_df['energia_gerada'],
                                      mode='lines', fill='tozeroy', name='Energia Gerada'))

    # Add 'consumo' as bars
    combined_fig.add_trace(go.Bar(x=filtered_df['data'], y=filtered_df['consumo'], name='Consumo'))

    # Update the layout of the combined chart
    combined_fig.update_layout(title='Consumo and Energia Gerada Over Time', xaxis_title='Date', yaxis_title='Value')

    # Create the doughnut chart to display the relationship between 'unidade' and 'consumo' with absolute numbers
    doughnut_fig = px.pie(filtered_df, names='unidade', values='consumo', title='Consumo by Unidade', hole=0.4)

    # Calculate the average of the sum of 'consumo' by month
    monthly_avg_consumo = filtered_df.groupby('month_year')['consumo'].sum().mean()

    # Calculate the average of the sum of 'energia_gerada' by month
    monthly_avg_energia = filtered_df.groupby('month_year')['energia_gerada'].sum().mean()

    # Calculate the average of the sum of 'Gasto' by month
    monthly_avg_gasto = filtered_df.groupby('month_year')['valor_pago'].sum().mean()

    # Calculate the average of the sum of 'Economia' by month
    monthly_avg_economia = filtered_df.groupby('month_year')['economia'].sum().mean()

    # Calculate the average of the sum of 'Gasto' by month by 'Unidade'
    gasto_uni = filtered_df.groupby('unidade')['valor_pago'].mean()

    # Calculate the average of the sum of 'Economia' by month by 'unidade'
    economia_uni = filtered_df.groupby('unidade')['economia'].mean()

    # Calculate the  the sum of 'credito' by únidade'
    # sum_credito_unidade = filtered_df.groupby('unidade')['credito_mes'].sum()
    # sum_credito_Total = filtered_df['credito_mes'].sum()
    # monthly_avg_consumo_unidade = filtered_df.groupby(['unidade','month_year'])['consumo'].sum().mean() #--- Pq da erro qdo ativo essa linha

    # print(sum_credito_unidade)
    # print(sum_credito_Total)
    # print(monthly_avg_consumo_unidade)


    # Create the new area chart to display the relationship between 'data' and 'saldo_credito'
    saldo_credito_fig = px.area(
        filtered_df, x='data', y='saldo_credito',
        color='unidade',
        title='Saldo Credito Over Time',
        labels={'saldo_credito': 'Saldo Credito'}
    )

    # Create the donut chart to display the relationship between 'unidade' and 'credito_mes'
    donut_chart_credito_mes = px.pie(filtered_df, names='unidade', values='credito_mes', title='Credito Mes by Unidade',
                                     hole=0.4)

    # Create the Gasto_Energia chart to display the relationship between 'data' and 'valor_pago'
    gasto_energia_fig = px.bar(
        filtered_df, x='data', y='valor_pago',
        color='unidade',
        title='Despesa c/ Energia Over Time',
        labels={'valor_pago': '(R$)'}
    )

    # Create the  economia-chart to display the relationship between 'data' and 'economia'
    economia_chart_fig = px.bar(
        filtered_df, x='data', y='economia',
        color='unidade',
        title='Economia Over Time',
        labels={'economia': '(R$)'}
    )

    return combined_fig, doughnut_fig, f'Avg Consumo: {monthly_avg_consumo:.0f} kWh', f'Avg Energia Gerada: {monthly_avg_energia:.0f} kWh', saldo_credito_fig, donut_chart_credito_mes, gasto_energia_fig, economia_chart_fig, f'Global: R$ {monthly_avg_gasto:.2f}', f'Global: R$ {monthly_avg_economia:.2f}',f'R$ {gasto_uni.iloc[0]:.2f}',f'R$ {gasto_uni.iloc[1]:.2f}',f'R$ {gasto_uni.iloc[2]:.2f}',f'R$ {gasto_uni.iloc[-1]:.2f}',f' R$ {economia_uni.iloc[0]:.2f}',f'R$ {economia_uni.iloc[1]:.2f}',f'R$ {economia_uni.iloc[2]:.2f}',f'R$ {economia_uni.iloc[-1]:.2f}',



if __name__ == '__main__':
    app.run_server(debug=True)
