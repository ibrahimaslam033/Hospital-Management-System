CREATE DATABASE IF NOT EXISTS hospital;

USE hospital;

-- =========================
-- PATIENTS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS patients (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    disease VARCHAR(100)
);

-- =========================
-- DOCTORS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS doctors (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    specialization VARCHAR(100)
);

-- =========================
-- ASSIGNMENTS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS assignments (
    patient_id INT,
    doctor_id INT
);

-- =========================
-- OPTIONAL: BILL TABLE
-- =========================
CREATE TABLE IF NOT EXISTS bills (
    patient_id INT,
    amount INT,
    details VARCHAR(255)
);