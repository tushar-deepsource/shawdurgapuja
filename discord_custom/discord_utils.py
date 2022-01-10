from __future__ import absolute_import

from celery.decorators import task

from .request_discord import *


@task("message_me")
def message_me(message: str, channel_id: int, embed: bool = None):
    """Send message to required channel for the ping"""
    try:
        if not embed:
            discord_api_req(f"/channels/{channel_id}/messages",
                            "post",
                            data={"content": message})
        else:
            discord_api_req(
                f"/channels/{channel_id}/messages",
                "post",
                data={"embed": embed.to_dict()},
            )
    except:
        pass
