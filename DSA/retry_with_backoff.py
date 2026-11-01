import requests
import time    
import random

def retry_with_backoff(call_api, max_retries=5, backoff_factor=1):
    for attempt in range(max_retries):
        try:
            return call_api()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            ## exponential backoff like 1, 2, 4, 8, 16 seconds
            delay  = backoff_factor * (2 ** attempt)
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
            delay+= random.unform(0, 0.5) 
            # Adding jitter it prevent all failed reuqest to retry at the same time or a
            # void multiple clients retrying at the same time 
            time.sleep(delay)
            
def call_api():
    url = "https://dummyjson.com/products"
    response = requests.get(url)
    response.raise_for_status()
    
    return response.json()