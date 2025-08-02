 # alpha-trader 🚀

A Python-only dashboard to analyze stocks using technical analysis and AI insights.

## 🔧 Stack
- Dash (UI Framework)
- Plotly (Charting)
- yfinance + pandas-ta (Data & Technical Indicators)
- OpenAI + Gemini (AI-Powered Trend Prediction)
- Hosted locally or on AWS or Azure

## 📁 Project Structure
```
smart_stock_trend_ai/
│
├── app.py               # Main Dash app
├── utils/               # Utility functions for data, AI
├── models/              # Optional ML models
├── assets/              # Static files (CSS/images)
├── notebooks/           # Jupyter experiments
├── requirements.txt     # Dependencies
└── README.md            # Project docs
```

## ▶️ Running the App
```bash
pip install -r requirements.txt
python app.py
```

Set API keys via environment variables:
```bash
export OPENAI_API_KEY=your_key
export GEMINI_API_KEY=your_key
```

## 🧠 Sample Prompt
The app generates technical indicators and passes them to both ChatGPT and Gemini to interpret short-term stock trends.

## 📈 Output
- Interactive candlestick + SMA charts
- AI commentary from ChatGPT and Gemini