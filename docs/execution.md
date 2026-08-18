# Execution Guide

The application entrypoint is the runner under `src/` and supports three execution modes:

- waterfall flow: default when no arguments are passed
- queue listener: `--queue download|pdf|webdav`
- prepare-links workflow: `--prepare-links <file>`

## Local execution

Run the default workflow:

    python src

Start a queue worker:

    python src --queue download
    python src --queue pdf
    python src --queue webdav

Prepare a list of manga links from a file:

    python src --prepare-links ./links.txt

This creates a queue-ready file for later review and queue insertion.

## Docker execution

The Docker image uses the same entrypoint and arguments:

    docker run --rm <image>
    docker run --rm <image> --queue download
    docker run --rm <image> --queue pdf
    docker run --rm <image> --queue webdav

## Compose deployment

The repo includes a Compose file that starts one worker per queue:

    docker compose up --build

Each service loads the values from `.env` through `env_file` and runs the correct queue worker command.

## Configuration

The project reads runtime configuration from `.env`. Copy `.env.example` before running the app:

    cp .env.example .env

This is the current source of connection and secret values; older `config.ini` settings are not the canonical runtime configuration.

## Notes

- The Docker image is intended to run the app runtime, not helper scripts.
- Maintenance utilities remain in `scripts/` and `scripts_helper/` and are not part of the default runtime lifecycle.
