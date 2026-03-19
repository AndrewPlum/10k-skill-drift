import pandas as pd
import requests
import os
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import warnings
import re

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

def extract_item_1(soup):
    # 1. Find the "Item 1" anchor
    # We look for a tag that contains 'ITEM 1' specifically 
    # and isn't just a link in the Table of Contents.
    start_node = None
    all_fonts = soup.find_all('font')
    
    for font in all_fonts:
        text = font.get_text(strip=True).upper()
        # Look for the exact match; usually bold/underlined in filings
        if text == "ITEM 1." or text == "ITEM 1":
            # Ensure it's not the Table of Contents (often in an <a> tag)
            if not font.find_parent('a'):
                start_node = font
                break
                
    if not start_node:
        return "Could not find Item 1 start."

    # 2. Traverse siblings to collect content
    content = []
    # Move up to a high-level parent (like the <div> or <p> containing the table)
    current_node = start_node.find_parent('div') 
    
    while current_node:
        text_content = current_node.get_text(separator=" ", strip=True)
        
        # 3. Stop condition: Reaching Item 2
        # Check if "ITEM 2" appears at the start of a block
        if "ITEM 2" in text_content.upper()[:20]:
            break
            
        content.append(text_content)
        current_node = current_node.find_next_sibling()

    return "\n\n".join(content)

if __name__ == "__main__":
    ticker = "WMT" 
    #ticker = "AMZN"
    cik = get_cik_from_ticker(ticker)

    if cik:
        company_10k_url = get_latest_10k_url(cik)
        print(f"Latest 10-K for {ticker}: {company_10k_url}")
        
        response = requests.get(company_10k_url, headers=HEADERS)
        raw_html = response.text
        
        """
        start_index = raw_html.find("Item 1.") 
        end_index = raw_html.find("Item 2.") 
        labor_context = raw_html[start_index:end_index]
        
        #print(labor_context)
        filename = "labor_context_preview.html"

        # Save the extracted string as an HTML file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(labor_context)
        """

        soup = BeautifulSoup(response.content, 'html.parser')

        business_section = extract_item_1(soup)
        print(business_section[:1000])