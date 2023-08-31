from src.channel import Channel


class Video(Channel):
    def __init__(self, video_id: str):
        self.video_id = video_id
        self.video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                               id=self.video_id).execute()
        self.video_title = self.video_response['items'][0]['snippet']['title']
        self.video_link = f'https://www.youtube.com/watch?v={self.video_id}'
        self.view_count = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count = self.video_response['items'][0]['statistics']['likeCount']
