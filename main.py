import os 
import collections
import shutil
import hashlib

def get_folder_path():
    user_path = os.path.expanduser('~')
    
    folders = {
        '1': os.path.join(user_path, 'Desktop'),  
        '2': os.path.join(user_path, 'Documents'), 
        '3': os.path.join(user_path, 'Downloads')
    }
    
   
    print("\nWhich folder would you like to organize?")
    print("1. Desktop")
    print("2. Documents")
    print("3. Downloads")
    print("4. Custom Path")
    print("5. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '5':
            return None
        elif choice == '4':
            custom_path = input("Enter the full path to the folder: ").strip()
            if os.path.exists(custom_path) and os.path.isdir(custom_path):
                return os.path.normpath(custom_path)
            else:
                print("Invalid path. Please try again.")
        elif choice in folders:
            folder_path = os.path.normpath(folders[choice])
            if os.path.exists(folder_path):
                return folder_path
            else:
                print(f"Folder not found: {folder_path}")
                print("Please choose another option.")
        else:
            print("Invalid choice. Please try again.")

def get_file_hash(file_path):
    """Calculate MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def organize_files(folder_path):
    if not folder_path:
        return
    
    print(f"\nOrganizing files in: {folder_path}")
    
    file_mapping = collections.defaultdict(list)
    hash_mapping = {}  # Store file hashes to detect duplicates

    # First pass: Calculate hashes and identify duplicates
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        
        if os.path.isdir(file_path) or file.endswith('_files'):
            continue
            
        # Calculate file hash
        try:
            file_hash = get_file_hash(file_path)
        except Exception as e:
            print(f"Error reading {file}: {str(e)}")
            continue

        file_type = os.path.splitext(file)[1][1:].lower()
        if file_type:
            if file_hash in hash_mapping:
                print(f"Duplicate found: {file} is identical to {hash_mapping[file_hash]}")
                try:
                    os.remove(file_path)  # Remove duplicate file
                    print(f"Removed duplicate: {file}")
                    continue
                except Exception as e:
                    print(f"Error removing duplicate {file}: {str(e)}")
            else:
                hash_mapping[file_hash] = file
                file_mapping[file_type].append(file)

    # Second pass: Move unique files to type folders
    for file_type, files in file_mapping.items():
        type_folder = os.path.join(folder_path, f"{file_type}_files")
        os.makedirs(type_folder, exist_ok=True)
        
        for file in files:
            source = os.path.join(folder_path, file)
            destination = os.path.join(type_folder, file)
            try:
                shutil.move(source, destination)
                print(f"Moved {file} to {type_folder}")
            except Exception as e:
                print(f"Error moving {file}: {str(e)}")

def main():
    while True:
        folder_path = get_folder_path()
        if not folder_path:
            print("Exiting program...")
            break
            
        try:
            organize_files(folder_path)
            print("\nFile organization completed!")
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
        
       
        if input("\nWould you like to organize another folder? (y/n): ").lower() != 'y':
            print("Exiting program")
            break

if __name__ == "__main__":
    main()



