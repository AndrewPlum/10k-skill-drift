import requests
from bs4 import BeautifulSoup
import re

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

def extract_item1(raw_html):
    """
    Extracts the item 1 section from the passed in raw html.
    """
    start_pattern = re.compile(r">item(\s|&#160;|&nbsp;)1(\.|\s|&#160;|&nbsp;)<", re.IGNORECASE)
    end_pattern = re.compile(r">item(\s|&#160;|&nbsp;)2(\.|\s|&#160;|&nbsp;)<", re.IGNORECASE)

    start_matches = list(start_pattern.finditer(raw_html))
    end_matches = list(end_pattern.finditer(raw_html))

    if not start_matches or not end_matches:
        return "Could not find Item 1 or Item 2 anchors."
    
    """# Uncomment to print matches
    for start_match in start_matches:
        print(start_match)
    for end_match in end_matches:
        print(end_match)
    #"""    

    first_item2_match = end_matches[-1]
    end_index = first_item2_match.start()

    start_index = None
    for match in start_matches:
        if match.start() < end_index:
            start_index = match.start()
        else:
            break

    if start_index is None:
        return "Logic error: No Item 1 found before Item 2."

    item1_content_raw = raw_html[start_index:end_index]
    soup = BeautifulSoup(item1_content_raw, 'html.parser')

    return soup.get_text(separator=" ", strip=True)

def extract_human_capital_text(raw_html):
    start_pattern = re.compile(r">human(\s|&#160;|&nbsp;)capital", re.IGNORECASE)
    end_pattern = re.compile(r">item(\s|&#160;|&nbsp;)1A(\.|\s|&#160;|&nbsp;)<", re.IGNORECASE)

    start_matches = list(start_pattern.finditer(raw_html))
    end_matches = list(end_pattern.finditer(raw_html))

    if not start_matches or not end_matches:
        return "Could not find Item 1 or Item 2 anchors."
    
    """# Uncomment to print matches
    for start_match in start_matches:
        print(start_match)
    for end_match in end_matches:
        print(end_match)
    #"""    

    first_item2_match = end_matches[-1]
    end_index = first_item2_match.start()

    start_index = None
    for match in start_matches:
        if match.start() < end_index:
            start_index = match.start()
        else:
            break

    if start_index is None:
        return "Logic error: No Item 1 found before Item 2."

    item1_content_raw = raw_html[start_index:end_index]
    soup = BeautifulSoup(item1_content_raw, 'html.parser')

    return soup.get_text(separator=" ", strip=True)