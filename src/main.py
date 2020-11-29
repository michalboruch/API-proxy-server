# -*- coding: utf-8 -*-

import json
import os
import requests
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = ""
PORT = 8080

try:
    API_URL = os.environ["API_URL"]
except:
    sys.exit("API URL not provided.")


class ProxyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # Transmit request headers
        headers = {}

        # Make a request to the target API
        r = requests.get(
            f"{API_URL}{self.path}",
            cookies=self._dict_cookies,
            headers=headers,
        )

        # Transmit status code
        self.send_response(r.status_code)

        # Transmit headers
        self.send_header("Set-Cookie", dict(r.cookies))

        for k, v in r.headers.items():
            self.send_header(k, f"{v}\n")
        self.end_headers()

        self.wfile.write(bytes(self._prep_body(r), "utf-8"))

    def do_POST(self):
        # Transmit request headers
        headers = {}

        # Transmit request data
        data = json.dumps({})

        try:
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
        except:
            print(f"Getting data from request failed.")

        # Make a request to the target API
        r = requests.post(
            f"{API_URL}{self.path}",
            cookies=self._dict_cookies,
            data=json.loads(data),
            headers=headers,
        )

        # Transmit status code
        self.send_response(r.status_code)

        # Transmit headers
        self.send_header("Set-Cookie", dict(r.cookies))

        for k, v in r.headers.items():
            self.send_header(k, f"{v}\n")
        self.end_headers()

        self.wfile.write(bytes(self._prep_body(r), "utf-8"))

    # Helpers
    @property
    def _dict_cookies(self):
        """Convert header cookies to dictionary."""
        cookies = self.headers["Cookie"] or ""
        ret_cookies = {}
        if cookies:
            cookies = cookies.split(";")
            for c in cookies:
                k, v = c.split("=")
                ret_cookies[k] = v
        return ret_cookies

    @staticmethod
    def _prep_body(response):
        """Get body based response on content type."""
        content_type = response.headers.get("Content-type")
        body = None
        if "json" in content_type:
            body = json.dumps(response.json())
        else:
            body = response.text
        return body


if __name__ == "__main__":
    webServer = HTTPServer((HOST, PORT), ProxyServer)
    print("Server started!")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
