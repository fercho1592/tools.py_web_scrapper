from webdav4.client import Client
import os
from feature_interfaces.models.folders_struct import FolderPath
from feature_interfaces.protocols.config_protocol import LoggerProtocol


class WebDAVService:
    def __init__(
        self, logger: LoggerProtocol, url: str, user: str, password: str
    ) -> None:
        self._logger = logger
        self._url = url
        self._user = user
        self._password = password

    def check_file_exists(self, file_path: str) -> bool:
        client = Client(
            base_url=self._url,
            auth=(self._user, self._password),
        )

        return client.exists(file_path)

    def upload_file(
        self, local_file_path: FolderPath, file_name: str, remote_file_path: FolderPath
    ) -> None:
        client = Client(
            base_url=self._url,
            auth=(self._user, self._password),
        )

        self._logger.info(
            "Uploading file from [%s] to [%s]",
            f"{local_file_path.get_file_path(file_name)}",
            f"{remote_file_path.get_file_path(file_name)}",
        )
        if not client.exists(remote_file_path.relative_path):
            self.create_remote_dirs(client, remote_file_path.relative_path)

        client.upload_file(
            from_path=f"{local_file_path.get_file_path(file_name)}",
            to_path=f"{remote_file_path.get_file_path(file_name)}",
        )
        self._logger.info("File uploaded successfully to [%s]", remote_file_path)
        pass

    def create_remote_dirs(self, client: Client, remote_path: str):
        dirs = remote_path.split("/")
        path = ""
        for dir in dirs:  # Exclude the file name
            path_str = os.path.join(path, dir)
            if not client.exists(path_str):
                client.mkdir(path_str)
            path = path_str
