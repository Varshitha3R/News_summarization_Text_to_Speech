import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from gtts import gTTS
import os
import base64
import uuid

# Initialize models
summarizer = pipeline("summarization", model="t5-small")
sentiment_analyzer = pipeline("sentiment-analysis")

# Predefined keyword-topic mapping
TOPIC_KEYWORDS = {
    "Car": ["Tesla", "vehicle", "car", "EV", "electric car", "automobile", "autonomous driving"],
    "Finance": ["stock", "investment", "profit", "revenue", "market", "shareholders"],
    "Technology": ["AI", "artificial intelligence", "software", "innovation", "tech", "robotics"],
    "Regulations": ["government", "policy", "law", "compliance", "regulations"],
    "Protests": ["protest", "strike", "boycott", "rally", "activists"]
}

def determine_topics_from_title(title):
    try:
        summarized_title = summarizer(title, max_length=15, min_length=5, do_sample=False)[0]['summary_text']
        summarized_title_lower = summarized_title.lower()

        detected_topics = []
        for topic, keywords in TOPIC_KEYWORDS.items():
            if any(keyword.lower() in summarized_title_lower for keyword in keywords):
                detected_topics.append(topic)

        return detected_topics if detected_topics else ["General"]
    
    except Exception as e:
        print(f"Error in topic detection: {e}")
        return ["General"]

def clean_text(text):
    return text.replace("\n", " ").replace("\r", " ").strip()

def scrape_news(company_name):
    url = f"https://www.bing.com/news/search?q={company_name}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('a', class_='title')

        scraped_articles = []
        for article in articles[:10]:  # Get only top 10 articles
            title = clean_text(article.text)
            if not title:
                continue  # Skip empty titles

            try:
                summary = summarizer(title, max_length=50, min_length=10, do_sample=False)[0]['summary_text']
                
                # Get sentiment analysis with confidence
                sentiment_result = sentiment_analyzer(summary)[0]
                sentiment_label = sentiment_result['label'].lower()
                confidence = sentiment_result['score']

                # If confidence is low, classify as neutral
                if confidence < 0.7:
                    sentiment_label = "neutral"

                topics = determine_topics_from_title(title)

                scraped_articles.append({
                    "Title": title,
                    "Summary": summary,
                    "Sentiment": sentiment_label,
                    "Topics": topics
                })
            except Exception as e:
                print(f"Error processing article: {e}")
                continue  # Skip faulty articles

        return scraped_articles
    except Exception as e:
        print(f"Error during scraping: {e}")
        return []

def scrape_and_analyze(company_name):
    articles = scrape_news(company_name)

    if not articles:
        return {"error": f"No articles found for the company '{company_name}'"}

    sentiment_distribution = {"positive": 0, "negative": 0, "neutral": 0}
    
    topic_occurrences = {}

    for article in articles:
        sentiment = article["Sentiment"]
        sentiment_distribution[sentiment] += 1
        
        for topic in article["Topics"]:
            topic_occurrences[topic] = topic_occurrences.get(topic, 0) + 1

    sorted_topics = sorted(topic_occurrences.items(), key=lambda x: x[1], reverse=True)
    common_topics = [topic for topic, count in sorted_topics if count > 1]
    unique_topics = [topic for topic, count in sorted_topics if count == 1]

    topic_overlap = {
        "Common Topics": common_topics,
        "Unique Topics": unique_topics
    }

    # Determine final sentiment based on majority sentiment
    if sentiment_distribution["positive"] > sentiment_distribution["negative"]:
        final_sentiment = "सकारात्मक"
    elif sentiment_distribution["negative"] > sentiment_distribution["positive"]:
        final_sentiment = "नकारात्मक"
    else:
        final_sentiment = "तटस्थ"

    result = {
        "Company": company_name,
        "Articles": articles,
        "Comparative Sentiment Score": {
            "Sentiment Distribution": sentiment_distribution,
            "Topic Overlap": topic_overlap
        },
        "Final Sentiment Analysis": f"{company_name} की ताज़ा खबरें ज्यादातर {final_sentiment} हैं।"
    }

    hindi_audio_path = generate_hindi_tts(result["Final Sentiment Analysis"])

    if hindi_audio_path and os.path.exists(hindi_audio_path):
        result["Audio"] = encode_audio_to_base64(hindi_audio_path)
    else:
        print("Error: Hindi TTS file was not generated.")
        result["Audio"] = None  # Ensure response does not break if audio is missing

    return result

def generate_hindi_tts(text):
    if not text:
        return None

    unique_filename = f"{uuid.uuid4().hex[:10]}_output.mp3"
    tts = gTTS(text=text, lang="hi")
    tts.save(unique_filename)

    # Ensure the file exists before returning
    if os.path.exists(unique_filename):
        return unique_filename
    else:
        print("Error: TTS file was not created.")
        return None

def encode_audio_to_base64(audio_path):
    if not audio_path or not os.path.exists(audio_path):
        print("Error: Audio file does not exist or path is invalid.")
        return None

    try:
        with open(audio_path, "rb") as audio_file:
            encoded_audio = base64.b64encode(audio_file.read()).decode("utf-8")
        return f"data:audio/mp3;base64,{encoded_audio}"
    except Exception as e:
        print(f"Error encoding audio: {e}")
        return None
