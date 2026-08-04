import json
import os


# -----------------------------------------
# Load JSON File
# -----------------------------------------

def load_json(file_path, default_data=None):

    if default_data is None:
        default_data = []

    # Create file if it doesn't exist
    if not os.path.exists(file_path):

        with open(file_path, "w") as file:
            json.dump(default_data, file, indent=4)

        return default_data

    try:

        with open(file_path, "r") as file:

            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):

        print(f"\nWarning: {file_path} was empty or corrupted.")
        print("Creating a new file with default values.\n")

        with open(file_path, "w") as file:

            json.dump(default_data, file, indent=4)

        return default_data


# -----------------------------------------
# Save JSON File
# -----------------------------------------

def save_json(file_path, data):

    with open(file_path, "w") as file:

        json.dump(data, file, indent=4)


# -----------------------------------------
# Check File Exists
# -----------------------------------------

def file_exists(file_path):

    return os.path.exists(file_path)


# -----------------------------------------
# Delete File
# -----------------------------------------

def delete_file(file_path):

    if os.path.exists(file_path):

        os.remove(file_path)

        return True

    return False
