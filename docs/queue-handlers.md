# Queue handlers

Queue handlers live under `src/app/handlers/` and are responsible for processing queue messages.

## Active queue handlers

### `queue_download_handler.py`

- Handles a download queue item.
- Reads a `DownloadQueueCommand`.
- Resolves the last downloaded page from the file manager.
- Invokes the manga downloader service.
- Logs and records failures.

### `pdf_creator_queue_handler.py`

- Handles PDF creation jobs.
- Reads a `PDFCreateQueueCommand`.
- Invokes the PDF creator service.
- Cleans up converted image folders after generation.
- Logs process and errors.

### `webdav_queue_handler.py`

- Handles WebDAV upload jobs.
- Reads a `WebDavQueueCommand`.
- Delegates to the WebDAV service.
- Logs success or upload failure.

## Queue protocol

The common contract is defined in `src/contracts/protocols/queue_handler_protocol.py`.

Each queue handler is expected to:

- accept a `QueueMessage[TCommand]`
- expose an `on_message` method
- return a `Thread` for background processing
