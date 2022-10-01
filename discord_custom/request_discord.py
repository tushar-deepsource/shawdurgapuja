import json
from functools import lru_cache
from urllib import request

from django.conf import settings


@lru_cache
def discord_api_req(
    path: str,
    method: str = "post" or "get",
    data = None,
    content_type: str = "application/json",
):
    base_api = "https://discord.com/api"
    headers = {
        "User-Agent": "Shaw Durga Puja Website",
        "X-Ratelimit-Precision": "millisecond",
        "Authorization": f"Bot {settings.TOKEN}",
        "Content-Type": content_type,
    }
    print(data, 'hi')
    if method == "post":
        req = request.Request(url=base_api + path,
                              headers=headers,
                              method="POST")
    if method == "get":
        req = request.Request(url=base_api + path,
                              headers=headers,
                              method="GET")
    if data:
        data = json.dumps(data)
        data = data.encode()
    r = request.urlopen(req, data=data)
    content = r.read()
    return content
