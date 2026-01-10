import os


def main():
    # get all folders in Desktop/Manga_downloads/
    desktop_path = os.path.expanduser("~/Desktop")
    manga_downloads_path = os.path.join(desktop_path, "Manga_downloads", "pdfs")

    if not os.path.exists(manga_downloads_path):
        print("Manga_downloads folder does not exist.")
        return

    folders = [
        f
        for f in os.listdir(manga_downloads_path)
        if os.path.isdir(os.path.join(manga_downloads_path, f))
    ]

    # for each folder check their content recursively and if they have pdf files with same name than folder move the pdf to the parent folder and delete the folder
    for folder in folders:
        check_folder(os.path.join(manga_downloads_path, folder))


def check_folder(folder_path):
    files = os.listdir(folder_path)
    pdf_files = [f for f in files if f.endswith(".pdf")]
    folder = os.path.basename(folder_path)
    # check if folder is empty
    if not files:
        os.rmdir(folder_path)
        return

    if pdf_files and pdf_files[0] == f"{folder}.pdf":
        source_pdf = os.path.join(folder_path, pdf_files[0])
        destination_pdf = os.path.join(folder_path, "..", f"{folder}.pdf")
        os.rename(source_pdf, destination_pdf)
        print(
            f"Moved {source_pdf} to {destination_pdf} and deleted folder {folder_path}"
        )

    # check subfolders
    subfolders = [
        f
        for f in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, f))
    ]
    for subfolder in subfolders:
        check_folder(os.path.join(folder_path, subfolder))


if __name__ == "__main__":
    main()
