#!/usr/bin/env python
# coding: utf-8


import plotly.express as px
import yfinance as yf
import pandas as pd
import dash
import ta
import dash_bootstrap_components as dbc
import os

from ta.trend import sma_indicator
from ta.trend import ema_indicator
from ta import momentum
from ta import trend
from ta import volatility
from ta import volume
from ta.momentum import awesome_oscillator
from ta.volatility import bollinger_hband
from ta.volatility import bollinger_lband
from ta.volatility import bollinger_mavg
from dash.dependencies import Input, Output
from dash import html
from dash import dcc
from datetime import date




df = pd.DataFrame()
app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])
server = app.server


# In[2]:


# DECIDING THE APP LAYOUT
app.layout = html.Div(
    [
        # TITLE
        html.H3(children="Visualizing Technical Indicators Using Python and Plotly. - By Surya Sashank Gundepudi",
                style={
                    'textAlign': 'center'
                }),
        # NOTE
        html.Div(children='''(This is for educational purposes only)''',
                 style={
                     'textAlign': 'center',
                 }),
        # LINK FOR TUTORIAL
        html.Div(children=[html.A('SEARCH FOR TUTORIAL AND SOURCE AT GITHUB',
                                  href='https://github.com/suryasashankgundepudi', target='_blank')],
                 style={
                     'textAlign': 'center',
                 }),
        # LINK FOR TECHNICAL ANALYSIS LIBRARY DOCUMENTATION
        html.Div(children=[html.A("""UNDERSTAND WHICH PARAMETERS ARE NEEDED PLEASE GO HERE. 
        IF PARAMETERS ARE MISSING DEFAULT VALUES ARE TAKEN""",
                                  href='https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html',
                                  target='_blank')],
                 style={
                     'textAlign': 'center',
                 }),
        # LINK FOR CURRENT INDICATOR
        html.Div(children=[html.A('LEARN MORE ABOUT CURRENT INDICATOR HERE',
                                  href='https://www.investopedia.com/terms/s/sma.asp',
                                  id="indicator-link",
                                  target='_blank')],
                 style={
                     'textAlign': 'center',
                 }),

        html.Br(),
        html.Br(),

        # THE FIRST ROW AS SEEN IN APPLICATION
        dbc.Row(
            [
                # TEXT FOR TICKER
                dbc.Col(html.Div(children='''Enter The ticker from yahoo finance. Copy and paste all letters 
                at same time please: '''),
                        align='start',
                        style={"margin-left": "20px"}),

                # TEXT FOR START AND END DATE
                dbc.Col((html.Div(children='''Enter the START DATE and END DATE''')), align='end',
                        style={"margin-left": "100px"}),

            ],
            align="start",
        ),

        # THE SECOND ROW AS SEEN IN THE APPLICATION
        dbc.Row(
            [
                # INPUT FOR TICKER VALUE
                dbc.Col((dcc.Input(id="input-1", type="text", value="AMZN")), align='start',
                        style={"margin-left": "20px", 'border-radius': 10}),

                # INPUT FOR DATE RANGE
                dbc.Col((dcc.DatePickerRange(
                    id='my-date-picker-range',
                    min_date_allowed=date(2005, 1, 1),
                    max_date_allowed=date(2020, 12, 31),
                    initial_visible_month=date(2018, 1, 1)
                )), align='end',
                    style={"margin-left": "100px", 'border-radius': 10})]
        ),
        html.Br(),
        html.Br(),

        # THE THIRD ROW AS SEEN IN THE APPLICATION
        dbc.Row(
            [
                # TEXT FOR SHORT WINDOW LENGTH
                dbc.Col(html.Div(children='''Enter the Short Window Length'''), align='start',
                        style={"margin-left": "20px"}),

                # TEXT FOR LONG WINDOW LENGTH
                dbc.Col(html.Div(children='''Enter the Long Window Length (if indicator requires only one 
                window it will take the first one)'''),
                        align='center'),

                # TEXT FOR SIGNAL WINDOW
                dbc.Col(html.Div(children='''Enter the signal Window (if indicator requires only one 
                window length it will take the first value)''')),

                # TEXT FOR TYPE OF INDICATOR
                dbc.Col((html.Div(children='''Select the Type of Indicator''')), align='end',
                        style={"margin-right": "40px"}),

            ],
            align="start",
        ),

        # THE FOURTH ROW AS SEEN IN THE APPLICATION
        dbc.Row(
            [
                # INPUT VALUE FOR SHORT WINDOW LENGTH
                dbc.Col((dcc.Input(id="input-window", type="number", value=12)), align='start',
                        style={"margin-left": "20px", 'border-radius': 10}),

                # INPUT VALUE FOR LONG WINDOW LENGTH
                dbc.Col((dcc.Input(id="input-window-long", type="number", value=26,
                                   style={'border-radius': 10})), align='center'),

                # INPUT VALUE FOR LONG WINDOW LENGTH
                dbc.Col((dcc.Input(id="input-window-signal", type="number", value=9,
                                   style={'border-radius': 10}))),

                # INPUT VALUE FOR INDICATOR
                dbc.Col((dcc.Dropdown(
                    id='indicator',
                    options=[
                        {'label': "Accumulation/Distribution Index", 'value': "ACCDI"},
                        {'label': 'Aroon Indicator', 'value': 'AROON'},
                        {'label': "Average Directional index", 'value': 'ADX'},
                        {'label': "Average True Range (ATR)", 'value': 'Average True Range'},
                        {'label': 'Awesome Oscillator', 'value': 'Awesome Oscillator'},
                        {'label': 'Bollinger Bands (std - 2)', 'value': 'Bollinger Bands'},
                        {'label': 'Chaikin Money Flow (CMF)', 'value': 'Chaikin Money Flow'},
                        {'label': 'Cummilative Returm', 'value': 'CUMRET'},
                        {'label': 'Daily Return', 'value': 'DRET'},
                        {'label': 'Donchian Channel Bands', 'value': 'DCI'},
                        {'label': 'Ease of Movement', 'value': 'Ease of Movement'},
                        {'label': 'Exponential Moving Average', 'value': 'Exponential Moving Average'},
                        {'label': "Ichimoku Kinkō Hyō (Ichimoku)", 'value': 'ICHIMOKU'},
                        {'label': 'Kaufman’s Adaptive Moving Average', 'value': 'KAMA'},
                        {'label': 'Kelter Channel Index', 'value': "KCI"},
                        {'label': 'Money Flow index', 'value': "MFI"},
                        {'label': 'MACD', 'value': 'MACD'},
                        {'label': 'Negative Volume Index Indicator', 'value': "NVII"},
                        {'label': 'Percentage Price Oscillator', 'value': 'Percentage Price Oscillator (PPO)'},
                        {'label': 'Percentage Volume Oscillator', 'value': 'Percentage Volume Oscillator'},
                        {'label': 'Rate of Change', 'value': 'Rate of Change'},
                        {'label': 'Relative Strength Index (RSI)', 'value': 'Relative Strength Index'},
                        {'label': 'Simple Moving Average', 'value': 'Simple Moving Average'},
                        {'label': 'Ulcer Index', 'value': 'ULCI'},
                        {'label': 'Volume Weighted Average Price', 'value': "VWAP"},
                        {'label': 'Weighted Moving Average', 'value': 'WMA'}

                    ],
                    value='Simple Moving Average'
                )), align='end',
                    style={"margin-right": "40px", 'border-radius': 10})]
        ),
        html.Br(),
        dcc.Graph(id='GRAPH'),

    ])


@app.callback(
    Output('GRAPH', 'figure'),
    Input("input-1", "value"),
    Input('indicator', 'value'),
    Input('input-window', 'value'),
    Input('input-window-long', 'value'),
    Input('input-window-signal', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output(input1, indicator_1, window_input, window_input_long, signal_input, start_date, end_date):
    # DOWNLOADING THE DATA FROM YAHOO FINANCE
    df = yf.download(input1, start_date, end_date)
    # SAVING ONLY THE NECESSARY VALUES INTO STOCK
    Stock = pd.DataFrame({
        "Date": df.index,
        "Close": df["Close"],
        "High": df["High"],
        "Low": df["Low"],
        "Volume": df["Volume"]
    })

    # ACCUMALATION DISTRIBUTION INDEX
    if indicator_1 == "ACCDI":
        Stock["ADI"] = volume.acc_dist_index(high=Stock["High"], low=Stock["Low"],
                                             close=Stock["Close"], volume=Stock["Volume"])
        fig = px.line(Stock[["ADI"]], title='Accumulation/Distribution Index (ADI)')
        fig.update_layout(transition_duration=500)
        return fig



    # AROON INDICATOR
    elif indicator_1 == "AROON":
        Stock["AROON UP"] = trend.aroon_up(Stock["Close"], window=window_input)
        Stock["AROON DOWN"] = trend.aroon_down(Stock["Close"], window=window_input)
        fig = px.line(Stock[["AROON UP", "AROON DOWN"]], title='Aroon Indicator')
        fig.update_layout(transition_duration=500)
        return fig



    # AVERAGE DIRECTIONAL INDICATOR
    elif indicator_1 == "ADX":
        Stock["ADX"] = trend.adx(Stock["High"], Stock["Low"], Stock["Close"],
                                 window=window_input)
        Stock["DX_NEG"] = trend.adx_neg(Stock["High"], Stock["Low"], Stock["Close"],
                                        window=window_input)
        Stock["DX_POS"] = trend.adx_pos(Stock["High"], Stock["Low"], Stock["Close"],
                                        window=window_input)
        fig = px.line(Stock[["ADX"]], title='Average Directional Indicator')
        fig.update_layout(transition_duration=500)
        return fig



    # AWESOME INDICATOR
    elif indicator_1 == "Awesome Oscillator":
        Stock["Awesome Oscillator"] = awesome_oscillator(Stock["High"], Stock["Low"], window1=window_input,
                                                         window2=window_input_long)
        fig = px.line(Stock[["Awesome Oscillator"]], title='Awesome Indicator')
        fig.update_layout(transition_duration=500)
        return fig



    # AVERAGE TRUE RANGE INDICATOR
    elif indicator_1 == "Average True Range":
        Stock["Average True Range"] = volatility.average_true_range(high=Stock["High"], low=Stock["Low"],
                                                                    close=Stock["Close"], window=window_input)
        fig = px.line(Stock[["Average True Range"]], title='Average True Range')
        fig.update_layout(transition_duration=500)
        return fig



    # BOLLINGER BANDS
    elif indicator_1 == "Bollinger Bands":
        Stock["HIGH BAND"] = bollinger_hband(Stock["Close"], window=window_input, window_dev=2)
        Stock["LOW BAND"] = bollinger_lband(Stock["Close"], window=window_input, window_dev=2)
        Stock["MID BAND"] = bollinger_mavg(Stock["Close"], window=window_input)
        fig = px.line(Stock[["Close", "HIGH BAND", "LOW BAND", "MID BAND"]], title='Close and Bollinger Bands')
        fig.update_layout(transition_duration=500)
        return fig




    # CHAIKIN INDICATOR
    elif indicator_1 == "Chaikin Money Flow":
        Stock["Chaikin Money Flow"] = volume.chaikin_money_flow(high=Stock["High"], low=Stock["Low"],
                                                                close=Stock["Close"], volume=Stock["Volume"],
                                                                window=window_input)
        fig = px.line(Stock[["Chaikin Money Flow"]], title='Chaikin Indicator')
        fig.update_layout(transition_duration=500)
        return fig



    # Commodity Channel Index (CCI)
    elif indicator_1 == "CCI":
        Stock["CCI"] = trend.cci(high=Stock["High"], low=Stock["Low"],
                                 close=Stock["Close"], window=window_input)
        fig = px.line(Stock[["Close", "CCI"]], title='Close VS Commodity Chanel Index')
        fig.update_layout(transition_duration=500)
        return fig




    # CUMMILATIVE RETURN
    elif indicator_1 == "CUMRET":
        Stock["Cummilative Return"] = ta.others.cumulative_return(Stock['Close'])
        fig = px.line(Stock[["Cummilative Return"]], title='Cummilative Return')
        fig.update_layout(transition_duration=500)
        return fig



    # DAILY RETURN
    elif indicator_1 == "DRET":
        Stock["Daily Return"] = ta.others.daily_return(Stock['Close'])
        fig = px.line(Stock[["Daily Return"]], title='Daily Return')
        fig.update_layout(transition_duration=500)
        return fig



    # Donchian CHANNEL INDICATOR
    elif indicator_1 == "DCI":
        Stock["HIGH BAND"] = volatility.donchian_channel_hband(high=Stock["High"], low=Stock["Low"],
                                                               close=Stock["Close"], window=window_input)
        Stock["LOW BAND"] = volatility.donchian_channel_lband(high=Stock["High"], low=Stock["Low"],
                                                              close=Stock["Close"], window=window_input)
        Stock["MID BAND"] = volatility.donchian_channel_mband(high=Stock["High"], low=Stock["Low"],
                                                              close=Stock["Close"], window=window_input)
        fig = px.line(Stock[["Close", "HIGH BAND", "LOW BAND", "MID BAND"]], title='Close and Donchian Channel Bands')
        fig.update_layout(transition_duration=500)
        return fig



    # EASE OF MOVEMENT INDICATOR
    elif indicator_1 == "Ease of Movement":
        Stock["Ease of Movement"] = volume.ease_of_movement(high=Stock["High"], low=Stock["Low"],
                                                            volume=Stock["Volume"], window=window_input)
        fig = px.line(Stock[["Ease of Movement"]], title='Ease of Movement')
        fig.update_layout(transition_duration=500)
        return fig



    # EXPONENTIAL MOVING AVERAGE
    elif indicator_1 == "Exponential Moving Average":
        Stock["EMA"] = ema_indicator(Stock["Close"], window=window_input)
        fig = px.line(Stock[["Close", "EMA"]], title='Close VS Exponential Moving Average')
        fig.update_layout(transition_duration=500)
        return fig






    # Ichimoku Kinkō Hyō (Ichimoku)
    elif indicator_1 == "ICHIMOKU":
        Stock["Senkou Span A"] = trend.ichimoku_a(high=Stock["High"], low=Stock["Low"], window1=window_input,
                                                  window2=window_input_long)
        Stock["Senkou Span B"] = trend.ichimoku_b(high=Stock["High"], low=Stock["Low"], window2=window_input_long,
                                                  window3=signal_input)
        Stock["Kiju Sen (Base Line)"] = trend.ichimoku_base_line(high=Stock["High"], low=Stock["Low"],
                                                                 window1=window_input,
                                                                 window2=window_input_long)
        Stock["Tenkan Sen (Conversion Line)"] = trend.ichimoku_conversion_line(high=Stock["High"], low=Stock["Low"],
                                                                               window1=window_input,
                                                                               window2=window_input_long)
        fig = px.line(Stock[["Close", "Senkou Span A", "Senkou Span B", "Kiju Sen (Base Line)",
                             "Tenkan Sen (Conversion Line)"]],
                      title='Close and Ichimoku')
        fig.update_layout(transition_duration=500)
        return fig



    # KAUFMAN'S ADAPTIVE MOVING AVERAGE
    elif indicator_1 == "KAMA":
        Stock["KAMA"] = momentum.kama(Stock["Close"], window=window_input)
        fig = px.line(Stock[["Close", "KAMA"]], title='Close VS KAMA')
        fig.update_layout(transition_duration=500)
        return fig


    # KELTER CHANNEL INDICATOR
    elif indicator_1 == "KCI":
        Stock["HIGH BAND"] = volatility.keltner_channel_hband(Stock['High'], Stock['Low'],
                                                              Stock["Close"], window=window_input,
                                                              window_atr=window_input_long)
        Stock["LOW BAND"] = volatility.keltner_channel_lband(Stock['High'], Stock['Low'],
                                                             Stock["Close"], window=window_input,
                                                             window_atr=window_input_long)
        Stock["MID BAND"] = volatility.keltner_channel_mband(Stock['High'], Stock['Low'],
                                                             Stock["Close"], window=window_input,
                                                             window_atr=window_input_long)
        fig = px.line(Stock[["Close", "HIGH BAND", "LOW BAND", "MID BAND"]], title='Close and Keltner Indicator')
        fig.update_layout(transition_duration=500)
        return fig



    # MONEY FLOW INDEX
    elif indicator_1 == "MFI":
        Stock["MFI"] = volume.money_flow_index(high=Stock["High"], low=Stock["Low"],
                                               close=Stock["Close"], volume=Stock["Volume"],
                                               window=window_input)
        fig = px.line(Stock["MFI"], title='MONEY FLOW INDEX')
        fig.update_layout(transition_duration=500)
        return fig



    # MOVING AVERAGE CONVERGENCE DIVERGENCE
    elif indicator_1 == "MACD":
        Stock["MACD"] = trend.macd(Stock["Close"], window_slow=window_input_long,
                                   window_fast=window_input)
        Stock["MACD SIGNAL"] = trend.macd_signal(Stock["Close"], window_slow=window_input_long,
                                                 window_fast=window_input, window_sign=signal_input)
        fig = px.line(Stock[["MACD", "MACD SIGNAL"]], title='MACD AND MACD SIGNAL')
        fig.update_layout(transition_duration=500)
        return fig

    # NEGATIVE VOLUME INDEX INDICATOR
    elif indicator_1 == "NVII":
        Stock["NVII"] = volume.negative_volume_index(close=Stock["Close"], volume=Stock["Volume"])
        fig = px.line(Stock[["Close", "NVII"]], title='Close and Negative Volume Index Indicator')
        fig.update_layout(transition_duration=500)
        return fig


    # PERCENTAGE PRICE OSCILLATOR
    elif indicator_1 == "Percentage Price Oscillator (PPO)":
        Stock["PPO"] = momentum.ppo(Stock["Close"], window_slow=window_input_long,
                                    window_fast=window_input, window_sign=signal_input)
        fig = px.line(Stock[["PPO"]], title='PPO')
        fig.update_layout(transition_duration=500)
        return fig



    # PERCENTAGE VOLUME OSCILLATOR
    elif indicator_1 == "Percentage Volume Oscillator":
        Stock["PVO"] = momentum.pvo(Stock["Close"], window_slow=window_input_long,
                                    window_fast=window_input, window_sign=signal_input)
        Stock["SIGNAL"] = momentum.pvo(Stock["Close"], window_slow=window_input_long,
                                       window_fast=window_input, window_sign=signal_input)
        fig = px.line(Stock[["PVO", "SIGNAL"]], title='PVO VS PVO SIGNAL')
        fig.update_layout(transition_duration=500)
        return fig



    # RATE OF CHANGE
    elif indicator_1 == "Rate of Change":
        Stock["ROC"] = momentum.roc(Stock["Close"], window=window_input)
        fig = px.line(Stock["ROC"], title='RATE OF CHANGE')
        fig.update_layout(transition_duration=500)
        return fig



    # RELATIVE STRENGTH INDEX
    elif indicator_1 == "Relative Strength Index":
        Stock["RSI"] = momentum.rsi(Stock["Close"], window=window_input)
        fig = px.line(Stock[["RSI"]], title='Relative Strength Index')
        fig.update_layout(transition_duration=500)
        return fig



    # SIMPLE MOVING AVERAGE
    elif indicator_1 == "Simple Moving Average":
        Stock["MA"] = sma_indicator(Stock["Close"], window=window_input)
        fig = px.line(Stock[["Close", "MA"]], title='Close VS Simple Moving Average')
        fig.update_layout(transition_duration=500)
        return fig


    # ULCER INDEX
    elif indicator_1 == "ULCI":
        Stock["ULCI"] = volatility.ulcer_index(Stock["Close"], window=window_input)
        fig = px.line(Stock[["ULCI"]], title='Ulcer Index')
        fig.update_layout(transition_duration=500)
        return fig



    # VOLUME WEIGHTED AVERAGE PRICE
    elif indicator_1 == "VWAP":
        Stock["VWAP"] = volume.volume_weighted_average_price(high=Stock["High"], low=Stock["Low"],
                                                             close=Stock["Close"], volume=Stock["Volume"],
                                                             window=window_input)
        fig = px.line(Stock[["Close", "VWAP"]], title='Close VS Volume Weighter Average Price')
        fig.update_layout(transition_duration=500)
        return fig


    # WEIGHTED MOVING AVERAGE
    # VOLUME WEIGHTED AVERAGE PRICE
    elif indicator_1 == "WMA":
        Stock["WMA"] = trend.wma_indicator(close=Stock["Close"], window=window_input)
        fig = px.line(Stock[["Close", "WMA"]], title='Close VS Weighted Moving Average')
        fig.update_layout(transition_duration=500)
        return fig


# UPDATING THE LINKS FOR TECHNICAL INDICATOR

@app.callback(
    Output('indicator-link', 'href'),
    Input('indicator', 'value')
)
def update_link(indicator_1):
    if indicator_1 == "ACCDI":
        url = """https://www.ifcm.co.uk/ntx-indicators/awesome-oscillatorr"""
        return url


    elif indicator_1 == "Awesome Oscillator":
        url = "https://www.ifcm.co.uk/ntx-indicators/awesome-oscillator"
        return url


    elif indicator_1 == "ADX":
        url = """https://www.ifcm.co.uk/ntx-indicators/awesome-oscillator"""
        return url



    elif indicator_1 == "AROON":
        url = """https://www.investopedia.com/terms/a/aroon.asp"""
        return url


    elif indicator_1 == "Average True Range":
        url = """https://www.ifcm.co.uk/ntx-indicators/awesome-oscillatore"""
        return url


    elif indicator_1 == "Bollinger Bands":
        url = "https://www.investopedia.com/trading/using-bollinger-bands-to-gauge-trends/"
        return url


    elif indicator_1 == "Chaikin Money Flow":
        url = "https://school.stockcharts.com/doku.php?id=technical_indicators:chaikin_money_flow_cmf"
        return url


    elif indicator_1 == "CCI":
        url = "https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html#ta.trend.CCIIndicator"
        return url


    elif indicator_1 == "Ease of Movement":
        url = """https://en.wikipedia.org/wiki/Ease_of_movement"""
        return url


    elif indicator_1 == "Exponential Moving Average":
        url = "https://www.investopedia.com/terms/e/ema.asp"
        return url


    elif indicator_1 == "ICHIMOKU":
        url = """https://school.stockcharts.com/doku.php?id=technical_indicators:ichimoku_cloud"""
        return url
    elif indicator_1 == "Kaufman’s Adaptive Moving Average":
        url = "https://www.tradingview.com/ideas/kama/"
        return url

    elif indicator_1 == "KCI":
        url = """https://school.stockcharts.com/doku.php?id=technical_indicators:keltner_channels"""
        return url


    elif indicator_1 == "MFI":
        url = """https://school.stockcharts.com/doku.php?id=technical_indicators:money_flow_index_mfi"""
        return url


    elif indicator_1 == "MFI":
        url = """https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html#ta.trend.MACD"""
        return url


    elif indicator_1 == "Percentage Price Oscillator (PPO)":
        url = "https://school.stockcharts.com/doku.php?id=technical_indicators:price_oscillators_ppo"
        return url


    elif indicator_1 == "Percentage Volume Oscillator":
        url = "https://school.stockcharts.com/doku.php?id=technical_indicators:percentage_volume_oscillator_pvo"
        return url


    elif indicator_1 == "Rate of Change":
        url = "https://school.stockcharts.com/doku.php?id=technical_indicators:rate_of_change_roc_and_momentum"
        return url


    elif indicator_1 == "Relative Strength Index":
        url = "https://www.investopedia.com/terms/r/rsi.asp"
        return url


    elif indicator_1 == "Simple Moving Average":
        url = "https://www.investopedia.com/terms/s/sma.asp"
        return url

    elif indicator_1 == "ULCI":
        url = """https://school.stockcharts.com/doku.php?id=technical_indicators:ulcer_index"""
        return url

    elif indicator_1 == "VWAP":
        url = """https://school.stockcharts.com/doku.php?id=technical_indicators:vwap_intraday"""
        return url


    elif indicator_1 == "WMA":
        url = "https://corporatefinanceinstitute.com/resources/knowledge/trading-investing/weighted-moving-average-wma/"
        return url


# In[3]:


if __name__ == '__main__':
    app.run_server()

# In[ ]:
