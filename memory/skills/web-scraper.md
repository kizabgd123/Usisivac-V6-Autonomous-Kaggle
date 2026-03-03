---
name: web-scraper
description: Extracts structured data from web pages for market intelligence and lead generation.
status: active
priority: high
tags: [scraping, data-extraction, python, beautifulsoup]
created: 2026-01-02
type: global-skill
---

# Web Scraper Skill

## Purpose
To autonomously browse, extract, and structure data from target URLs. This skill is the "eyes" of the automated lead generation and market intelligence workflows.

## Capabilities
1.  **Fetch**: Retrieve HTML content from a given URL.
2.  **Parse**: Extract specific data points (prices, emails, company names) using CSS selectors or XPath.
3.  **Structure**: Convert unstructured HTML into clean JSON.
4.  **Handle Pagination**: (Optional) Follow 'Next' buttons to scrape multiple pages.

## Dependencies
- `requests` or `selenium` (for dynamic content)
- `beautifulsoup4`
- `lxml`

## Usage Template (Python)

```python
import requests
from bs4 import BeautifulSoup
import json

def scrape_url(url, schema):
    """
    Scrapes a URL and extracts data based on the provided schema.
    
    Args:
        url (str): The URL to scrape.
        schema (dict): A dictionary mapping field names to CSS selectors.
                       Example: {"price": ".product-price", "title": "h1"}
    
    Returns:
        dict: Extracted data.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        data = {}
        
        for field, selector in schema.items():
            element = soup.select_one(selector)
            data[field] = element.get_text(strip=True) if element else None
            
        return data
        
    except Exception as e:
        return {"error": str(e)}

# Example Usage
# schema = {"company_name": ".org-top-card-summary__title", "website": ".org-top-card-primary-actions__action"}
# print(scrape_url("https://linkedin.com/company/example", schema))
```

## Safety & Compliance
- ✅ **Respect robots.txt**: Always check if scraping is allowed.
- ⛔ **Rate Limiting**: Do not send more than 1 request per second to the same domain.
- ⛔ **PII**: Do not scrape personal private data without consent.
