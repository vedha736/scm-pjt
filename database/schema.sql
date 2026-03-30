-- Smart Expense Tracker - Database Schema
-- File: /database/schema.sql

CREATE DATABASE IF NOT EXISTS smart_expense_tracker;
USE smart_expense_tracker;

-- Users Table
CREATE TABLE users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50)  NOT NULL UNIQUE,
    email       VARCHAR(100) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    created_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- Categories Table
CREATE TABLE categories (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(50)  NOT NULL,
    icon        VARCHAR(20),
    color       VARCHAR(10),
    user_id     INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Expenses Table
CREATE TABLE expenses (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    user_id       INT          NOT NULL,
    category_id   INT,
    title         VARCHAR(100) NOT NULL,
    amount        DECIMAL(10,2) NOT NULL,
    date          DATE         NOT NULL,
    description   TEXT,
    payment_mode  ENUM('cash','card','upi','netbanking') DEFAULT 'cash',
    created_at    TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Budgets Table
CREATE TABLE budgets (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT           NOT NULL,
    category_id INT,
    amount      DECIMAL(10,2) NOT NULL,
    month       INT           NOT NULL,
    year        INT           NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Default Categories (Seed Data)
INSERT INTO categories (name, icon, color, user_id) VALUES
('Food',        '🍔', '#FF6B6B', NULL),
('Transport',   '🚗', '#4ECDC4', NULL),
('Shopping',    '🛍️', '#45B7D1', NULL),
('Bills',       '💡', '#FFA07A', NULL),
('Health',      '💊', '#98D8C8', NULL),
('Education',   '📚', '#7B68EE', NULL),
('Entertainment','🎬', '#FFD700', NULL),
('Other',       '📦', '#C0C0C0', NULL);
