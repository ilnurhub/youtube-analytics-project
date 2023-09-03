import os
from googleapiclient.discovery import build
import isodate
from datetime import timedelta


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.__playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                         part='contentDetails',
                                                                         maxResults=50, ).execute()
        self.__video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.__playlist_videos['items']]
        self.__video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                                 id=','.join(self.__video_ids)).execute()
        self.__playlists = self.get_service().playlists().list(channelId=self.channel_id(),
                                                               part='contentDetails,snippet',
                                                               maxResults=50,
                                                               ).execute()
        self.title = self.playlist_title()
        self.__total_duration = self.total_duration

    def channel_id(self):
        """
        Возвращает id канала, в котором находится плейлист
        """
        video_id = self.__video_response['items'][0]['id']
        video_resp = self.get_service().videos().list(part='snippet,statistics',
                                                      id=video_id
                                                      ).execute()
        return video_resp['items'][0]['snippet']['channelId']

    def playlist_title(self):
        """
        Возвращает название плейлиста
        """
        for playlist in self.__playlists['items']:
            if playlist['id'] == self.playlist_id:
                return playlist['snippet']['title']

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        max_like_count = 0
        video_url = ''
        for video in self.__video_response['items']:
            if int(video['statistics']['likeCount']) > max_like_count:
                video_url = f'https://youtu.be/{video["id"]}'
        return video_url

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        api_key = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    @property
    def total_duration(self):
        all_video_duration = timedelta(hours=0, minutes=0, seconds=0)
        for video in self.__video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            all_video_duration += duration
        self.__total_duration = all_video_duration
        return self.__total_duration
