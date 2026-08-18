# Services reference

This document lists the active service modules under `src/services/` and their purpose.

## Image conversion

- `image_converter_service.py`
- Contains the conversion logic for image folders into PDF-ready output.
- Depends on the image converter interface and file system utilities.

## Manga downloader

- `manga_downloader_service.py`
- Performs the scraper-driven manga download workflow.
- Uses a `MangaScraper` instance and page iteration logic.

## PDF creation

- `pdf_creator_service.py`
- Builds the final PDF from a converted image folder.
- Accepts the PDF metadata and output directory.

## WebDAV upload

- `webdav_service.py`
- Verifies the local PDF exists and uploads it to the configured remote WebDAV location.
- Supports a check-before-upload flow.

## Shared infrastructure services

- `src/core/services/file_manager.py`
- `src/core/services/error_handler.py`
- `src/core/services/user_feedback_handler.py`

These are supporting services used across the application.
