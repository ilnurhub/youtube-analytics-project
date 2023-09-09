import os
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id: str):
        self.video_id = video_id
        self.video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                               id=self.video_id).execute()
        try:
            self.title = self.video_response['items'][0]['snippet']['title']
        except IndexError:
            self.title = None
            self.video_link = None
            self.view_count = None
            self.like_count = None
        else:
            self.video_link = f'https://www.youtube.com/watch?v={self.video_id}'
            self.view_count = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        """
        Возвращает название видео
        """
        return self.title

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        api_key = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
