# Project documentation

This folder stores the project’s runtime and architecture notes for developers and automation.

## Purpose

- Document the current runtime entrypoints and worker layout.
- Keep architecture and service responsibility notes in one place.
- Explain the queue-based download flow and the prepare-links workflow.
- Help future contributors and AI agents understand the project without reading every source file.

## Contents

- `architecture.md`: architectural boundaries and message flow
- `services.md`: service inventory and responsibilities
- `queue-handlers.md`: queue handlers and their message lifecycle
- `manual-tools.md`: maintenance scripts and manual utilities
- `execution.md`: local, Docker, and queue runtime instructions

## Runtime summary

The current CLI supports three execution modes:

- waterfall flow: default startup with no arguments
- queue listener: `--queue download|pdf|webdav`
- prepare-links workflow: `--prepare-links <file>`

## Recommended convention

- Keep each document focused on one topic.
- Prefer short, practical examples over long narrative sections.
- Update docs whenever runtime flags or configuration names change.
