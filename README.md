# Trustably App

Trustably is a comprehensive assessment and reporting platform designed to evaluate organizational AI maturity and governance. It allows users to conduct assessments, track progress, and generate detailed PDF reports based on a structured framework of knowledge areas and focus scores.

## Features

- **Assessment Management**: Create, update, and manage multiple AI assessments.
- **QA Library**: A structured library of questions organized by knowledge areas.
- **Detailed Analysis**: Track assessment status and scores across various dimensions (Functional Governance, Observability, Culture, Unified Platform, and Security).
- **PDF Report Generation**: Generate professional, branded PDF reports including:
  - Overall and focus-area scores.
  - Spider charts for visual maturity analysis.
  - Gap analysis and strategic roadmaps.
- **History Tracking**: View a log of assessment events and milestones.

##  Tech Stack

- **Backend**: Python 3.10+ / Flask
- **Frontend**: HTML, CSS (Jinja2 Templates)
- **PDF Generation**: ReportLab, Pandas
- **Data Storage**: JSON (for assessments and responses), TSV (for question metadata)
- **Server**: Gunicorn (production)

## 📁 Project Structure

```text
trustably-app/
├── app.py                 # Flask application entry point
├── main.py                # Utility/Main script
├── trustably_report.py    # PDF report generation logic using ReportLab
├── handlers/
│   ├── api.py             # API endpoints for assessment CRUD operations
│   ├── ui.py              # UI routes and page rendering
│   └── util.py            # Shared utility functions and constants
├── static/
│   ├── data/              # JSON stores for assessments and responses
│   ├── metadata/          # TSV files containing question definitions
│   └── reports/           # Generated PDF reports
├── templates/              # Jinja2 HTML templates for the web interface
└── requirements.txt       # Project dependencies
```

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Virtual environment (recommended)

### Setup Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/ayanguha/trustably-app 
   cd trustably-app
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

## 🏃 Running the Application

### Development Mode
Run the Flask app directly:
```bash
flask run --debug 
```
The application will be available at `http://127.0.0.1:5000`.

### Production Mode
Use Gunicorn for a more robust deployment:
```bash
gunicorn app:app
```


##  How it Works

1. **Metadata**: The app reads question definitions from `static/metadata/questions.tsv`.
2. **Assessments**: Users create assessments via the UI, which are stored as JSON objects in `static/data/assessments.json`.
3. **Reporting**: The `trustably_report.py` module processes assessment data and uses `ReportLab` to generate a high-quality PDF report with visual charts and a strategic roadmap.

##  Current Deployment

https://trustably-app.onrender.com/ 

- This uses automated deployment using https://render.com/ 

## To Do

- Add backend 
- Add Databricks/Snowflake/AWS deployment process
