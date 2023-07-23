import os
import shutil
from collections import defaultdict
import concurrent.futures

def collect_picture_files(src_dir, dest_dir):
    picture_extensions = {'.jpg', '.jpeg', '.png'}
    file_groups = defaultdict(list)

    excluded_dirs = {'WhatsApp', 'SomeOtherApp'}  # Use a set for faster lookup
    excluded_dirs_lower = {dir_name.lower() for dir_name in excluded_dirs}

    def is_picture_file(filename):
        _, ext = os.path.splitext(filename)
        return ext.lower() in picture_extensions

    def traverse_directory(dir_path):
        for root, _, files in os.walk(dir_path):
            for filename in files:
                if is_picture_file(filename):
                    src_path = os.path.join(root, filename)
                    file_groups[filename].append(src_path)

    def copy_file(src_path, dest_dir):
        dest_path = os.path.join(dest_dir, os.path.basename(src_path))
        shutil.copy2(src_path, dest_path)
        print(f"Copied: {src_path} -> {dest_path}")

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Concurrently traverse directories
        for root, _, _ in os.walk(src_dir):
            executor.submit(traverse_directory, root)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Concurrently copy files
        for filename, files in file_groups.items():
            for src_path in files:
                executor.submit(copy_file, src_path, dest_dir)

if __name__ == "__main__":
    # Get the directory where the script is located.
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Create the 'Pictures' folder in the script's directory.
    destination_directory = os.path.join(script_directory, 'Pictures')

    try:
        collect_picture_files(os.path.expanduser("~"), destination_directory)
        print("All picture files have been copied to the Pictures folder.")
    except Exception as e:
        print(f"An error occurred: {e}")
