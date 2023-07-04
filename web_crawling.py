from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
import sqlite3
import spacy

# Load English tokenizer, POS tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")

# Simple text extraction function
def extract_health_related_info(text):
    blob = TextBlob(text)
    health_related_sentences = []
    keywords = ["diet", "exercise", "sleep", "stress", "hydration", "nutrition", "workout", "steps", "activity", "calories"]
    for sentence in blob.sentences:
        if any(keyword in sentence.lower() for keyword in keywords):
            health_related_sentences.append(str(sentence))
    return health_related_sentences

# Function to scrape the website and extract health information
def scrape_for_health_info(url, extractor):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    text = ' '.join(p.get_text() for p in soup.find_all('p'))
    health_info = extractor(text)
    return health_info

# Create a connection to the SQLite database
# Doesn't matter if the database does not yet exist
conn = sqlite3.connect('health_info.db')

# Create a cursor
c = conn.cursor()

# Execute some SQL to create a table in the database
c.execute('''CREATE TABLE IF NOT EXISTS health_info
            (advice text)''')

# Scrape the website and store health information
url = "https://www.mayoclinic.org/healthy-lifestyle"
health_info = scrape_for_health_info(url, extract_health_related_info)
for info in health_info:
    # Use Spacy to check if the sentence is an imperative
    doc = nlp(info)
    if doc[0].tag_ == 'VB' or doc[0].tag_ == 'MD':
        c.execute("INSERT INTO health_info VALUES (?)", (info,))

# Save (commit) the changes and close the connection to the database
conn.commit()
conn.close()

# Reconnect to the database to fetch and print the data
conn = sqlite3.connect('health_info.db')
c = conn.cursor()
c.execute("SELECT * FROM health_info")
rows = c.fetchall()
for row in rows:
    print(row)
conn.close()
