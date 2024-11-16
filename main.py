from fastapi import FastAPI
import mysql.connector
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI()

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="NikhilMySQL@987",
        database="scraping_db"
    )

@app.get("/scrape")
def scrape_data():
    url = "https://quotes.toscrape.com/"  
    response = requests.get(url)  

    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = soup.find_all('span', class_='text')  
    scraped_data = [(quote.text.strip(),) for quote in quotes]  

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        quote TEXT
    )
    """)

    cursor.executemany("INSERT INTO quotes (quote) VALUES (%s)", scraped_data)
    conn.commit() 
    conn.close() 

    return {"message": "Scraping completed", "scraped_quotes": [quote[0] for quote in scraped_data]}

@app.get("/data")
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM quotes")
    rows = cursor.fetchall()
    conn.close()
    
    return {"data": [{"id": row[0], "quote": row[1]} for row in rows]}
