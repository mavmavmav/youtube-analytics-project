import datetime

import isodate
from datetime import timedelta
from src.channel import Channel



youtube = Channel.get_service()

class Playlist:
    def __init__(self, playlist_id):
        self.title = ''
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"
        self.__playlist_id = playlist_id
        self.response_init()

    @property
    def playlist_id(self):
        return self.__playlist_id

    def response_init(self):
        playlist_response = youtube.playlists().list(part='snippet',
                                                     id=self.playlist_id,
                                                     ).execute()
        self.title: str = playlist_response['items'][0]['snippet']['title']
        self.playlist_response = playlist_response

    def videos_from_playlist_list(self):
        list_ = []
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        for i in video_response['items']:
            list_.append(i)
        return list_

    @property
    def total_duration(self) -> timedelta:
        total_duration = timedelta()
        for video in self.videos_from_playlist_list():
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration


    def show_best_video(self):
        best_video = ""
        best_video_count = 0
        for video in self.videos_from_playlist_list():
            like_count: int = video['statistics']['likeCount']
            if int(like_count) > best_video_count:
                best_video = f"https://youtu.be/{video['id']}"
        return best_video

