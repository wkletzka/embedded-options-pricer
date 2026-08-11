import finnhub
import os

# Grab API key from environment var
api_key = os.getenv("FINNHUB_API_KEY")

# Setup client
finnhub_client = finnhub.Client(api_key=api_key)

# Company news
news = finnhub_client.company_news('NBIS', _from="2026-08-06", to="2026-08-10")

for article in news:
    print(article)
    print('\n')