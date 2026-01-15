CREATE DATABASE IF NOT EXISTS ictf;
USE ictf;

CREATE TABLE IF NOT EXISTS games (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    state VARCHAR(50) DEFAULT 'RUNNING',
    status VARCHAR(50) DEFAULT 'ACTIVE',
    current_round INT DEFAULT 1
);

CREATE TABLE IF NOT EXISTS rounds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT,
    number INT,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS teams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    ip_address VARCHAR(45)
);

-- Chèn dữ liệu mẫu để GameBot có mục tiêu hoạt động
INSERT INTO games (name, state, status, current_round) VALUES ('ictf_2026', 'RUNNING', 'ACTIVE', 1);
