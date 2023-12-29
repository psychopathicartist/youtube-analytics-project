from googleapiclient.discovery import build

import os
import isodate
import datetime


class PlayList:
    """Класс для плейлиста видео"""

    def __init__(self, playlist_id: str) -> None:
        """Экземпляр инициализируется названием плейлиста"""
        self.__playlist_id = playlist_id
        info_playlist = self.get_service().playlists().list(id=self.__playlist_id,
                                                            part='contentDetails,snippet',
                                                            maxResults=50,).execute()
        self.title: str = info_playlist['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id

    def __str__(self) -> str:
        """Возвращает информацию о плейлисте для пользователя"""
        return self.title

    @property
    def playlist_id(self):
        """Возвращает id плейлиста"""
        return self.__playlist_id

    @staticmethod
    def get_service():
        """Возвращает объект для работы с YouTube API"""
        api_key = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    @property
    def video_response(self):
        """Возвращает информацию обо всех видео из плейлиста"""
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50, ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(video_ids)).execute()
        return video_response

    @property
    def total_duration(self):
        """Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста"""
        time_counter = []
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            durations = isodate.parse_duration(iso_8601_duration)
            time_counter.append(durations)
        duration = sum(time_counter, datetime.timedelta())
        return duration

    def show_best_video(self) -> str:
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        max_like_count = 0
        best_url = ''
        for video in self.video_response['items']:
            like_count = video['statistics']['likeCount']
            if int(like_count) >= max_like_count:
                max_like_count = int(like_count)
                best_url = 'https://youtu.be/' + video['id']
        return best_url
