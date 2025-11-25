from datetime import datetime
from pathlib import Path

def setup_output_directory(base_dir="../data/raw"):
    """
    Crea un directorio de salida con timestamp (usando pathlib) 
    y devuelve un objeto Path.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 2. Usar pathlib para crear la ruta
    output_dir = Path(base_dir) / f"jobs_{timestamp}"
    
    # 3. Usar .mkdir() del objeto Path
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 4. Devolver el objeto Path (no un string)
    return output_dir