# Project documentation

This folder stores project documentation for human developers and AI agents.

## Purpose

- Keep architecture and service structure notes in one place.
- Describe the responsibilities of each service and queue handler.
- Help future AI agents understand the project shape without reading all source files.

## Contents

- `architecture.md`: project architecture and responsibilities
- `services.md`: service inventory and usage
- `queue-handlers.md`: queue-based handlers and message flow
- `manual-tools.md`: one-off/manual scripts moved out of the main app flow

## Recommended convention

- Prefer short Markdown files focused on one topic.
- Add links between documents when the subject spans multiple areas.
- Keep the docs aligned with the current folder structure in `src/`.
