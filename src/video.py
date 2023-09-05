import json
import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:

    def __init__(self, video_id):
        self._video_id = video_id
        self.title = None
        self.url = None
        self.total_views = None
        self.like_count = None
        self.init_func()



    @property
    def video_id(self):
        return self._video_id

    @classmethod
    def init_func(cls):
        try:
            video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=cls.video_id
                                               ).execute()
            cls.title: str = video_response['items'][0]['snippet']['title']

        except IndexError:
            print('Неверный Video_ID')

        else:
            cls.url_video: str = 'https://www.youtube.com/watch?v=' + cls._video_id
            cls.total_views: int = int(video_response['items'][0]['statistics']['viewCount'])
            cls.like_count: int = int(video_response['items'][0]['statistics']['likeCount'])


    def to_json(self, filename):
        data = {
            'title': self.video_title,
            'view_count': self.view_count,
            'like_count': self.like_count,
            'comment_count': self.comment_count,

        }
        with open(filename, 'w', encoding='UTF-8') as f:
            json.dump(data, f, ensure_ascii=False)

    def printj(self: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(self, indent=2, ensure_ascii=False))

    def __str__(self):
        return f'{self.video_title}'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return f'{self.video_title}'
