# PyMangaScrapper

This project downloads and processes manga content through a queue-based runtime. It supports:

- a default waterfall workflow
- RabbitMQ queue listeners for the `download`, `pdf`, and `webdav` workers
- a link preparation workflow to turn a text file of links into a queue-ready file for review

## Requirements

Install Python dependencies:

    pip3 install -r Requirements.txt

Create a local environment file from the example:

    cp .env.example .env

Then edit `.env` with the values for your runtime, RabbitMQ broker, and service credentials.

## Runtime modes

The application entrypoint is the package runner under `src/`:

    python src

### Default flow

Running the app without arguments starts the waterfall flow:

    python src

### Queue listener

Start a specific queue worker:

    python src --queue download
    python src --queue pdf
    python src --queue webdav

### Prepare links workflow

Prepare a file of manga links into a queue-ready output file:

    python src --prepare-links ./links.txt

This reads each link, resolves metadata, and writes:

- `temp-download-queue.txt`
- `error_links.txt`

The output file is in the same directory as the source file unless a custom output path is configured in the worker logic.

## Docker

The project includes a Compose file that starts one worker per queue:

    docker compose up --build

Individual queue workers can also be started directly:

    docker run --rm <image> --queue download
    docker run --rm <image> --queue pdf
    docker run --rm <image> --queue webdav

## Environment configuration

The project uses `.env` instead of the older `config.ini` setup. The required keys are documented in `.env.example`.

Key variables include:

- RabbitMQ connection and credentials
- WebDAV host/user/password
- Azure Service Bus values
- Telegram bot token
- logging level

## Project docs

See the docs folder for architecture and execution notes:

- [docs/README.md](docs/README.md)
- [docs/execution.md](docs/execution.md)
- [docs/architecture.md](docs/architecture.md)
- [docs/services.md](docs/services.md)
- [docs/queue-handlers.md](docs/queue-handlers.md)
- [docs/manual-tools.md](docs/manual-tools.md)

## Common errors

- https://medium.com/@yen.hoang.1904/resolve-issue-ssl-certificate-verify-failed-when-trying-to-open-an-url-with-python-on-macos-46d868b44e10
