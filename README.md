# ToxScreen - Toxicity Detection Dashboard

ToxScreen is a web-based tool that detects toxic content in user comments using the Google Perspective API. It supports both individual comment analysis and bulk Excel uploads, with a PDF report generation and dashboard insights.

## Features

- Single Text Toxicity Analysis
- Bulk Toxicity Analysis via Excel
- PDF Toxicity Distribution Report
- Perspective API metrics: TOXICITY, INSULT, THREAT, IDENTITY_ATTACK, SEVERE_TOXICITY
- Streamlit Dashboard UI
- Downloadable ZIP with Excel + Report

## Project Structure

toxscreen/
├── api/
│   └── app.py               # FastAPI backend
├── dashboard/
│   └── app.py               # Streamlit frontend
├── utils/
│   └── perspective.py       # Perspective API integration
│   └── report_generator.py  # Generates PDF report
├── requirements.txt
└── README.md

## Installation

### 1. Clone the repo

    git clone https://github.com/your-username/ToxScreen.git
    cd ToxScreen

### 2. Set up virtual environment

    python -m venv venv
    source venv/bin/activate    # On Windows: venv\Scripts\activate
    pip install -r requirements.txt

## Perspective API Setup

1. Go to: https://perspectiveapi.com/
2. Get an API key from Google Cloud Console.
3. Add it in utils/perspective.py:

    API_KEY = "YOUR_API_KEY"

## Run the Application

### 1. Start FastAPI backend

    uvicorn api.app:app --reload

### 2. Start Streamlit frontend

    streamlit run dashboard/app.py

## Excel Input Format

The uploaded Excel file should have a `text` column:

| text                     |
|--------------------------|
| "You are so dumb."       |
| "Great work!"            |
| "I hate this platform."  |

## Output

When you upload an Excel file:

- A processed Excel file with added toxicity scores
- A PDF report showing score distribution
- Both files zipped and downloadable

## Dependencies

Install all with:

    pip install -r requirements.txt

Includes:
- fastapi
- streamlit
- pandas
- openpyxl
- matplotlib
- plotly
- google-api-python-client
- uvicorn

## Contributing

PRs and suggestions welcome! Please open issues or submit pull requests.

## License

MIT License. © 2025 Vedant Patil

