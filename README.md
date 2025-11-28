# Bill Extraction API - Bajaj Health Datathon

## Overview

A FastAPI-based bill extraction system leveraging Gemini LLM and Pytesseract OCR.

## Features

- ✅ FastAPI REST API
- ✅ Google Gemini LLM integration
- ✅ Pytesseract OCR for text extraction
- ✅ Bill item extraction
- ✅ Token usage tracking
- ✅ Fallback mechanisms

## Setup

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuration

Create a `.env` file with the following content:

```env
GEMINI_API_KEY=your_key_here
LLM_PROVIDER=gemini
USE_GOOGLE_VISION=false
API_PORT=8000
```

## Running

```bash
python app/main.py
```

## Testing

```bash
python test_api.py
```

## API Endpoints

- `GET /` — Welcome
- `GET /health` — Health check
- `POST /extract-bill-data` — Extract bill data

## Response Format

```json
{
    "is_success": true,
    "token_usage": {
        "total_tokens": 800,
        "input_tokens": 500,
        "output_tokens": 300
    },
    "data": {
        "pagewise_line_items": [...],
        "total_item_count": 0
    }
}
```
