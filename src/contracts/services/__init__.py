"""Services contract wrappers."""

from contracts.services import (
    error_handler as error_handler,
    http_service as http_service,
    i_web_reader as i_web_reader,
    pdf_creator as pdf_creator,
    user_feedback_handler as user_feedback_handler,
    webdav_service as webdav_service,
)

__all__ = [
    "error_handler",
    "http_service",
    "i_web_reader",
    "pdf_creator",
    "user_feedback_handler",
    "webdav_service",
]
