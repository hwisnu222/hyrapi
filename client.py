from contextlib import ExitStack
import os
import requests

from utils import Util


class Client:
    def __init__(self, path, config: dict):
        self.util = Util()
        self.path = path
        self.config = config

    def safe_join(self, base: str, path: str) -> str:
        return base.rstrip("/") + "/" + path.lstrip("/")

    def send(self, index_env=0):
        response = None
        endpoint = self.path.get("endpoint", "/")
        method = self.path.get("method", "GET").upper()
        headers = self.path.get("headers", {})
        body = self.path.get("body", {})
        header_auth, request_auth = self.util.load_auth_header(
            self.path.get("auth", {})
        )

        kwargs = {
            "method": method,
            "url": self.safe_join(
                self.config.get("servers", [{}])[index_env].get("url", ""), endpoint
            ),
            "auth": request_auth,
            "params": body if method == "GET" else None,
        }

        if headers.get("Content-Type") == "multipart/form-data":
            # remove header manually
            # requests will put header with boundary
            headers.pop("Content-Type", None)
            data = {}
            files = {}

            # close all openend file when done
            with ExitStack() as stack:
                for key, value in body.items():
                    if isinstance(value, str) and os.path.isfile(value):
                        f = stack.enter_context(open(value, "rb"))
                        files[key] = f
                    else:
                        data[key] = value

                kwargs["data"] = data
                kwargs["files"] = files
                kwargs["headers"] = {**headers, **header_auth}
                response = requests.request(**kwargs)
        else:
            kwargs["json"] = body if method in ["POST", "PUT", "PATCH"] else None
            kwargs["headers"] = {**headers, **header_auth}
            response = requests.request(**kwargs)

        return response
