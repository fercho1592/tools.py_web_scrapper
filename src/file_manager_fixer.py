from configs.dependency_injection import GetFileScrapperManager
from feature.services.file_manager import DOWNLOAD_FOLDER
from feature_interfaces.services.file_manager import IFileScrapperManager

path = DOWNLOAD_FOLDER

def fixMainFoldersName(fileManager: object):
    # Arrange Folders and group similar names

    # For Each group
        # Ask user if have to Group folders or keep as used
        # If YES
            # Create a new Folder with correct name
            # Move all elements to new folder
    pass

def fixFilesNames():
    fileManager = GetFileScrapperManager(path, None)
    # Get All Folders in main folder

    fixMainFoldersName({})

    # For each forlder get all PDfs name whit parent folder name
    # Group similar names and folder names
    
    #P2
        # For each Group
            # Show all elements in group
            # Ask User if is same element
            # If YES
                # Ask user for main element
                # identify main element
                # delete others
                # continue

            # Ask user if group elements
            # If YES
                # Print All path of first element
                # Ask user for a {name}
                # Ask user for {artist}
                # Create new Folder with {artist}/{name}/file.pdf
    pass

if __name__ == "__main__":
    fixFilesNames()
