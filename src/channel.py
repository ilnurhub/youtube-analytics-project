import json
import os
from googleapiclient.discovery import build
from config import ROOT_PATH


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.channel_id}'
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        return self.__channel_id

    def __str__(self):
        """
        Возвращает название и ссылку на канал по шаблону `<название_канала> (<ссылка_на_канал>)
        """
        return f"{self.title} ({self.url})"

    def __add__(self, other) -> int:
        """
        Возвращает результат сложения количества подписчиков двух каналов
        """
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """
        Возвращает результат вычитания количества подписчиков двух каналов
        """
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        """
        Возвращает результат сравнения "меньше" двух каналов по количеству подписчиков
        """
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        """
        Возвращает результат сравнения "меньше или равно" двух каналов по количеству подписчиков
        """
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __gt__(self, other):
        """
        Возвращает результат сравнения "больше" двух каналов по количеству подписчиков
        """
        return int(self.subscriber_count) > int(other.subscriber_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    def to_json(self, filename):
        """
        Сохраняет в файл значения атрибутов экземпляра `Channel`
        """
        channel_attributes = {
            'channel_id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        file_path = os.path.join(ROOT_PATH, 'src', filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                list_of_data = json.load(f)
        else:
            list_of_data = []
        list_of_data.append(channel_attributes)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(list_of_data, f, indent=1)

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        api_key = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube
