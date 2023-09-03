import os
from googleapiclient.discovery import build


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        api_key = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube
