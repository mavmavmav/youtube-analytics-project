import json
import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:

    def __init__(self, video_id):
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        self.video_response = video_response

        self.video_id: str = video_response['items'][0]['id']
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.video_url: str = 'https://youtu.be/' + self.video_id
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']

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
