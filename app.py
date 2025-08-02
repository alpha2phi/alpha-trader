# Smart Stock Trend Predictor with ChatGPT & Gemini AI
# Stack: Dash + Plotly + OpenAI + Gemini + yfinance + pandas-ta

import dash
from dash import html, dcc, Input, Output, State
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objs as go
import openai
import google.generativeai as genai
import os

# === API Keys (replace with your own) ===
openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-pro")

# === Dash App ===
app = dash.Dash(__name__)
app.title = "Smart Stock Trend Predictor"

# === Layout ===
app.layout = html.Div([
    html.H2("📈 Smart Stock Trend Predictor with AI"),

    dcc.Input(id="ticker", type="text", placeholder="Enter stock ticker (e.g. AAPL)", debounce=True),
    html.Button("Analyze", id="submit", n_clicks=0),

    html.Div(id="price-chart"),
    html.Div(id="ta-output"),
    html.Div(id="chatgpt-output"),
    html.Div(id="gemini-output")
])

# === Helper Functions ===
def get_stock_data(ticker):
    df = yf.download(ticker, period="3mo", interval="1d")
    df.ta.rsi(length=14, append=True)
    df.ta.macd(append=True)
    df.ta.sma(length=20, append=True)
    return df.dropna()

def generate_plot(df):
    candlestick = go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name="Candlestick"
    )
    sma_line = go.Scatter(x=df.index, y=df['SMA_20'], mode='lines', name='SMA 20')
    return dcc.Graph(
        figure=go.Figure(data=[candlestick, sma_line])
    )

def generate_prompt(ticker, df):
    latest = df.iloc[-1]
    return (
        f"You're a financial assistant. Analyze the current technical indicators for stock {ticker}:
"
        f"- RSI: {latest['RSI_14']:.2f}
"
        f"- MACD: {latest['MACD_12_26_9']:.2f}
"
        f"- Signal: {latest['MACDs_12_26_9']:.2f}
"
        f"- SMA 20: {latest['SMA_20']:.2f}
"
        f"- Close: {latest['Close']:.2f}
"
        f"Give a simple explanation of trend direction (bullish/bearish/uncertain) and why."
    )

# === Callbacks ===
@app.callback(
    Output("price-chart", "children"),
    Output("ta-output", "children"),
    Output("chatgpt-output", "children"),
    Output("gemini-output", "children"),
    Input("submit", "n_clicks"),
    State("ticker", "value")
)
def update_output(n, ticker):
    if not ticker:
        return dash.no_update
    try:
        df = get_stock_data(ticker)
        plot = generate_plot(df)
        prompt = generate_prompt(ticker, df)

        # ChatGPT
        gpt_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message['content']

        # Gemini
        gemini_response = gemini_model.generate_content(prompt).text

        return (
            plot,
            html.Pre(prompt),
            html.Div([html.H4("ChatGPT Response"), html.Pre(gpt_response)]),
            html.Div([html.H4("Gemini Response"), html.Pre(gemini_response)])
        )

    except Exception as e:
        return html.Div(f"Error: {e}"), "", "", ""

# === Run ===
if __name__ == "__main__":
    app.run_server(debug=True)
