# FastAPI Web Scraper with MySQL

## Project Overview
This project is a FastAPI application that scrapes data from a website using BeautifulSoup and stores the scraped data in a MySQL database. It provides two API endpoints:
- GET `/scrape`: Scrapes data from a specified website and stores it in the database.
- GET `/data`: Retrieves the stored data from the database.

## Table of Contents
- Requirements
- Setup Instructions
  - 1. Clone the Repository
  - 2. Setup MySQL Database
  - 3. Environment Variables
  - 4. Install Dependencies
  - 5. Run the Application
  - 6. Run with Docker (Optional)
- API Endpoints
- Running Tests
- Assumptions and Decisions

## Requirements
- Python 3.x
- MySQL Server
- FastAPI
- Uvicorn
- Requests
- BeautifulSoup4
- MySQL Connector/Python

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd fastapi-scraper
```

### 2. Setup MySQL Database
Make sure you have MySQL installed and running. Use the following commands to set up your database:

```sql
CREATE DATABASE scraping_db;
USE scraping_db;
```

### 3. Environment Variables
Create a `.env` file in the root directory with the following content:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=NikhilMySQL@987
DB_NAME=scraping_db
```

### 4. Install Dependencies
It's recommended to create a virtual environment before installing the dependencies.

On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

Now, install the required packages:
```bash
pip install -r requirements.txt
```

### 5. Run the Application
To run the FastAPI application locally, use the following command:

```bash
uvicorn main:app --reload --port 8080
```

The application will be available at: [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)

### 6. Run with Docker (Optional)
If you prefer using Docker, follow these steps:

1. Create a `docker-compose.yml` file with the following content:

    ```yaml
    version: '3.8'
    services:
      mysql:
        image: mysql:8.0
        container_name: mysql-db
        environment:
          MYSQL_ROOT_PASSWORD: NikhilMySQL@987
          MYSQL_DATABASE: scraping_db
        ports:
          - "3306:3306"
        volumes:
          - mysql_data:/var/lib/mysql
      fastapi:
        build: .
        command: uvicorn main:app --host 0.0.0.0 --port 8080
        volumes:
          - .:/app
        ports:
          - "8080:8080"
        depends_on:
          - mysql
    volumes:
      mysql_data:
    ```

2. Build and run the containers:
    ```bash
    docker-compose up --build
    ```

The FastAPI app will be available at [http://localhost:8080/docs](http://localhost:8080/docs).

## API Endpoints

### 1. Scrape Data
- **Endpoint**: `/scrape`
- **Method**: GET
- **Description**: Scrapes quotes from a specified website and stores them in the MySQL database.

**Response**:
```json
{
  "message": "Scraping completed",
  "scraped_quotes": ["Quote 1", "Quote 2", "Quote 3"]
}
```

### 2. Get Stored Data
- **Endpoint**: `/data`
- **Method**: GET
- **Description**: Fetches all the quotes stored in the MySQL database.

**Response**:
```json
{
  "data": [
    {"id": 1, "quote": "Quote 1"},
    {"id": 2, "quote": "Quote 2"},
    {"id": 3, "quote": "Quote 3"}
  ]
}
```

## Running Tests
To ensure your application is working correctly, you can run tests.

1. Create a `tests` folder and add test files, e.g., `test_scrape.py`:

    ```python
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app)

    def test_scrape_endpoint():
        response = client.get("/scrape")
        assert response.status_code == 200
        assert "message" in response.json()

    def test_data_endpoint():
        response = client.get("/data")
        assert response.status_code == 200
        assert isinstance(response.json()["data"], list)
    ```

2. Run the tests using:
    ```bash
    pytest tests/
    ```

## Assumptions and Decisions
- The scraper is targeting a static website (https://quotes.toscrape.com/) for demonstration purposes.
- The project uses MySQL as the database; adjust credentials in the `.env` file as needed.
- Data is stored in a table named `quotes`, which is created automatically if it doesn't exist.
- Docker is optional; the app can be run natively using `uvicorn`.
