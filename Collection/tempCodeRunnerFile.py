import os

def check_directory_permissions(path):
    directories = path.split(os.path.sep)
    current_path = directories[0]
    for directory in directories[1:]:
        current_path = os.path.join(current_path, directory)
        if not os.access(current_path, os.R_OK | os.W_OK | os.X_OK):
            print(f"Insufficient permissions for directory: {current_path}")
            return False
    print("All directories have sufficient permissions.")
    return True

# Example directory path
directory_path = "../Database/card_collection.db"

# Check permissions for each stage in the directory path
check_directory_permissions(directory_path)