# Execution Guide

This project supports two runtime modes:

- waterfall worker: runs the sequential processing flow directly
- queue listener: listens to a RabbitMQ queue and handles one message at a time

## Local entrypoint

The app entry point is the package runner in `src`:

    python src

This starts the waterfall workflow by default.

To start a queue listener, pass the queue name:

    python src --queue download
    python src --queue pdf
    python src --queue webdav

## Docker execution

The Docker image is built from the project root and uses the same app entrypoint:

    python src

Because the entrypoint accepts CLI arguments, the container can run any queue worker by overriding the command:

    docker run --rm <image> --queue download
    docker run --rm <image> --queue pdf
    docker run --rm <image> --queue webdav

This means the same image can launch the different queue listeners, but the runtime is still the app itself, not the helper scripts under `scripts/` or `scripts_helper/`.

## Compose deployment

The repo includes a Compose file that starts one worker per queue:

    docker compose up --build

This creates multiple containers that each listen to a different queue and connect to the configured RabbitMQ broker from `.env`.

## Notes

- The Docker image is intended to run the application runtime.
- Scripts in `scripts/` and `scripts_helper/` are maintenance utilities and are not part of the default app container lifecycle.
