#!/usr/bin/env python3

"""
Removes all the entries from the $HOME directory, that are either:
1. Files
2. Directories that do not contain .git subdirectory
"""

import shutil
import sys
import pathlib

ALLOWED_FILE_PATHS = [
    ".bashrc", 
    ".bash_profile",
    ".bash_login",
    ".bash_history",
    ".bash_logout",
    ".profile",
    ".gitconfig",
    ".viminfo",
    ".sudo_as_admin_successful",
]
ALLOWED_DIR_PATHS = [
    ".local",
    ".cache",
    ".config",
    ".docker",
    ".dotnet",
    ".gnupg",
    ".go",
    ".java",
    ".npm",
    ".pki",
    ".snap",
    ".ssh",
    ".vscode",
    ".vim",
    "snap",
    "Documents", # For cringy obsidian
    "Screenshots" # For cringy ubuntu screenshot tool
]

FILE_COLOR_CODE = "\033[0m"
DIR_COLOR_CODE = "\033[35m"
DEFAULT_COLOR_CODE = "\033[0m"

def ask_for_confirmation(prompt: str) -> bool:
    print(f"{prompt} [y/n]: ", end="")
    
    answer = input()
    return answer == "y" or answer == "Y"

def should_remove_file(file_path: pathlib.Path) -> bool:
    if file_path.name in ALLOWED_FILE_PATHS:
        return False

    return True

def should_remove_directory(dir_path: pathlib.Path) -> bool:
    if dir_path.name in ALLOWED_DIR_PATHS:
        return False

    git_subdir = dir_path / '.git'
    if git_subdir.exists() and git_subdir.is_dir():
        return False
    
    return True

def main():
    home_dir = pathlib.Path.home()
    
    if not home_dir.exists() or not home_dir.is_dir():
        print("Home directory not found or is not a directory")
        sys.exit(1)
    
    file_paths = []
    dir_paths = []
    
    try:
        for item in home_dir.iterdir():
            if item.is_file():
                if should_remove_file(item):
                    file_paths.append(item)

            elif item.is_dir():
                if should_remove_directory(item):
                    dir_paths.append(item)
    except Exception as e:
        print(f"Failed to inspect home directory: {e}")
        sys.exit(1)

    if len(file_paths) == 0 and len(dir_paths) == 0:
        print(f"No files to remove")
        sys.exit(0)
    
    dir_names = "  ".join(list(map(lambda x : x.name, dir_paths)))
    file_names = "  ".join(list(map(lambda x : x.name, file_paths)))

    prompt = f"{DIR_COLOR_CODE}{dir_names}  {FILE_COLOR_CODE}{file_names}{DEFAULT_COLOR_CODE}\nThe following entries will be removed; Proceed?"
    if not ask_for_confirmation(prompt):
        sys.exit(0)

    removed_files_quantity = 0
    removed_dirs_quantity = 0


    for file_path in file_paths:
        try:
            file_path.unlink()
            removed_files_quantity += 1
        except Exception as e:
            print(f"Failed to remove file {file_path.name}: {e}")

    for dir_path in dir_paths:
        try:
            shutil.rmtree(dir_path)
            removed_dirs_quantity += 1
        except Exception as e:
            print(f"Failed to remove dir {dir_path.name}: {e}")

    
    print(f"Removed total {removed_dirs_quantity} directories and {removed_files_quantity} files")

if __name__ == "__main__":
    main()
