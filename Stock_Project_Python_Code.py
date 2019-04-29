import pandas as pd
import pandas_datareader.data as web
import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime as date, datetime
from dash.dependencies import Input,Output,State


#reading the csv file which has all the names of the stocks:
para_df= pd.read_csv(r'F:\projects\plotly_dash_stock_ticker_project\Plotly-Dashboards-with-Dash-master\Plotly-Dashboards-with-Dash-master\Data\NASDAQcompanylist.csv')
#print(para_df.head())
parameter_df = para_df[['Symbol','Name']]


mylist = list(zip(para_df['Symbol'].tolist(),para_df['Name'].tolist()))
#print(mylist[2])

#generating a dash app
app = dash.Dash()
#creating a dynamic layout 
app.layout = html.Div([
        html.Div([
                html.H1('Comparison of Stocks')
                ],style= {'position':'relative','width':'55%','left':'500px','font-family':'Arial'}),
        html.Div([
        html.Div([
                html.H3('Enter the Stock Ticker Symbol')
                ],style={'font-family':'Arial'}),
        html.Div([
                dcc.Dropdown(id='my_stock_picker',options = [{'label':i[1],'value':i[0]} for i in mylist], value='TSLA',multi=True)
                ],style={'width':'55%','font-family':'Arial'}),
        ]),
        html.Div([
        dcc.Graph(id='my_graph')])
    ])        
@app.callback(Output('my_graph','figure'),
             [Input('my_stock_picker','value')]
             )
def update_graph(my_stock_ticker):
    print(my_stock_ticker)
    
    #dynamic dates from today
    end_date= datetime.date.today()
    #print(end_date)
    #since 'iex' takes only dates till last 5 years so, taking those dates
    start_date = datetime.date.today() - datetime.timedelta(days=5*365)
    #print(start_date)
    
    traces= []
    for tic in my_stock_ticker:
    
        df = web.DataReader(tic,'iex',start_date,end_date)
        #we are only concentrating the closing values
        traces.append({'x':df.index,'y':df['close'],'name':tic})
    
    fig = dict(
            data=traces,
            layout=dict(title='.',
                      xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='backward'),
                dict(count=1,
                    label='YTD',
                    step='year',
                    stepmode='todate'),
                dict(count=1,
                    label='1y',
                    step='year',
                    stepmode='backward'),
                dict(count=3,
                    label='3y',
                    step='year',
                    stepmode='backward'),
                dict(step='all')
            ])
        ),type='date')
    )
                )
    return fig
    
if __name__ =='__main__':
    app.run_server()
