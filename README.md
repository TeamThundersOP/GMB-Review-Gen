# GMB-Review-Gen

A Flask web application that generates SEO-friendly Google reviews for InboxTales digital agency. The app uses AI to create authentic-sounding reviews based on user input.

## Features

- Simple web interface
- AI-powered review generation
- SEO-friendly content
- Copy to clipboard functionality
- Mobile responsive design

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd inboxtales-review-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The app will be available at `http://localhost:5000`

## Usage

1. Enter your name or business name
2. Select a rating (3-5 stars)
3. Click "Generate Review"
4. Copy the generated review to clipboard

## Deployment

This application is configured for deployment on Render. See `render.yaml` for configuration details.

## Tech Stack

- Flask
- Python
- Bootstrap
- NinjaChat AI API 