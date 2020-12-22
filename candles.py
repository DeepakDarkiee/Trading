
import time
import config
import xlsxwriter
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import requests
import json
import os
import plotly.graph_objs as go 
        
app = dash.Dash()
print(__name__)
app.layout = html.Div(children=[
    html.Div(children='''
        Symbol to graph:
    '''),

    html.Div(id='output-graph'),
    dcc.Interval( 
			id = 'graph-update', 
			interval = 20000,
			n_intervals = 0
		), 

])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input('graph-update','n_intervals' )]
)
def update_value(symbol):
    symbol='TTM'
    
    if os.path.exists('{}.xlsx'.format(symbol)):
        os.remove('{}.xlsx'.format(symbol))
    time.sleep(3)
    with open('{}.xlsx'.format(symbol), 'w') as w:
        w.write('')
        # gets stock data
    data = {
            'function': 'TIME_SERIES_INTRADAY' ,
            'symbol': symbol ,
            'interval': '1min' ,
            'outputsize': 'full' ,
            'datatype': 'json' ,
            'apikey': config.API_KEY
        }
    response = requests.get('https://www.alphavantage.co/query?', params=data)
	# api_request = requests.get(f"https://sandbox.iexapis.com/stable/stock/{ticker}/{IEX_CLOUD_API_TOKEN}")
    
    try:
        dummy = response.json()['Time Series (1min)']
    except Exception as exc:
        print(':While getting stock data for {}, got error from AlphaVantage... Waiting 15 seconds...'.format(symbol))
    data = response.json()['Time Series (1min)']
    print(data)
    workbook = xlsxwriter.Workbook('{}.xlsx'.format(symbol))
    worksheet = workbook.add_worksheet('stock data')
    worksheet.write(0,0,"Time")
    worksheet.write(0, 1, "open")
    worksheet.write(0, 2, 'high')
    worksheet.write(0, 3, 'low')
    worksheet.write(0, 4, 'close')
    worksheet.write(0, 5, 'volume')
    d_count = 1
    for day in data.keys():
    
        stock_data = data[day]
        worksheet.write(d_count, 0, str(day))
        worksheet.write(d_count, 1, float(stock_data['1. open']))
        worksheet.write(d_count, 2, float(stock_data['2. high']))
        worksheet.write(d_count, 3, float(stock_data['3. low']))
        worksheet.write(d_count, 4, float(stock_data['4. close']))
        worksheet.write(d_count, 5, float(stock_data['5. volume']))
        d_count += 1
        # insert formulas
    i, maxRow = 1, worksheet.dim_rowmax + 1
        
    num_format = workbook.add_format({'num_format': '0.00;0.00'})
    percent_format = workbook.add_format({'num_format': '0.0000%'})
    # avg per day
    worksheet.write(0, 7, 'Day Avg.')
    while i < maxRow:
        worksheet.write(i, 7, '=(B{}+E{})/2'.format(i+1, i+1), num_format)
        i += 1
    worksheet.write(maxRow - 2, 8, 'Avg(Total)')
    worksheet.write(maxRow - 1, 8, '=AVERAGE(H2:H{})'.format(maxRow), num_format)
    # total percent change
    worksheet.write(maxRow - 2, 10, 'Total %change')
    worksheet.write(maxRow - 1, 10, '=((E2-B101)/B101)*100', num_format)
    workbook.close()
    file = pd.read_excel("{}.xlsx".format(symbol))     
    fig=go.Figure(
            data=[
                go.Candlestick(
            
                    low=file['low'],
                    high=file['high'],
                    close=file['close'],
                    open=file['open'],
                    increasing_line_color='green',
                    decreasing_line_color='blue'
                )
            ]

        )
    fig.update_layout(
    autosize=False,
    width=1000,
    height=700,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
    paper_bgcolor="LightSteelBlue",
)

        

    return dcc.Graph( id='plot',
        
        figure=fig
    )

if __name__ == '__main__':
    app.run_server(debug=True)

