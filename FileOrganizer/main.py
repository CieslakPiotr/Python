import os
from pathlib import Path

#Lists of file types and directories names
directories_types = {
    "Pictures": [".jpeg", ".jpg", ".png"],
    "Videos": [".mov", ".mp4", ".wmv", ".mpg", ".mpeg", ".mkv"],
    "PDFs": [".pdf"],
    "Music": [".mp3", ".msv"]
}

#Map extensions in the dictionaries by using dictionary comprehension
formats_mapped_to_directories = {
    extension: directory
    for directory, extensions in directories_types.items()
    for extension in extensions
}

#Function responsible for sorting files
def organize():
    #Checks if scanned, is a directory, if yes, skip
    for entry in os.scandir():
        if entry.is_dir():
            continue
        #Put entry through {ath and get its extension
        file_path = Path(entry)
        file_format = file_path.suffix.lower()
        #If extension in formats_mapped_to_directories create a directory
        if file_format in formats_mapped_to_directories:
            directory_path = Path(formats_mapped_to_directories[file_format])
            directory_path.mkdir(exist_ok=True)
            file_path.rename(directory_path.joinpath(file_path)) #Rename path to relocate file

    #Checks for empty directory and deletes it
    for directory in os.scandir():
        if directory.is_dir():
            try:
                os.rmdir(directory)
            except:
                pass

if __name__ == "__main__":
    organize()