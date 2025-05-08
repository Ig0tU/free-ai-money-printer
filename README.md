
Built by https://www.blackbox.ai

---

# Free AI Money Printer - Debunking Misleading Claims

This repository contains our research and implementation to debunk a series of misleading posts related to crypto trading and automation using various APIs. The investigation highlights incorrect API usage, data misinterpretations, and the necessary adjustments made to achieve reliable results.

## Project Overview

A popular narrative circulating on social media suggests that by leveraging AI models, anyone can identify and invest in early-stage crypto tokens before they experience massive price surges. This project aims to analyze and debunk such claims, providing clarity and correct methodologies in using APIs for crypto trading insights.

### Key Findings

1. **Fake API URL**: The original posts referenced unofficial and potentially fraudulent API URLs.
2. **Misleading Data Analysis**: The analysis was based on incorrect data that the assumed APIs did not return.
3. **Incorrect Twitter Analysis**: The suggested API for Twitter analysis was both inaccurate and required a paid subscription.
4. **Token Security Check Flaws**: The code relied on improper HTML parsing instead of using the official API for risk assessments.

**Disclaimer**: This repository does not provide financial advice and is intended for educational and research purposes only.

## Installation

To replicate our findings and run the implementation, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/FractalXBT/free-ai-money-printer.git
   cd free-ai-money-printer
   ```

2. Install dependencies:
   ```bash
   pip install requests pandas python-dotenv colorama websockets
   ```

## Usage

- To run the main data scraping and analysis script, execute:
   ```bash
   python pump_fun_scraper.py
   ```

- The application is also designed to work as a Flask web app. Start the Flask app by running:
   ```bash
   python app.py
   ```

Access the app in your web browser at `http://localhost:8000`.

### Example Token Data for Testing

You can test the application with sample token data:
```json
[
  {
    "name": "Sample Token 1",
    "symbol": "ST1",
    "price": "0.00123",
    "market_cap": "1000000",
    "volume_24h": "50000",
    "twitter_mentions": "1500",
    "telegram_members": "5000",
    "reddit_subscribers": "2000"
  },
  {
    "name": "Sample Token 2",
    "symbol": "ST2",
    "price": "0.05678",
    "market_cap": "5000000",
    "volume_24h": "250000",
    "twitter_mentions": "3000",
    "telegram_members": "10000",
    "reddit_subscribers": "4500"
  }
]
```

## Features

- Detailed analysis of cryptocurrency tokens based on real-time metrics.
- Integration with AI models to derive insights and recommendations.
- Logging for monitoring the performance of the analysis.
- A web interface for user-friendly interaction and visualization of results.

## Dependencies

The following dependencies are required:
- `requests`
- `pandas`
- `python-dotenv`
- `colorama`
- `websockets`
- `flask`
- `flask-login`

## Project Structure

Here's a brief overview of the project structure:

```
free-ai-money-printer/
│
├── app.py                     # Flask web application
├── ai_model_handler.py        # Handles AI model calls and history tracking
├── pump_fun_scraper.py        # Main script for analyzing tokens using AI insights
├── analysis_history.json      # Stores analysis results for historical reference
├── README.md                  # Project documentation
└── .env                       # Environment variables (not included in repo for security)
```

**Developed by**: The FractalXBT Research Team

This README provides all necessary information to understand, install, and use the project effectively. For further contributions and inquiries, feel free to open issues or pull requests on the GitHub repository.