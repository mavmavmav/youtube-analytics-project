from googleapiclient.discovery import build
import os
import json
import isodate


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализирует id канала.
        Дальше все данные будут подтягиваться по API.
        """

        youtube = self.get_service()
        response = youtube.channels().list(id=channel_id,
                                           part='snippet, statistics')
        self.response = response.execute()

        data_info = self.response.get('items', [])
        self.channel_id = data_info[0]['id']
        self.title = data_info[0]['snippet']['title']
        self.description = data_info[0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{channel_id}'
        self.subs_count = int(data_info[0]['statistics']['subscriberCount'])
        self.video_count = int(data_info[0]['statistics']['videoCount'])
        self.view_count = int(data_info[0]['statistics']['viewCount'])


    def __str__(self):
        """
        Отображение информации для пользователя
        """
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """
        Операция сложения 1arg и 2arg
        """
        return self.subs_count + other.subs_count

    def __sub__(self, other):
        """
        Операция вычитания 1arg и 2arg
        """
        return int(self.subs_count) - int(other.subs_count)

    def __gt__(self, other):
        """
        Операция 1arg > 2arg
        """
        return self.subs_count > other.subs_count

    def __ge__(self, other):
        """
        Операция 1arg >= 2arg
        """
        return self.subs_count >= other.subs_count

    def __lt__(self, other):
        """
        Операция 1arg < 2arg
        """
        return self.subs_count < other.subs_count

    def __le__(self, other):
        """
        Операция 1arg <= 2arg
        """
        return self.subs_count <= other.subs_count

    def __eq__(self, other):
        """
        Операция сравнения 1arg и 2arg
        """
        return self.subs_count == other.subs_count

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube

    @staticmethod
    def printj(dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

    def to_json(self, filename):
        data = {
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscribers': self.subs_count,
            'video_count': self.video_count,
            'total_views': self.view_count,
        }
        with open(filename, 'w', encoding='UTF-8') as f:
            json.dump(data, f, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        self.printj(self.response)
        # playlists = youtube.playlists().list(channelId=self.channel_id,
        #                                      part='contentDetails,snippet',
        #                                      maxResults=50,
        #                                      ).execute()
        #
        # playlist_id = playlists['items'][0]['id']
        # playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
        #                                                part='contentDetails',
        #                                                maxResults=50,
        #                                                ).execute()
        #
        # video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        #
        # video_response = youtube.videos().list(part='contentDetails,statistics',
        #                                id=','.join(video_ids)
        #                                ).execute()
        # for video in video_response['items']:
        #     # YouTube video duration is in ISO 8601 format
        #     iso_8601_duration = video['contentDetails']['duration']
        #     duration = isodate.parse_duration(iso_8601_duration)
