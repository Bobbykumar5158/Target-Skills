import json
import os

def read_data(FILE):

    if not os.path.exists(FILE):
        return {}
    
    try:
        with open(FILE, "r", encoding="utf-8") as file:
            return json.load(file)
            
    except json.JSONDecodeError:
        print(f"Warning: {FILE} was corrupted. Returning empty dataset.")
        return {}
    
    except Exception as e:
        print(f"Error reading {FILE}: {e}")
        return {}
    
def write_data(FILE,data):

    try:
        with open(FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    
    except Exception as e:
        print(f"Error writing to {FILE}: {e}")
        return False