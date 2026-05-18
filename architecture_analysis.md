Workspace: Collecting workspace information## Estructura general del proyecto

El proyecto está organizado en un layout típico de aplicación Python con:

- src → código fuente principal (módulos / paquetes)
- scripts_helper → scripts auxiliares (JS y Python) para tareas específicas
- `tests/` dentro de src → tests unitarios y de integración
- archivos de configuración (config.ini, Requirements.txt, .pylintrc, etc.)
- integración con Docker (DOCKERFILE)

---

## Carpetas principales y su contenido

### src

Contiene el código de la aplicación. Es el _entry point_ principal (**main**.py) y su lógica principal:

- **main**.py
  - Orquesta el flujo completo (leer cola, descargar manga, convertir imágenes, crear PDF, subir a WebDAV).
  - Usa handlers (`MangaDownloaderHandler`, `ImageConverterHandler`, `PDFCreatorHandler`, `WebDavHandler`) y `MangaScraper` (estrategia + lógica de descarga).

- configs  
  Configuración y DI:
  - dependency_injection.py
    - Construye y registra providers en `feature.container.Container`.
    - Relaciona interfaces (protocolos) con implementaciones concretas (`HttpService`, `PdfCreator`, `PillowImageConverter`, etc.).
  - config_manager.py
    - `ConfigParserService` (lee config.ini).
    - `EnvironConfig` (lee variables de entorno, con defaults de `ConfigEnum`).
  - queue_reader.py
    - Lee listas de descarga desde un archivo `download-queue.txt`.

- feature  
  Implementaciones de negocio (descarga, conversión, PDF, etc.).
  - container.py
    - Contenedor simple (DI) utilizado por dependency_injection.py.
  - `feature/services/`
    - file_manager.py → manejo de archivos/carpetas (crear, mover, listar imágenes).
    - error_handler.py → escritura de logs de errores.
    - user_feedback_handler.py → impresión de mensajes y barra de progreso.
  - `feature/manga_strategy/`
    - Estrategias para scraping de manga según dominio (E-Hentai, TMH, etc).
    - manga_scrapper_context.py → clase `MangaScraper` que usa `IMangaStrategy` + `IHttpService` + utilidades para descarga de páginas, avance de páginas, etc.
    - `manga_implementations/` → implementaciones concretas:
      - container.py → fábrica de estrategias (`StrategyFactory`) que usa `ConfigEnum` para seleccionar estrategia según URL.
      - \_base_strategy.py → clases base para estrategias y páginas.
      - `e_web/` → estrategia para dominio E (implementa `EMangaStrategy`, `EMangaIndex`, `EMangaPage`).
      - `tmh/` → estrategia para dominio TMH (`TmhMangaStrategy`, `TmhMangaIndex`, `TmhMangaPage`).
  - `feature/image_converter/`
    - pillow_image_converter.py → convierte imágenes usando Pillow.
  - `feature/web_driver/`
    - Parser HTML genérico (no depende de Selenium, usa `html.parser`):
      - html_decoder.py + dom_reader.py → convierten HTML en una estructura DOM propia (`IWebReaderDriver` / `IWebElementDriver`).
      - tests en `feature/web_driver/tests/`.

- handler  
  Handlers orientados a casos de uso:
  - manga_downloader_handler.py → descarga todas las páginas de un manga usando `MangaScraper`.
  - image_converter_handler.py → convierte imágenes a formato PNG/JPG según configuración.
  - pdf_creator_handler.py → crea PDF desde carpetas de imágenes.
  - webdav_handler.py → sube PDF a WebDAV usando `WebDAVService`.
  - video_scrapper_handler.py / video_downloader_handler.py → handlers (más recientes) para vídeo (no están conectados en **main**.py).

- infrastructure  
  Infraestructura concreta:
  - http_service.py → implementa `IHttpService` (requests + parser HTML).
  - pdf_generator.py → implementa `IPdfCreator` con `fpdf`.

- tools  
  Herramientas auxiliares:
  - custom_decorators.py → decorador (`delayed_view_timer`) que añade delay de 5s.
  - string_path_fix.py → normalización de strings para rutas (quita acentos, etc.).

---

## Componentes clave y relaciones

### Inyección de dependencias

dependency_injection.py construye el **contenedor** (`feature.container.Container`) y registra:

- Providers:
  - `IHttpService` → `infrastructure.http_service.HttpService`
  - `IImageEditorService` → `feature.image_converter.pillow_image_converter.PillowImageConverter`
  - `IPdfCreator` → `infrastructure.pdf_generator.PdfCreator`
  - `WebDAVService` → `feature_interfaces.services.webdav_service.WebDAVService`
- Factories:
  - `MangaScraper` (depende de `IMangaStrategy`)
  - `IMangaStrategy` → resuelve con `StrategyFactory` (según dominio URL usando `ConfigEnum`).

### Flujo principal (**main**.py)

1. Lee cola de descargas (`configs.queue_reader.read_queue`).
2. Para cada entrada:
   - Construye `MangaFoldersStruct` (paths locales + WebDAV).
   - Crea `MangaScraper` (por URL) y obtiene metadata (`get_manga_data()`).
   - **Descarga** con `MangaDownloaderHandler` (usa `MangaScraper` + `MangaScraper.set_starting_page()/download_current_page()`).
   - **Convierte** imágenes con `ImageConverterHandler`.
   - **Genera PDF** con `PDFCreatorHandler`.
   - **Sube a WebDAV** con `WebDavHandler`.

### Estrategias de scraping (manga)

- Se definen interfaces en i_manga_strategy.py.
- Implementaciones específicas en:
  - e_web (dominio E)
  - tmh (dominio TMH)
- `StrategyFactory` (en container.py) usa `ConfigEnum` para obtener el dominio base desde config.

### WebDAV

- `WebDAVService` (implementación matriz) usa `webdav4.client.Client` para:
  - comprobar existencia (`check_file_exists`)
  - crear carpetas (`create_remote_dirs`)
  - subir archivos (`upload_file`)
- `WebDavHandler` (en webdav_handler.py) usa `FileManager` para verificar existencia local y luego llama a la implementación de servicio.

---

## Tests y estilo

- Tests con `pytest` están en tests (ej. string_tools_test.py) y en `src/feature/web_driver/tests/...`.
- El workspace configura `pytest` en settings.json.

---

## Scripts auxiliares (scripts_helper)

Scripts usados para tareas manuales (no están integrados al flujo principal):

- tmh_script.js / e_script.js → scripts JS para generar listas de enlaces desde páginas (se usan en navegador).
- test_webdav.py → script para probar subida WebDAV con `webdav4`.
- fix_folder_location.py → reorganiza PDFs en el disco bajo `~/Desktop/Manga_downloads/pdfs/`.
- youtube_test.py → descarga vídeo con `yt_dlp`.
