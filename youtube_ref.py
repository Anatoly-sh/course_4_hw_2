import os
import json
from googleapiclient.discovery import build
import datetime
import isodate

"""
Файл .env в корне проекта  — это текстовый файл, содержащий пары “ключ/значение” 
всех переменных среды. Необходимо установить библиотеку python-dotenv. load_dotenv() 
— для поиска файла .env и загрузки из него переменных среды.
"""
from dotenv import load_dotenv
load_dotenv()


class Main:
    """Класс для работы с ютубом"""
    api_key: str = os.getenv('SKYPROAPIKEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self):
        pass

    @staticmethod
    def dict_to_json(data: dict) -> json:
        """Возвращает словарь в формате json"""
        return json.dumps(data, indent=2, ensure_ascii=False)

    @classmethod
    def get_service(cls):
        """метод класса, который возвращает объект для работы с API ютуба"""
        return cls.youtube

    @classmethod
    def _get_channel(cls, channel_id: str) -> dict:
        """Информация о канале"""
        channel = cls.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        return channel

    @classmethod
    def _get_video(cls, video_id) -> dict:
        """Данные о видео"""
        video = cls.youtube.videos().list(id=video_id, part='snippet,statistics').execute()
        return video

    @classmethod
    def _get_playlist(cls, playlist_id) -> dict:
        """Данные о плейлисте"""
        playlist = cls.youtube.playlists().list(id=playlist_id, part='contentDetails, snippet').execute()
        return playlist

    @classmethod
    def _get_playlist_channel(cls, channel_id: str) -> dict:
        """Плейлист канала"""
        playlist = cls.youtube.playlists().list(channelId=channel_id,
                                                part='contentDetails, snippet',
                                                maxResults=50).execute()
        return playlist

    @classmethod
    def _get_ids_videos_in_playlist(cls, playlist_id: str) -> list:
        """id видео из плейлиста"""
        playlist_videos = cls.youtube.playlistItems().list(playlistId=playlist_id,
                                                           part='contentDetails',
                                                           maxResults=50).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        return video_ids

    @classmethod
    def _get_info_video_in_playlist(cls, ids_videos: list) -> dict:
        """Информация о видео в плейлисте"""
        video_response = cls.youtube.videos().list(part='contentDetails,statistics',
                                                   id=','.join(ids_videos)).execute()
        return video_response


class Channel(Main):

    def __init__(self, id_channel: str):
        """Класс Channel для работы с каналами youtube.
        Экземпляр класса Channel инициализируется с помощью id канала"""
        super().__init__()
        self.__id_channel = id_channel
        self.__title = self.channel['items'][0]['snippet']['title']
        self.__description = self.channel['items'][0]['snippet']['description']
        self.__url = self.channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.__subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.__video_count = self.channel['items'][0]['statistics']['videoCount']
        self.__views_count = self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        """Метод возврата названия канала"""
        return f'Channel: {self.title}'

    def __add__(self, other) -> int:
        """Метод сложения количества подписчиков"""
        if not isinstance(other, Channel):
            raise ValueError('Второй объект не Channel')
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __gt__(self, other) -> bool:
        """Метод сравнения количества подписчиков >"""
        if not isinstance(other, Channel):
            raise ValueError('other - не класс Channel')
        return self.subscriber_count > other.subscriber_count

    def __lt__(self, other) -> bool:
        """Метод сравнения количества подписчиков <"""
        if not isinstance(other, Channel):
            raise ValueError('other - не класс Channel')
        return self.subscriber_count < other.subscriber_count

    @property
    def channel_id(self) -> str:
        """Возвращает id"""
        return self.__id_channel

    @property
    def title(self) -> str:
        """Возвращает название канала"""
        return self.__title

    @property
    def description(self) -> str:
        """Возвращает описание канала"""
        return self.__description

    @property
    def url(self) -> str:
        """Возвращает ссылку на канал"""
        return self.__url

    @property
    def subscriber_count(self) -> str:
        """Возвращает количество подписчиков"""
        return self.__subscriber_count

    @property
    def video_count(self) -> str:
        """Возвращает количество видео"""
        return self.__video_count

    @property
    def views_count(self) -> str:
        """Возвращает количество просмотров"""
        return self.__views_count

    @property
    def channel(self) -> dict:
        """Возвращает информацию о канале"""
        return self._get_channel(channel_id=self.__id_channel)

    def print_info(self) -> json:
        """Вывод информации о канале на экран"""
        print(super().dict_to_json(data=self.channel))      # из Main

    def to_json(self, name: str) -> json:
        """Сохраняет информацию по каналу, хранящуюся в атрибутах экземпляра класса Channel, в json-файл"""
        with open(name, 'w', encoding='utf-8') as file:
            data = {'id': self.channel_id, 'title': self.title, 'description': self.description,
                    'url': self.url, 'subscriber_count': self.subscriber_count, 'video_count': self.video_count,
                    'views_count': self.views_count}
            json.dump(data, file, indent=2, ensure_ascii=False)     # мб можно упростить


class Video(Main):
    """
    Класс Video для работы с видеороликами youtube - получения статистики.
    Пример id видео: '26_i7vQmd-8' - из адреса https://www.youtube.com/watch?v=26_i7vQmd-8&ab_channel=....
    В экземпляре инициализируются атрибуты:
        - название видео (title)
        - количество просмотров (view_count)
        - количество лайков (like_count)"""
    def __init__(self, video_id):
        super().__init__()
        self.__video_id = video_id
        self.__title = self.info_video['items'][0]['snippet']['localized']['title']
        self.__view_count = self.info_video['items'][0]['statistics']['viewCount']
        self.__like_count = self.info_video['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.__title

    @property
    def info_video(self) -> dict:
        """Возвращает словарь с данными по видео"""
        return self._get_video(self.__video_id)

    @property
    def video_id(self):
        """Возвращает id"""
        return self.__video_id

    @property
    def title(self) -> str:
        """Возвращает название видео"""
        return self.__title

    @property
    def view_count(self) -> str:
        """Возвращает количество просмотров"""
        return self.__view_count

    @property
    def like_count(self) -> str:
        """Возвращает количество лайков"""
        return self.__like_count

    def print_info(self) -> json:
        """Вывод информации на экран"""
        print(super().dict_to_json(data=self.info_video))


class PLVideo(Video, Main):

    def __init__(self, video_id, playlist_id):
        """Дополнительно инициализируется id плейлиста
        После создания экземпляра дополнительно инициализируются атрибуты:
        - id канала (channel_id)
        - название плейлиста (playlist_name)
        """
        super().__init__(video_id)
        self.__playlist_id = playlist_id
        self.__channel_id = self.info_video['items'][0]['snippet']['channelId']
        self.__playlist_name = self.playlist['items'][0]['snippet']['title']

    def __str__(self):
        return f"{super().__str__()} ({self.__playlist_name})"

    @property
    def playlist_id(self) -> str:
        """Возвращает id плейлиста"""
        return self.__playlist_id

    @property
    def channel_id(self):
        """Возвращает id канала"""
        return self.__channel_id

    @property
    def playlist_name(self) -> str:
        """Возвращает имя плейлиста"""
        return self.__playlist_name

    @property
    def playlist(self) -> dict:
        """Возвращает словарь с данными по плейлисту"""
        return self._get_playlist(self.__playlist_id)

    @property
    def playlist_channel(self) -> dict:
        """Возвращает плейлист канала"""
        return self._get_playlist_channel(self.channel_id)

    def print_info_playlist(self) -> json:
        """Вывод информации о плейлисте на экран"""
        print(super().dict_to_json(data=self.playlist))


class PlayList(Main):

    def __init__(self, playlist_id):
        super().__init__()
        self.__playlist_id = playlist_id
        self.__title = self.playlist['items'][0]['snippet']['title']
        self.__url = f'https://www.youtube.com/playlist?list={self.__playlist_id}'

    def __str__(self):
        return f"Плейлист - '{self.__title}'"

    @property
    def playlist_id(self) -> str:
        """Возвращает id плейлиста"""
        return self.__playlist_id

    @property
    def title(self) -> str:
        """Возвращает название плейлиста"""
        return self.__title

    @property
    def url(self) -> str:
        """Возвращает ссылку на плейлист"""
        return self.__url

    @property
    def playlist(self) -> dict:
        """"""
        return self._get_playlist(playlist_id=self.__playlist_id)

    @property
    def ids_videos(self) -> list:
        """Возвращает список id всех видел в плейлисте"""
        return self._get_ids_videos_in_playlist(playlist_id=self.__playlist_id)

    @property
    def total_duration(self) -> datetime.timedelta:
        """Возвращает общее время плейлиста"""
        return self.get_total_duration()

    def get_total_duration(self) -> datetime.timedelta:
        """Получает общее время плейлиста"""
        videos = self._get_info_video_in_playlist(ids_videos=self.ids_videos)
        total = datetime.timedelta()

        for video in videos['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration
        return total

    def show_best_video(self):
        """Получает ссылку на лучшее видео в плейлисте"""
        videos = self._get_info_video_in_playlist(ids_videos=self.ids_videos)
        best_likes = 0
        best_id = ''
        for video in videos['items']:
            likes = int(video['statistics']['likeCount'])
            if likes > best_likes:
                best_likes = likes
                best_id = video['id']
        return f"Ссылка на самое популярное видео в плейлисте: https://youtu.be/{best_id}"


if __name__ == '__main__':

    # 1
    # vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
    # vdud.print_info()
    # 2
    # vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
    # print(vdud.title)
    # print(vdud.video_count)
    # print(vdud.url)
    # менять не можем
    # vdud.channel_id = 'Новое название'
    # print(Channel.get_service())
    # vdud.to_json('vdud.json')
    # 3
    # ch1 = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
    # ch2 = Channel('UC1eFXmJNkjITxPFWTy6RsWg')
    # print(ch1)
    # print(ch2)
    # print(ch1 > ch2)
    # print(ch1 + ch2)
    # 4
    # video1 = Video('9lO06Zxhu88')
    # video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
    # print(video1)
    # print(video2)
    # 5
    pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
    print(pl.title)
    print(pl.url)
    duration = pl.total_duration
    print(duration)
    print(type(duration))
    print(duration.total_seconds())
    print(pl.show_best_video())
