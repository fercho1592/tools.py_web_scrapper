# Architecture overview

## Top-level structure

- `src/`: main application code.
- `src/app/handlers/`: queue/message handlers only.
- `src/services/`: functional service modules executed by handlers or orchestrators.
- `src/core/`: infrastructure, dependency injection, logger, queue reader, filesystem helpers.
- `src/contracts/`: interfaces, protocols, DTOs, and shared data contracts.
- `tools/manual/`: proof-of-concept and manual scripts moved out of the app root.
- `resources/`: static assets such as fonts.

## Main responsibilities

### `src/services`

This folder contains the actual business and workflow logic used by the application, such as:

- image conversion
- manga download orchestration
- PDF creation
- WebDAV upload

These modules are meant to be reusable, testable, and independent from queue transport details.

### `src/app/handlers`

This folder contains queue handlers that receive `QueueMessage` objects and delegate work to services.

Queue handlers are responsible for:

- reading a queue command
- invoking the corresponding service or function
- logging and error handling
- background execution

### `src/core`

This part contains the infrastructure layer:

- dependency injection container
- logger factory
- file management helpers
- config access
- queue reading utilities

### `src/contracts`

This contains the shapes used across the project:

- protocols
- config contracts
- service interfaces
- folder/path models

## Processing flow

1. A command is read from a queue or the app entry point.
2. The queue handler resolves or invokes the corresponding service.
3. The service performs the actual work.
4. Results are logged and reported back through the handler or UI layer.

## Notes

The project was reorganized so that:

- business logic stays in `src/services/`
- queue transport logic stays in `src/app/handlers/`
- manual/proof-of-concept scripts live in `tools/manual/`
