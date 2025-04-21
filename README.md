# Healthcare Spending Survey System

[![Link to Render deployment](https://healthcare-survey-1.onrender.com)

A Flask-based web application for collecting and analyzing healthcare spending data, featuring MongoDB integration and admin analytics.

## Features

- **Anonymous Data Collection**: Secure web form with privacy assurance
- **MongoDB Storage**: Scalable cloud database using MongoDB Atlas
- **Admin Dashboard**: Password-protected analytics portal
- **Data Visualization**: Jupyter Notebook-powered charts and graphs
- **Automatic CSV Export**: Real-time data export for analysis
- **Render Deployment**: Production-ready hosting configuration

## Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/healthcare-survey.git
   cd healthcare-survey
2.Install dependencies
  pip install -r requirements.txt

## Deployment
1. Create Render account

    New → Web Service → Connect GitHub repository

2. Configure settings:

  Build Command: pip install -r requirements.txt

  Start Command: gunicorn app:app

3. Set environment variables:

  MONGO_URI

  SECRET_KEY

  ADMIN_USER

  ADMIN_PASS

Deploy!

## Data Analysis Workflow
Collect data via web form

1. Run Jupyter notebook:

jupyter notebook notebooks/Healthcare\ Analysis.ipynb
Execute all cells to generate updated charts

Refresh admin dashboard to view new visualizations

Download charts via admin portal for presentations

## Folder structure
healthcare-survey/
├── app/               # Flask application
│   ├── static/        # CSS and generated charts
│   ├── templates/     # HTML templates
│   ├── __init__.py    # App initialization
│   └── routes.py      # Application routes
├── data/              # CSV exports (gitignored)
├── notebooks/         # Jupyter analysis
├── requirements.txt   # Dependencies
└── .env               # Configuration (gitignored)
