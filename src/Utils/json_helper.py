import re
import json

def extract_json_from_text(text):
    # Try to find a JSON array or object by looking for something 
    # starting with [ and ending with ], or { and ending with }.
    # We'll try arrays first and if that fails, try objects.
    
    # Pattern for extracting a JSON array
    array_pattern = r'(\[[\s\S]*?\])'
    # Pattern for extracting a JSON object
    object_pattern = r'(\{[\s\S]*?\})'
    
    # Attempt to find an array
    array_match = re.search(array_pattern, text)
    if array_match:
        candidate = array_match.group(1).strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass  # If this fails, we'll try the object pattern

    # Attempt to find an object
    object_match = re.search(object_pattern, text)
    if object_match:
        candidate = object_match.group(1).strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass
    
    # If no valid JSON is found, return None
    return None