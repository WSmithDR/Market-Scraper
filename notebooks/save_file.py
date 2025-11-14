import os
from datetime import datetime
import json

def setup_output_directory(base_dir="data/raw"):
    """Create output directory with timestamp if it doesn't exist"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(base_dir, f"jobs_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir
