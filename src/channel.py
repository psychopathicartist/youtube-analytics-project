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
        self.subscriber_count = int(info['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(info['items'][0]['statistics']['videoCount'])
        self.view_count = int(info['items'][0]['statistics']['viewCount'])

    def __str__(self) -> str:
        """Возвращает информацию о канале для пользователя"""
        return f'{self.title} ({self.url})'

    def __add__(self, other) -> int:
        """Возвращает результат от операции сложения количества
        подписчиков двух каналов"""
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other) -> int:
        """Возвращает результат от операции вычитания количества
        подписчиков двух каналов"""
        return self.subscriber_count - other.subscriber_count

    def __lt__(self, other) -> bool:
        """Возвращает результат от операции сравнения "меньше"
        количества подписчиков двух каналов"""
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other) -> bool:
        """Возвращает результат от операции сравнения "меньше
        или равно" количества подписчиков двух каналов"""
        return self.subscriber_count <= other.subscriber_count

    def __gt__(self, other) -> bool:
        """Возвращает результат от операции сравнения "больше"
        количества подписчиков двух каналов"""
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other) -> bool:
        """Возвращает результат от операции сравнения "больше
        или равно" количества подписчиков двух каналов"""
        return self.subscriber_count >= other.subscriber_count

    def __eq__(self, other) -> bool:
        """Возвращает результат от операции сравнения "равно"
        количества подписчиков двух каналов"""
        return self.subscriber_count == other.subscriber_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(channel)

    def to_json(self, filename) -> None:
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
