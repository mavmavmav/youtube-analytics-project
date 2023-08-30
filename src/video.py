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
        self.video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                       id=self.video_id
                                       ).execute()


        self.video_id: str = self.video_response['items'][0]['id']
        self.video_title: str = self.video_response['items'][0]['snippet']['title']
        self.video_url: str = 'https://youtu.be/' + self.video_id
        self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
        self.video_Id = video_id
        self.playlist_id = playlist_id

    def __str__(self):
        return f'{self.video_title}'



if __name__ == '__main__':
    video1 = Video('AWX4JnAnjBE')
    Video.printj(video1.video_response)
    print(video1.video_id)
    print(video1.video_title)
    print(video1.video_url)
    print(video1.view_count)
    print(video1.like_count)

    video2 = PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC')
    print(video2.video_Id)
    print(video2.video_title)
    print(video2.video_url)
    print(video2.view_count)
    print(video2.like_count)
    print(video2.playlist_id)
    PLVideo.printj(video2.video_response)
