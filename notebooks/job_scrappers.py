from jobspy import scrape_jobs

def scrape_glassdoor_jobs(search_term, location, num_pages=10, results_wanted=200):
    """Scrape job listings from Glassdoor"""
    print(f"Scraping {results_wanted} {search_term} jobs in {location}...")
    
    jobs = scrape_jobs(
        site_name="glassdoor",
        search_term=search_term,
        location=location,
        results_wanted=results_wanted,
        hours_old=720,  # Last 30 days
        num_pages=num_pages,
        country_indeed='Argentina'  # Focus on Argentina
    )
    
    return jobs

