from jobspy import scrape_jobs
#from operations import (
#   hours_old_since_2025
#)
import itertools

def run_scraper(
    sites=["indeed","glassdoor"],
    search_terms=None,
    locations=None,
    countries=None,
    results_wanted=1000,
    hours_old=None
):
    if search_terms is None:
        search_terms = ["Fintech","EdTech","Future of Work"]
    if locations is None:
        locations = ["Remote"]
    if countries is None:
        countries = ["Australia","Austria"]

    all_jobs = []
    for country, term in itertools.product(countries, search_terms):
        print(f"Buscando en {country} por {term}")
        try:
            df = scrape_jobs(
                site_name=sites,
                search_term=term,
                location=locations[0],
                country_indeed=country,
                results_wanted=results_wanted,
                hours_old=hours_old
            )
            if df is not None and not df.empty:
                print(f"✅ Encontrados {len(df)} trabajos para {term} en {country}")
                all_jobs.append(df)
        except Exception as e:
            print(f"❌ Error scraping {term} @ {country}: {e}")

    return all_jobs if all_jobs else None

