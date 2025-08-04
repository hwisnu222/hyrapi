import requests


class Client:
    def __init__(self, host, path, config: dict):
        self.host = host
        self.path = path
        self.config = config

    def safe_join(self, base: str, path: str) -> str:
        return base.rstrip("/") + "/" + path.lstrip("/")

    def send(self):
        endpoint = self.path.get("endpoint", "/")
        method = self.path.get("method", "GET").upper()
        headers = self.path.get("headers", {})
        body = self.path.get("body", {})

        response = requests.request(
            method=method,
            url=self.safe_join(
                self.config.get("servers", [{}])[0].get("url", ""), endpoint
            ),
            headers=headers,
            json=body if method in ["POST", "PUT", "PATCH"] else None,
            params=body if method == "GET" else None,
        )

        return response
