import os
import tkinter as tk
from tkinter import filedialog, ttk
from main import organize_files

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        organize_files(folder_selected)

def main():
    root = tk.Tk()
    root.title("File Organizer")
    root.geometry("450x400")
    root.configure(bg="#f0f0f0")
    
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=10)
    
    tk.Label(root, text="Select a folder to organize:", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=15)
    
    user_path = os.path.expanduser('~')
    folders = {
        "Desktop": os.path.join(user_path, "Desktop"),
        "Documents": os.path.join(user_path, "Documents"),
        "Downloads": os.path.join(user_path, "Downloads")
    }
    
    for name, path in folders.items():
        ttk.Button(root, text=name, command=lambda p=path: organize_files(p)).pack(pady=5)
    
    ttk.Button(root, text="Choose Custom Folder", command=browse_folder).pack(pady=10)
    ttk.Button(root, text="Exit", command=root.quit).pack(pady=30)
    
    root.mainloop()

if __name__ == "__main__":
    main()