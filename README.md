# Twitter Search API & Monitoring System

A robust, modular Flask-based API for scraping and monitoring Twitter/X data. This system features intelligent account management, database integration, and a real-time monitoring dashboard.

## 🚀 Key Features

*   **Modular Architecture**: Clean separation of concerns (Routes, Services, Utils).
*   **Database Integration**: Stores all scraped tweets and system logs in MySQL.
*   **Smart Account Rotation**: 
    *   Centralized account management via database.
    *   Automatic rotation to prevent rate limits.
    *   Status tracking (Active, Rate Limited, Suspended).
*   **Robust Error Handling**: Specifically handles `TooManyRequests` (429) and other Twitter errors.
*   **Pro Scheduler**: 
    *   Runs automatically in the background.
    *   Fetches **dynamic keywords** and **accounts** from the database.
    *   Randomized intervals (Jitter) for stealth.
*   **Real-time Monitoring Dashboard**: Endpoint to view system stats, account health, and recent logs.

## 📂 Project Structure

```
├── main.py                 # Entry point (Flask App)
├── config.py               # Configuration (DB, Ports)
├── schema.sql              # Database Schema (Tweets, Accounts, Logs, Keywords)
├── requirements.txt        # Python Dependencies
├── scheduler_job.py        # Background Scheduler (Pro Version)
│
├── routes/                 # API Endpoints
│   ├── search_route.py     # POST /search (Scraping)
│   └── monitoring_route.py # GET /monitoring (Dashboard)
│
├── services/               # Business Logic
│   ├── twitter_service.py  # Twitter Interaction (Twikit)
│   └── monitoring_service.py # Dashboard Stats Logic
│
└── utils/                  # Utilities
    ├── database.py         # DB Connection & Helpers
    ├── account_manager.py  # Account Selection & Updates
    └── tweet_mapper.py     # Data Normalization
```

## 🛠️ Setup & Installation

1.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Database Setup**
    *   Ensure MySQL is running.
    *   Update `config.py` with your database credentials.
    *   Initialize the database tables:
        ```bash
        python -c "from config import db_config; from utils.database import init_db; init_db(db_config)"
        ```

3.  **Seed Data**
    *   Insert your Twitter accounts into the `accounts` table.
    *   Insert keywords into the `keywords` table.

4.  **Run the Application**
    ```bash
    python main.py
    ```

## 🔌 API Endpoints

### 1. Search Tweets
*   **URL**: `/search`
*   **Method**: `POST`
*   **Body**:
    ```json
    {
        "query": "keyword lang:id",
        "username": "optional_override",
        "password": "optional_override"
    }
    ```
*   **Response**: Structured JSON with summary of success/failed and saved data.

### 2. Monitoring Dashboard
*   **URL**: `/monitoring`
*   **Method**: `GET`
*   **Response**:
    *   `stats`: Total tweets, success/fail counts.
    *   `accounts`: List of accounts and their status.
    *   `recent_logs`: Latest system activity.

## 🤖 Scheduler
The scheduler is defined in `scheduler_job.py`. To enable it, uncomment `start_scheduler()` in `main.py`. It will automatically:
1.  Pick a random active account.
2.  Pick a random active keyword.
3.  Perform a search and save results.
