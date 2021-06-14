import requests
from django.conf import settings


def discord_api_req(
    path: str,
    method: str = 'post' or 'get',
    data: dict=None, 
    content_type: str = 'application/json'
):
    base_api = 'https://discord.com/api'
    headers = {
        'User-Agent': 'Shaw Durga Puja Website',
        'X-Ratelimit-Precision': 'millisecond',
        'Authorization': f'Bot {settings.TOKEN}',
        'Content-Type': content_type
    }
    if method == 'post':
        request = requests.post(
            base_api+path,
            headers=headers,
            json=data
        )
    if method == 'get':
        if data:
            request = requests.get(
                base_api+path,
                headers=headers,
            )
        else:
            request = requests.get(
                base_api+path,
                headers=headers,
                params=data
            )
    return request
