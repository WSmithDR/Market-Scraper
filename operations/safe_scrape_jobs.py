import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import time
import random
from jobspy import scrape_jobs

@retry(
    stop=stop_after_attempt(3),  # Maximum 3 attempts
    wait=wait_exponential(multiplier=1, min=4, max=10),  # Exponential backoff
    retry=retry_if_exception_type(requests.exceptions.HTTPError)
)
def safe_scrape_jobs(**kwargs):
    """
    A wrapper around jobspy's scrape_jobs with retry logic and rate limiting.
    
    Args:
        **kwargs: Arguments to pass to scrape_jobs
        
    Returns:
        The result from scrape_jobs or None if all retries fail
    """
    try:
        result = scrape_jobs(**kwargs)  # Directly call the function
        # Add a random delay between requests to avoid rate limiting
        time.sleep(random.uniform(1, 3))
        return result
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            retry_after = int(e.response.headers.get('Retry-After', 5))
            print(f"Rate limited. Waiting {retry_after} seconds before retry...")
            time.sleep(retry_after)
        raise  # Re-raise to trigger retry
    except Exception as e:
        print(f"Unexpected error in safe_scrape_jobs: {str(e)}")
        raise