from .request_discord import *
from celery import shared_task

@shared_task
async def message_me(message: str, channel_id: int,  embed: bool = None):
    '''Send message to required channel for the ping'''
    try:
        if not embed:
            await discord_api_req(
                f'/channels/{channel_id}/messages',
                'post',
                data={
                    'content': message
                }
            )
        else:
            await discord_api_req(
                f'/channels/{channel_id}/messages',
                'post',
                data={
                    'embed': embed.to_dict()
                }
            )
    except:
        pass