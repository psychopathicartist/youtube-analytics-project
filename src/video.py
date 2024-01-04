from googleapiclient.discovery import build

import os


class IDError(Exception):
    """Класс исключения при отсутствии видео с введенным id"""
    def __init__(self):
        self.message = 'Видео с таким id не существует.'

    def __str__(self):
        return self.message


class Video:
    """Класс для видео"""
    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API"""
        try:
            self.video_id = video_id
            info_video = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=self.video_id).execute()
            if not info_video['items']:
                raise IDError
            else:
                self.title: str = info_video['items'][0]['snippet']['title']
                self.url: str = 'https://www.youtube.com/watch?v=info_video' + self.video_id
                self.count: int = info_video['items'][0]['statistics']['viewCount']
                self.like_count: int = info_video['items'][0]['statistics']['likeCount']
        except IDError as error:
            print(error.message)
            self.title = None
            self.url = None
            self.count = None
            self.like_count = None

    def __str__(self) -> str:
        """Возвращает информацию о видео для пользователя"""
        return self.title

    @staticmethod
    def get_service():
        """Возвращает объект для работы с YouTube API"""
        api_key = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)


class PLVideo(Video):
    """Класс для плейлиста видео"""
    def __init__(self, video_id: str, playlist_id: str) -> None:
        """Экземпляр инициализируется id видео и id плейлиста. Дальше все данные будут подтягиваться по API"""
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self) -> str:
        """Возвращает информацию о плейлисте для пользователя"""
        return self.title
