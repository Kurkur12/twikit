CREATE DATABASE IF NOT EXISTS project;
USE project;

CREATE TABLE IF NOT EXISTS tweets (
    id VARCHAR(255) PRIMARY KEY,
    created_at_datetime DATETIME,
    user_id VARCHAR(255),
    user_name VARCHAR(255),
    user_screen_name VARCHAR(255),
    text TEXT,
    lang VARCHAR(10),
    retweet_count INT,
    favorite_count INT,
    reply_count INT,
    quote_count INT,
    view_count INT,
    place_id VARCHAR(255),
    place_name VARCHAR(255),
    place_full_name VARCHAR(255),
    place_country VARCHAR(255),
    place_country_code VARCHAR(10),
    url VARCHAR(512),
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scraping_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_username VARCHAR(255),
    status VARCHAR(50), -- 'success', 'failed', 'rate_limit'
    message TEXT,
    tweets_count INT DEFAULT 0,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
