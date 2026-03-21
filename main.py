import extractor

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
