import json
import os
from datetime import datetime

def save_chat_export(history_data, export_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_export_{timestamp}.json"
    filepath = os.path.join(export_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(history_data, f, indent=4)
        
    return filepath