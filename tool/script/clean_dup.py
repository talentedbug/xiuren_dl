"""
Generated by Microsoft Copilot
Improved by talentedbug

Be aware of potential copyright issues

This script finds duplicate files in a given directory and removes them
"""

import os
import hashlib
import concurrent.futures

def hash_file(file_path):
    """Generates a hash for a file."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest(), file_path

def find_duplicates(directory):
    """Finds duplicate files in the given directory."""
    hashes = {}
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Generate list of files
        file_paths = [
            os.path.join(root, file_name) 
            for root, _, files in os.walk(directory) 
            for file_name in files
        ]
        
        # Process files in parallel
        future_to_file = {executor.submit(hash_file, file_path): file_path for file_path in file_paths}
        
        for future in concurrent.futures.as_completed(future_to_file):
            try:
                file_hash, file_path = future.result()
                if file_hash in hashes:
                    hashes[file_hash].append(file_path)
                else:
                    hashes[file_hash] = [file_path]
            except Exception as e:
                print(f"[Warning] Error processing file: {e}")

    return hashes

def main():
    directory = '/var/www/img/kuaishou/img'  # Replace with the path to your directory
    duplicates = find_duplicates(directory)
    
    if duplicates:
        print("[Info] Duplicate files found and cleaned:")
        for file_hash, file_list in duplicates.items():
            if len(file_list) > 1:
                print(f"[Info] {' | '.join(file_list)}")
                for file_to_remove in file_list[1:]:
                    os.remove(file_to_remove)
                    print(f"[Info] Removed: {file_to_remove}")
    else:
        print("[Info] No duplicate files found.")

if __name__ == "__main__":
    main()
