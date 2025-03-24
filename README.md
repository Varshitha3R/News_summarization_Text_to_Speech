# News Summarization and text-to-speech

This project is a web-based application that scrapes company-related news from Bing, summarizes the articles, performs sentiment analysis, extracts topics dynamically, and provides a comparative sentiment score. Additionally, the final sentiment analysis result is converted into Hindi speech using gTTS.

## Features
- **News Scraping**: Fetches the latest news articles for a given company using BeautifulSoup.
- **Text Summarization**: Summarizes articles using the `t5-small` model from Hugging Face.
- **Sentiment Analysis**: Determines the sentiment of the news articles using Hugging Face's sentiment analysis pipeline.
- **Topic Extraction**: Identifies topics based on predefined keyword mappings.
- **Comparative Sentiment Analysis**: Aggregates sentiment scores across multiple articles.
- **Hindi TTS Generation**: Converts the final sentiment analysis into Hindi speech using gTTS.
- **Streamlit UI**: Provides a simple user interface for input and result visualization.
- **Flask API**: Serves the analysis as a REST API endpoint.

## Project Structure
```
project_folder/
│── app.py                 # Streamlit-based UI
│── api.py                 # Flask API for analysis
│── utils.py               # Utility functions for scraping, summarization, sentiment analysis, etc.
│── requirements.txt       # Required dependencies
│── README.md              # Project documentation
```

## Installation & Setup

### 1. Clone the Repository
```sh
git clone <repository_url>
cd project_folder
```

### 2. Create and Activate a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Run the Flask API
```sh
python api.py
```

The Flask API will start at `http://127.0.0.1:5000/analyze`.

### 5. Run the Streamlit App
```sh
streamlit run app.py
```

The Streamlit app will launch in the browser, allowing users to enter a company name and analyze the news sentiment.

## API Usage

### Endpoint
```
POST http://127.0.0.1:5000/analyze
```

### Request Body (JSON)
```json
{
    "company": "Tesla"
}
```

### Response Format
```json
{
    "Company": "Tesla",
    "Articles": [
        {
            "Title": "Tesla Stock Rises Amid Strong Q1 Earnings",
            "Summary": "Tesla reports strong Q1 earnings, beating analysts' expectations.",
            "Sentiment": "POSITIVE",
            "Topics": ["Finance", "Stock"]
        }
    ],
    "Comparative Sentiment Score": {
        "Sentiment Distribution": {
            "Positive": 5,
            "Negative": 3,
            "Neutral": 2
        },
        "Topic Overlap": {
            "Common Topics": ["Finance"],
            "Unique Topics": ["Regulations"]
        }
    },
    "Final Sentiment Analysis": "Tesla की ताज़ा खबरें ज्यादातर सकारात्मक हैं।",
    "Audio": "data:audio/mp3;base64,...."
}
```

## Dependencies
The required Python packages are listed in `requirements.txt`:
```txt
streamlit
flask
requests
beautifulsoup4
transformers
gtts
uuid
```
Install them using:
```sh
pip install -r requirements.txt
```

## Deployment on Hugging Face Spaces
1. Create a new Space on Hugging Face.
2. Select `Streamlit` as the SDK.
3. Upload your project files.
4. Add a `requirements.txt` file with necessary dependencies.
5. Ensure `app.py` is correctly set as the main entry point.
6. Deploy the Space and test the web app.

## Future Improvements
- Add more NLP models for better sentiment accuracy.
- Improve topic detection with machine learning techniques.
- Optimize the scraping process for multiple sources.
- Deploy as a containerized application using Docker.

---
This project provides an efficient way to analyze company-related news sentiment and convert key insights into Hindi speech, making it useful for business analysts, investors, and regional audiences.

