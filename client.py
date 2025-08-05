import requests

from utils import Util


class Client:
    def __init__(self, path, config: dict):
        self.util = Util()
        self.path = path
        self.config = config

    def safe_join(self, base: str, path: str) -> str:
        return base.rstrip("/") + "/" + path.lstrip("/")

    def send(self):
        endpoint = self.path.get("endpoint", "/")
        method = self.path.get("method", "GET").upper()
        headers = self.path.get("headers", {})
        body = self.path.get("body", {})
        header_auth, request_auth = self.util.load_auth_header(
            self.path.get("auth", {})
        )

        response = requests.request(
            method=method,
            url=self.safe_join(
                self.config.get("servers", [{}])[0].get("url", ""), endpoint
            ),
            headers={**headers, **header_auth},
            auth=request_auth,
            json=body if method in ["POST", "PUT", "PATCH"] else None,
            params=body if method == "GET" else None,
        )

        return response
