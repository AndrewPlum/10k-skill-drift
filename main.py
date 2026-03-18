import pandas as pd
import requests
import os

user_name = os.getenv("SEC_USER_NAME", "Default Name")
user_email = os.getenv("SEC_USER_EMAIL", "default@email.com")

HEADERS = {"User-Agent": f"{user_name} ({user_email})"}

def get_cik_from_ticker(ticker):
    """
    Fetch CIK for a given ticker.
    """
    company_tickers_url = "https://www.sec.gov/files/company_tickers.json"
    response = requests.get(company_tickers_url, headers=HEADERS)
    data = response.json()
    for key, val in data.items():
        if val["ticker"] == ticker.upper():
            return str(val["cik_str"]).zfill(10)
    return None

def get_latest_10k_url(cik):
    """
    Get the URL for the most recent 10-K filing.
    """
    submissions_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    response = requests.get(submissions_url, headers=HEADERS)
    data = response.json()

    recent_filings = data["filings"]["recent"]
    for i, form in enumerate(recent_filings["form"]):
        if form == "10-K":
            accession_num = recent_filings["accessionNumber"][i].replace("-","")
            primary_doc = recent_filings["primaryDocument"][i]
            return f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_num}/{primary_doc}"
    return None

if __name__ == "__main__":
    ticker = "WMT" 
    #ticker = "AMZN"
    cik = get_cik_from_ticker(ticker)

    if cik:
        company_10k_url = get_latest_10k_url(cik)
        print(f"Latest 10-K for {ticker}: {company_10k_url}")
        
        response = requests.get(company_10k_url, headers=HEADERS)
        raw_html = response.text
        