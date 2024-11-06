from imagededup.methods import PHash
import os
import shutil
from pathlib import Path
from tqdm import tqdm

def find_and_remove_duplicates(directory='.', move_to_trash=True):
    """
    Find and remove duplicate images in the specified directory using PHash method.
    
    Args:
        directory (str): Directory to scan for duplicates (default: current directory)
        move_to_trash (bool): If True, moves files to a 'duplicates' folder instead of deleting
    """
    # Create PHash object
    phasher = PHash()
    
    # Get the encodings for all images in the directory
    print("Generating image hashes...")
    encodings = phasher.encode_images(image_dir=directory)
    
    # Find duplicates using the correct method
    print("Finding duplicates...")
    files_to_remove = phasher.find_duplicates_to_remove(encoding_map=encodings)
    
    if not files_to_remove:
        print("No duplicates found!")
        return
    
    print(f"\nFound {len(files_to_remove)} duplicate files")
    
    # Create duplicates directory if moving files
    if move_to_trash:
        duplicates_dir = os.path.join(directory, 'duplicates')
        os.makedirs(duplicates_dir, exist_ok=True)
    
    # Process duplicates
    print("\nProcessing duplicates...")
    for file in tqdm(files_to_remove):
        file_path = os.path.join(directory, file)
        if os.path.exists(file_path):
            try:
                if move_to_trash:
                    shutil.move(file_path, os.path.join(duplicates_dir, file))
                else:
                    os.remove(file_path)
            except Exception as e:
                print(f"Error processing {file}: {str(e)}")
    
    print("\nOperation completed!")
    if move_to_trash:
        print(f"Duplicate files have been moved to: {duplicates_dir}")
    else:
        print("Duplicate files have been deleted")
    
    # Print some statistics
    print(f"\nStatistics:")
    print(f"Total images processed: {len(encodings)}")
    print(f"Duplicates found and processed: {len(files_to_remove)}")
    print(f"Unique images remaining: {len(encodings) - len(files_to_remove)}")

if __name__ == "__main__":
    # You can change these parameters as needed
    current_dir = '.'
    move_to_trash = True  # Set to False to delete files instead of moving them
    
    find_and_remove_duplicates(current_dir, move_to_trash)
