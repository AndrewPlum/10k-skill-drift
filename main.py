import pandas as pd
import re

import extractor
import analyzer

if __name__ == "__main__":
    ticker = "WMT" 
    cik = extractor.get_cik_from_ticker(ticker)

    if cik:
        company_10k_url = extractor.get_latest_10k_url(cik)
        print(f"Latest 10-K for {ticker}: {company_10k_url}")
        
        raw_html = extractor.fetch_10k_content(company_10k_url)

        item1_text = extractor.extract_item1(raw_html)

        with open(f"{ticker}10k_item1.txt", "w", encoding="utf-8") as file:
            file.write(item1_text)

        human_capital_text = extractor.extract_human_capital_text(raw_html)

        with open(f"{ticker}_human_capital.txt", "w", encoding="utf-8") as file:
            file.write(human_capital_text)

        # CSV downloaded from the O*net database - could connect to the API later for live data but that was demonstrated previously
        # and this serves our purposes fine
        hot_tech_skills_df = pd.read_csv("Hot_Technologies.csv")
        tech_skills_set = set(hot_tech_skills_df["Hot Technology"].tolist())

        match = re.search(rf"{re.escape(ticker)}-(\d{{4}})(\d{{2}})(\d{{2}})", company_10k_url, re.IGNORECASE) # assumes the year is 4 digits and format of url does not change
        if match:
            year = match.group(1)
            """# Uncomment if you use the other dates
            month = match.group(2)
            day = match.group(3)
            date_str = f"{year}-{month}-{day}"
            #"""
        else:
            print("Date not found in URL.")

        llm_skill_response_json = analyzer.analyze_labor_drift(human_capital_text, ticker, year)
        print(llm_skill_response_json)