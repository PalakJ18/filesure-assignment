import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import re
import math

# ---------------- CONNECT MONGODB ---------------- #
client = MongoClient("mongodb://localhost:27017/")
db = client["filesure"]
collection = db["companies"]

# ---------------- CLEAR OLD DATA ---------------- #
# Prevent duplicate entries on multiple runs
collection.delete_many({})

# ---------------- LOAD CSV ---------------- #
df = pd.read_csv("../company_records.csv")

# ---------------- CLEANING FUNCTIONS ---------------- #

# DATE PARSER
def parse_date(date):
    if pd.isna(date):
        return None
    for fmt in ("%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(str(date), fmt)
        except:
            continue
    return None

# CAPITAL CLEANER
def clean_capital(value):
    if pd.isna(value):
        return None
    value = str(value).replace(",", "").replace("■", "")
    try:
        return float(value)
    except:
        return None

# EMAIL VALIDATOR
def validate_email(email):
    if pd.isna(email):
        return {"value": None, "valid": False}
    
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return {
        "value": email,
        "valid": bool(re.match(pattern, email))
    }

# STATUS NORMALIZER
def normalize_status(status):
    if pd.isna(status):
        return None
    
    status = str(status).strip().lower()
    
    # Normalize only clear cases
    if status in ["under liq.", "under liq", "under liquidation"]:
        return "under liquidation"
    
    return status

# ---------------- APPLY CLEANING ---------------- #

df['status'] = df['status'].apply(normalize_status)
df['incorporation_date'] = df['incorporation_date'].apply(parse_date)
df['last_filing_date'] = df['last_filing_date'].apply(parse_date)
df['paid_up_capital'] = df['paid_up_capital'].apply(clean_capital)
df['email'] = df['email'].apply(validate_email)

# ---------------- CONVERT TO LIST ---------------- #

data = df.to_dict(orient="records")

# ---------------- FIX NaT / NaN ---------------- #

for record in data:
    for key, value in record.items():
        
        # Fix NaT (dates)
        if str(value) == "NaT":
            record[key] = None
        
        # Fix NaN (numbers)
        if isinstance(value, float) and math.isnan(value):
            record[key] = None

# ---------------- CREATE INDEX ---------------- #

# Helps fast filtering in API
collection.create_index([("status", 1), ("state", 1)])

# ---------------- INSERT INTO MONGODB ---------------- #

try:
    collection.insert_many(data)
    print("Data inserted successfully!")
except Exception as e:
    print("Error inserting data:", e)