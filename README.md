# FileSure Assignment – Tech Operations & Support Intern

## 📌 Overview
This project simulates a real-world data pipeline and API system.

The goal was to:
- Ingest messy CSV data into MongoDB
- Clean and normalize the data
- Build an API using Node.js
- Display data via a minimal frontend
- Clearly explain decisions and trade-offs

---

## 🛠️ Tech Stack
- **Python** – Data ingestion & cleaning (Pandas, PyMongo)
- **MongoDB** – Database
- **Node.js + Express** – API layer
- **Mongoose** – Schema modeling
- **HTML / JavaScript** – Basic frontend

---

## 📂 Project Structure
filesure-assignment/
│
├── data-ingestion/
│ └── ingest.py
│
├── backend/
│ ├── server.js
│ └── models/
│ └── Company.js
│
├── frontend/
│ └── index.html
│
├── screenshots/
│ ├── companies.png
│ ├── filter.png
│ └── summary.png
│
├── company_records.csv
├── package.json
└── README.md

## ⚙️ Setup Instructions

### 1. Install Dependencies
npm install
### 2. Start MongoDB
mongod
### 3. Run the Project
npm run start

### API Endpoints
All companies:
http://localhost:3000/companies
Filter:
http://localhost:3000/companies/filter?status=active&state=Delhi
Summary:
http://localhost:3000/companies/summary

## Screenshots of the API responses are included in the repository for reference.
