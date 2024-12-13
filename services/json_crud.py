import json
import os

def load_json(json_file=None, *args):
    def callback(file_path):
        load_json(file_path)

    if json_file is None:
        raise ValueError("json_file parameter must be provided")

    # Ensure the directory exists
    dir_name = os.path.dirname(json_file)
    if dir_name:  # Check if the directory name is not empty
        os.makedirs(dir_name, exist_ok=True)

    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {json_file}")
        create_default_json(json_file, callback)
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        create_default_json(json_file, callback)
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        create_default_json(json_file, callback)
        return {}

def save_json(json_file=None, data=None, *args):
    def callback(file_path):
        save_json(file_path, data)

    if json_file is None or data is None:
        raise ValueError("json_file and data parameters must be provided")

    # Ensure the directory exists
    dir_name = os.path.dirname(json_file)
    if dir_name:  # Check if the directory name is not empty
        os.makedirs(dir_name, exist_ok=True)

    try:
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            print(f"Data successfully saved to {json_file}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")
        create_default_json(json_file, callback)

def create_default_json(file_path, callback):
    default_data = {}
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(default_data, file, ensure_ascii=False, indent=4)
        print(f"Created an empty JSON file at {file_path}")
        callback(file_path)
    except Exception as e:
        print(f"Error creating default JSON file: {e}")
        callback(file_path)

# Example usage
if __name__=='__main__':
    data_to_save = {"name": "John", "age": 30, "city": "New York"}
    save_json('data.json', data_to_save)

    loaded_data = load_json('data.json')
    print(loaded_data)
