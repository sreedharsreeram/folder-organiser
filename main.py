import os 
import collections
import shutil

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

def organize_files(folder_path):
    if not folder_path:
        return
    
    print(f"\nOrganizing files in: {folder_path}")
    
    
    file_mapping = collections.defaultdict(list)

    
    for file in os.listdir(folder_path):
        
        if os.path.isdir(os.path.join(folder_path, file)) or file.endswith('_files'):
            continue
            
        file_type = os.path.splitext(file)[1][1:].lower()
        if file_type:  
            file_mapping[file_type].append(file)


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
            print("Exiting program...")
            break

if __name__ == "__main__":
    main()



