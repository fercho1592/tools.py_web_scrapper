## Estructura general del proyecto

El proyecto está organizado en un layout típico de aplicación Python con:

- `src/` → código fuente principal (módulos / paquetes)
- `scripts_helper/` → scripts auxiliares (JS y Python) para tareas específicas
- `src/tests/` y `src/web/driver/tests/` → tests unitarios
- archivos de configuración (`config.ini`, `Requirements.txt`, etc.)
- integración con Docker (`DOCKERFILE`)

---

## Carpetas principales y su contenido

### src

Contiene el código de la aplicación. El _entry point_ principal es `src/__main__.py`.

- `src/__main__.py`
  - Orquesta el flujo de descarga/transformación/subida.
  - Usa comandos en `app.handlers` y `MangaScraper`.

- `src/core/`
  - `core/container.py` → contenedor DI.
  - `core/config/`:
    - `dependency_injection.py` → armado de contenedor y bindings.
    - `config_manager.py` → lectura de `config.ini` y entorno.
    - `queue_reader.py` → parseo de colas de descarga.
    - `logger_factory.py` → creación de logger.
  - `core/services/`:
    - `file_manager.py` → manejo de archivos/carpetas.
    - `error_handler.py` → persistencia de errores.
    - `user_feedback_handler.py` → mensajes y barra de progreso.

- `src/contracts/`
  - Interfaces, protocolos y enums canónicos del dominio:
    - `contracts/enums/`
    - `contracts/models/`
    - `contracts/protocols/`
    - `contracts/services/`
    - `contracts/strategies/`
    - `contracts/web_drivers/`

- `src/manga/`
  - `manga_scrapper_context.py` → `MangaScraper`.
  - `manga_implementations/`:
    - `container.py` → `StrategyFactory`.
    - `_base_strategy.py` → clases base de estrategia/página/índice.
    - `e_web/` → `EMangaStrategy`, `EMangaIndex`, `EMangaPage`.
    - `tmh/` → `TmhMangaStrategy`, `TmhMangaIndex`, `TmhMangaPage`.

- `src/image/converter/`
  - `image_converter_interfaces.py` → contrato de conversión de imagen.
  - `pillow_image_converter.py` → implementación con Pillow.

- `src/web/driver/`
  - `query_selector.py` → motor selector CSS-like.
  - `html_parser/` + `bs4/` → decodificadores DOM.
  - `tests/` → tests de parser/selector.

- `src/app/handlers/`
  - Casos de uso desacoplados:
    - `manga_downloader_handler.py`
    - `image_converter_handler.py`
    - `pdf_creator_handler.py`
    - `webdav_handler.py`

- `src/infrastructure/`
  - `http_service.py` → implementación de `IHttpService` con `requests`.
  - `pdf_generator.py` → implementación de `IPdfCreator` con `fpdf`.

- `src/utils/`
  - `custom_decorators.py` → `delayed_view_timer`.
  - `string_path_fix.py` → normalización de strings para rutas.

---

## Componentes clave y relaciones

### Inyección de dependencias

`core.config.dependency_injection` construye `core.container.Container` y registra:

- Providers:
  - `IHttpService` → `infrastructure.http_service.HttpService`
  - `IImageEditorService` → `image.converter.pillow_image_converter.PillowImageConverter`
  - `IPdfCreator` → `infrastructure.pdf_generator.PdfCreator`
  - `WebDAVService` → `contracts.services.webdav_service.WebDAVService`
- Factories:
  - `MangaScraper` (depende de `IMangaStrategy`)
  - `IMangaStrategy` → `manga.manga_implementations.container.StrategyFactory`

### Flujo principal (`src/__main__.py`)

1. Lee cola con `core.config.queue_reader.read_queue`.
2. Para cada entrada:
   - Construye `MangaFoldersStruct`.
   - Crea `MangaScraper` por URL y obtiene metadata.
   - Descarga con `app.handlers.manga_downloader_handler`.
   - Convierte imágenes con `app.handlers.image_converter_handler`.
   - Genera PDF con `app.handlers.pdf_creator_handler`.
   - Sube a WebDAV con `app.handlers.webdav_handler`.

### Estrategias de scraping

- Contratos en `contracts.strategies.i_manga_strategy`.
- Implementaciones en `manga.manga_implementations.e_web` y `manga.manga_implementations.tmh`.
- Selección por dominio en `StrategyFactory` usando `ConfigEnum`.

### WebDAV

- `contracts.services.webdav_service.WebDAVService` usa `webdav4.client.Client` para:
  - comprobar existencia (`check_file_exists`)
  - crear carpetas remotas (`create_remote_dirs`)
  - subir archivos (`upload_file`)
- `app.handlers.webdav_handler` valida existencia local con `FileManager` y delega en `WebDAVService`.

---

## Tests

- Tests base en `src/tests/`.
- Tests de driver/selector en `src/web/driver/tests/`.
- Ejecución típica:
  - `PYTHONPATH=src .venv/bin/pytest -q src/tests src/web/driver/tests -q`

---

## Scripts auxiliares (`scripts_helper`)

Scripts para tareas manuales:

- `tmh_script.js` / `e_script.js` → generar listas de enlaces desde navegador.
- `test_webdav.py` → validar subida a WebDAV.
- `fix_folder_location.py` → reorganizar PDFs localmente.
- `youtube_test.py` → descarga de video con `yt_dlp`.
