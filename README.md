# IPHO Backend

Backend application for the IPHO project.

## Installation

```bash
npm install
```

## Usage

```bash
npm start
```

## Environment Variables

Create a `.env` file in the root directory and add your environment variables.

## API Documentation

[Add your API documentation here]

# IPHC Backend Setup Guide

## Quick Start
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## API Endpoints
- **Root**: `GET /` - API information
- **Predict**: `POST /api/predict/` - Make predictions
- **Test Logic**: `GET /api/predict/test-logic` - Test medical logic
- **Available Symptoms**: `GET /api/predict/symptoms` - Get all symptoms

## Database Setup
The application will automatically create the database if it doesn't exist.

## Development
```bash
# Freeze requirements
pip freeze > requirements.txt

# Run tests
python test_medical_logic.py
```

## Features
- ✅ Hybrid ML + Medical Logic
- ✅ 75+ Symptoms Supported
- ✅ Symptom-specific Intelligence
- ✅ Smart Disease Filtering