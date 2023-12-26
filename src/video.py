from googleapiclient.discovery import build

import os


class Video:
    """Класс для видео"""
    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API"""
        self.video_id = video_id
        info_video = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                      id=self.video_id).execute()
        self.video_title: str = info_video['items'][0]['snippet']['title']
        self.video_url: str = 'https://www.youtube.com/watch?v=info_video' + self.video_id
        self.view_count: int = info_video['items'][0]['statistics']['viewCount']
        self.like_count: int = info_video['items'][0]['statistics']['likeCount']

    def __str__(self) -> str:
        """Возвращает информацию о видео для пользователя"""
        return self.video_title

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
        return self.video_title
