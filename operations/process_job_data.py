import pandas as pd 
import numpy as np
import json
from datetime import datetime
from .convert_dates_to_datetime import convert_dates_to_datetime
from .connect_to_mongodb import connect_to_mongodb

def process_and_save_jobs(all_jobs_dfs, output_dir):
    """
    Process job data and save to MongoDB with error handling and backup.
    
    Args:
        all_jobs_dfs (list): List of DataFrames containing job data
        output_dir (str): Directory to save backup files
    """
    if not all_jobs_dfs:
        print("\nNo jobs were found.")
        return

    combined_jobs = combine_job_dataframes(all_jobs_dfs)
    jobs_data = combined_jobs.to_dict('records')
    
    db_connection = connect_to_mongodb()
    
    if db_connection is not None:
        process_with_mongodb(db_connection, jobs_data, output_dir)  # Pass output_dir here
    else:
        print("❌ Could not connect to MongoDB. Saving to JSON instead...")
    
    save_backup(combined_jobs, output_dir)

def combine_job_dataframes(job_dfs):
    """Combine and deduplicate job DataFrames."""
    if not job_dfs:
        return pd.DataFrame()
    return pd.concat(job_dfs, ignore_index=True).drop_duplicates(
        subset=['job_url', 'title', 'company']
    )

def process_with_mongodb(db_connection, jobs_data, output_dir):  # Add output_dir parameter
    """Process and save jobs to MongoDB with error tracking."""
    client = db_connection['client']
    collection = db_connection['collection']
    
    stats = {
        'inserted': 0,
        'updated': 0,
        'skipped': 0,
        'errors': []
    }
    
    try:
        for job in jobs_data:
            process_single_job(job, collection, stats)
        
        print_processing_summary(stats)
        log_errors(stats, output_dir)
        
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        raise
    finally:
        client.close()

def process_single_job(job, collection, stats):
    """Process and upsert a single job into MongoDB."""
    try:
        processed_job = process_job_data(job)
        
        result = collection.update_one(
            {"job_url": processed_job["job_url"]},
            {
                "$set": processed_job,
                "$setOnInsert": {"created_at": datetime.now()}
            },
            upsert=True
        )
        
        if result.upserted_id:
            stats['inserted'] += 1
        elif result.modified_count > 0:
            stats['updated'] += 1
        else:
            stats['skipped'] += 1
            
    except Exception as e:
        error_info = {
            "job_url": job.get("job_url", "unknown"),
            "error": str(e)
        }
        stats['errors'].append(error_info)
        print(f"⚠️ Error processing job {error_info['job_url']}: {error_info['error']}")

def print_processing_summary(stats):
    """Print a summary of the job processing results."""
    print("\n" + "="*50)
    print("📊 Job Processing Summary")
    print("="*50)
    print(f"✅ New jobs inserted: {stats['inserted']}")
    print(f"🔄 Existing jobs updated: {stats['updated']}")
    print(f"⏩ Jobs unchanged (skipped): {stats['skipped']}")
    print(f"❌ Errors: {len(stats['errors'])}")

def log_errors(stats, output_dir):
    """Log errors to console and save to file if there are any."""
    if not stats['errors']:
        return
        
    print("\n⚠️  Errors encountered:")
    for i, error in enumerate(stats['errors'][:5], 1):
        print(f"{i}. {error['job_url']}: {error['error']}")
    
    if len(stats['errors']) > 5:
        print(f"... and {len(stats['errors']) - 5} more errors")
    
    error_file = f"{output_dir}/import_errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(error_file, 'w') as f:
        json.dump(stats['errors'], f, indent=2)
    print(f"\n📝 Full error log saved to: {error_file}")

def save_backup(combined_jobs, output_dir):
    """Save job data to a JSON backup file."""
    if combined_jobs is None or combined_jobs.empty:
        print("⚠️ No data to save for backup.")
        return
        
    json_filename = f"{output_dir}/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    combined_jobs.to_json(json_filename, orient='records', indent=4, date_format='iso')
    print(f"📦 Backup saved to: {json_filename}")

def process_job_data(job):
    """Process a single job dictionary for MongoDB insertion."""
    # Make a copy to avoid modifying the original
    processed_job = job.copy()
    
    # Convert any numpy types to native Python types
    for key, value in processed_job.items():
        if isinstance(value, (np.generic, np.ndarray)):
            processed_job[key] = value.item() if value.size == 1 else value.tolist()
    
    # Ensure date fields are properly formatted
    date_fields = ['date_posted', 'application_deadline', 'last_updated']
    for field in date_fields:
        if field in processed_job and processed_job[field]:
            try:
                # If it's already a datetime object, convert to ISO format string
                if hasattr(processed_job[field], 'isoformat'):
                    processed_job[field] = processed_job[field].isoformat()
                # If it's a string that represents a date, convert to datetime first
                elif isinstance(processed_job[field], str):
                    processed_job[field] = pd.to_datetime(processed_job[field]).isoformat()
            except Exception as e:
                print(f"⚠️ Error processing date field '{field}': {str(e)}")
                processed_job[field] = None
    
    return processed_job