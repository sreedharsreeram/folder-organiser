import os
import collections
import shutil
import hashlib
from tkinter import messagebox

def get_file_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def organize_files(folder_path):
    if not folder_path:
        return
    
    file_mapping = collections.defaultdict(list)
    hash_mapping = {}  
    system_files = {'.DS_Store', 'Thumbs.db', 'desktop.ini'}
    
    for file in os.listdir(folder_path):
        if file in system_files or file.startswith('.') or file.endswith('_files'):
            continue
        
        file_path = os.path.join(folder_path, file)
        if os.path.isdir(file_path):
            continue
            
        if not os.access(file_path, os.R_OK):
            continue
        
        try:
            file_hash = get_file_hash(file_path)
            file_type = os.path.splitext(file)[1][1:].lower()
            
            if file_type:
                if file_hash in hash_mapping:
                    os.remove(file_path)
                else:
                    hash_mapping[file_hash] = file
                    file_mapping[file_type].append(file)
        except:
            continue

    for file_type, files in file_mapping.items():
        type_folder = os.path.join(folder_path, f"{file_type}_files")
        try:
            os.makedirs(type_folder, exist_ok=True)
            for file in files:
                shutil.move(os.path.join(folder_path, file), os.path.join(type_folder, file))
        except:
            continue
    
    messagebox.showinfo("Success", "Files have been organized successfully!")