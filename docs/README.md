# Project documentation

This folder stores project documentation for human developers and AI agents.

## Purpose

- Keep architecture and service structure notes in one place.
- Describe the responsibilities of each service and queue handler.
- Document how the app is executed locally and inside Docker.
- Help future AI agents understand the project shape without reading all source files.

## Contents

- `architecture.md`: project architecture and responsibilities
- `services.md`: service inventory and usage
- `queue-handlers.md`: queue-based handlers and message flow
- `manual-tools.md`: one-off/manual scripts moved out of the main app flow
- `execution.md`: local and Docker execution modes, entrypoints, and queue workers

## Execution summary

The application runtime is split into two main modes:

- waterfall worker: runs the sequential process flow with no queue argument
- queue listener: runs a RabbitMQ worker for a specific queue (`download`, `pdf`, or `webdav`)

## Recommended convention

- Prefer short Markdown files focused on one topic.
- Add links between documents when the subject spans multiple areas.
- Keep the docs aligned with the current folder structure in `src/`.
