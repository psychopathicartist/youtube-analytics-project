import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        info = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = info['items'][0]['snippet']['title']
        self.description = info['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.channel_id
        self.subscriber_count = info['items'][0]['statistics']['subscriberCount']
        self.video_count = info['items'][0]['statistics']['videoCount']
        self.view_count = info['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(channel)

    def to_json(self, filename):
        """Сохраняет в файл значения атрибутов экземпляра Channel"""
        data = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        api_key = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    @property
    def channel_id(self):
        return self.__channel_id
