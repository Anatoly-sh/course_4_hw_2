import os
import json
from googleapiclient.discovery import build
import pprint
import isodate

"""
Файл .env в корне проекта  — это текстовый файл, содержащий пары “ключ/значение” 
всех переменных среды. Необходимо установить библиотеку python-dotenv. load_dotenv() 
— для поиска файла .env и загрузки из него переменных среды.
"""
from dotenv import load_dotenv

channel_id = 'UCMCgOm8GZkHp8zJ6l7_hIuA'  # вДудь
# id_video
load_dotenv()


class Channel:
    """Класс Channel для работы с каналами youtube.
        Экземпляр класса Channel инициализируется с помощью id канала"""
    def __init__(self, channel_id):
        self.__id_channel = channel_id
        # определенный ютубом метод доступа к информации о канале
        self.channel_info = self.get_service().channels().list(id=channel_id, part='snippet, statistics').execute()
        # все остальное из channel_info (кроме url):
        self.title = self.channel_info['items'][0]['snippet']['title']
        self.description = self.channel_info['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.__id_channel
        self.subscriber_count = self.channel_info['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel_info['items'][0]['statistics']['videoCount']
        self.view_count = self.channel_info['items'][0]['statistics']['viewCount']

    def __str__(self):
        """Метод возврата названия канала"""
        return f'Channel: {self.title}'

    @property
    def channel_id(self):
        return self.__id_channel

    @classmethod
    def get_service(cls):
        """метод класса, который возвращает объект для работы с API ютуба"""
        api_key: str = os.getenv('SKYPROAPIKEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def save_to_file(self, file_name):
        """запись статистики в файл"""
        with open(file_name, 'w', encoding='UTF-8') as file:
            json.dump(self.channel_info, file, indent=4, ensure_ascii=False)

    def print_info(self):
        """Статистика канала
        см. методы build() , channels() , list() , execute()"""
        pr_info = json.dumps(self.channel_info, indent=4)
        return pr_info

    def __add__(self, other):
        """Метод сложения количества подписчиков"""
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __gt__(self, other):
        """Метод сравнения количества подписчиков >"""
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __lt__(self, other):
        """Метод сравнения количества подписчиков <"""
        return int(self.subscriber_count) < int(other.subscriber_count)


class Video:
    """
    Класс Video для работы с видео youtube.
    Атрибуты:
    - api_key - API ключ для доступа к сервису youtube.
    - get_service() - метод класса для получения объекта build,
       через который осуществляется доступ к сервису youtube
    - set_api_key() -метод класса для получения значения API ключа из config.py
    - __init__()- инициализация экземляра класса
    - get_video_statistic() - метод получения статистики видео по его id
    - __repr__() - метод возвращает представление объекта Video
    - __str__() - метод возвращает строку для печати для объекта Video"""

    def __init__(self, id_video):
        self.id_video = id_video
        # определенный ютубом метод доступа к информации о video
        self.video_data = self.get_service().videos().list(id=self.id_video, part='snippet, statistics').execute()
        self.video_info = json.dumps(self.video_data, indent=4)
        self.video_name = self.video_data['items'][0]['snippet']['title']
        self.video_view_count = self.video_data['items'][0]['statistics']['viewCount']
        self.video_like_count = self.video_data['items'][0]['statistics']['likeCount']

    @classmethod
    def get_service(cls):
        """метод класса, который возвращает объект для работы с API ютуба"""
        api_key: str = os.getenv('SKYPROAPIKEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


if __name__ == '__main__':
    video1 = Video('9lO06Zxhu88')  # '9lO06Zxhu88' - это id видео из ютуб
    print(video1.video_info)
    print(video1.video_name)
    print(video1.video_view_count)
    print(video1.video_like_count)
    # print(json.dumps(video1.video_data, indent=4))

    """vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
    playlists = vdud.print_info().playlists().list(channelId=channel_id,
                                                   part='contentDetails,snippet',
                                                   maxResults=50,
                                                   ).execute()"""
# Задание 1
#     vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
#     print(vdud.print_info())
#
#     print(Channel.get_service())        # <googleapiclient.discovery.Resource object at 0x106575fd0>

# Задание 2
#     vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')

# получаем значения атрибутов
#     print(vdud.title)
# вДудь
#     print(vdud.video_count)
# 163
#     print(vdud.url)
# https://www.youtube.com/channel/UCMCgOm8GZkHp8zJ6l7_hIuA

# менять не можем
#     vdud.channel_id= 'Новое название'
# AttributeError: property 'channel_id' of 'Channel' object has no setter

# можем получить объект для работы с API вне класса
#     print(Channel.get_service())
# <googleapiclient.discovery.Resource object at 0x000002B1E54F9750>

# создать файл 'vdud.json' в данными по каналу
# vdud.to_json('vdud.json')

# Задание 3
# ch1 = Channel('UC1eFXmJNkjITxPFWTy6RsWg')   # Редакция
# ch2 = Channel(channel_id)
# print(ch1)
# print(ch2)
# print(ch1 + ch2)
# print(ch1 > ch2)
# print(ch1 < ch2)


'''class Video:
    """
    Класс Video для работы с видео youtube.
    Атрибуты:
    - api_key - API ключ для доступа к сервису youtube.
    - get_service() - метод класса для получения объекта build,
     через который осуществляется доступ к сервису youtube
     - set_api_key() -метод класса для получения значения API ключа из config.py
     - __init__()- инициализация экземляра класса
     - get_video_statistic() - метод получения статистики видео по его id
     - __repr__() - метод возвращает представление объекта Video
     - __str__() - метод возвращает строку для печати для объекта Video
    """
    api_key: str = os.getenv('SKYPROAPIKEY')

    @classmethod
    def get_service(cls):
        """метод класса возвращает объект для работы с youtube"""
        with build('youtube', 'v3', developerKey=cls.api_key) as youtube:
            return youtube

    @classmethod
    def set_api_key(cls):
        """метод класса возвращает ключ для работы с youtube"""
        cls.api_key = key_for_youtube
        return cls.api_key

    def __init__(self, video_id):
        """инициализация класса.
        youtube - объект для работы с youtube"""
        self.set_api_key()
        self.video_id = video_id
        self.youtube = self.get_service()
        self.get_video_statistic()

    def get_video_statistic(self):
        """
        Метод получения статистики видео по его id.
        Атрибуты:
        - video_id - id видео из ютуб
        - video_name -название видео
        - video_count - количество просмотров
        - video_likes - количество лайков
        """
        video_response = self.youtube.videos().list(part='snippet,statistics', \
                                                    id=self.video_id).execute()
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.video_likes: int = video_response['items'][0]['statistics']['likeCount']
        self.comment_count: int = video_response['items'][0]['statistics']['commentCount']

    def __repr__(self):
        """метод возвращает представление объекта Video"""
        text = ""
        for dic in self.__dict__:
            text += dic + "=" + str(self.__dict__[dic]) + ", "
        return text[:-2]

    def __str__(self):
        """метод возвращает строку для печати для объекта Video"""
        return self.video_title


class PLVideo(Video):
    """
    Класс PLVideo для работы с видео и плейлистами youtube.
    Унаследован от Video.
    Атрибуты:
    - __init__() - - инициализация экземляра класса
    - get_playlist_statistic() - метод получения статистики для видео из плейлиста
    - __repr__() - метод возвращает представление объекта Video
    - __str__() - метод возвращает строку для печати для объекта Video
    """

    def __init__(self, video_id, playlist_id):
        "инициализация объекта класса PLVideo"
        Video.__init__(self, video_id)
        self.playlist_id = playlist_id
        self.get_playlist_statistic()

    def get_playlist_statistic(self):
        """
        метод получения статистики для видео из плейлиста.
         Атрибуты:
        - playlist_name - название плейлиста
        """
        playlist = self.youtube.playlists().list(id=self.playlist_id, part='snippet').execute()
        self.playlist_name = playlist['items'][0]['snippet']['title']

        # playlist_videos = self.youtube.playlistItems().list(playlistId=\
        #     self.playlist_id, part='contentDetails', maxResults=50,).execute()

        # получить все id видеороликов из плейлиста
        # video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items'] if video['contentDetails']['videoId'] == self.video_id]

    def __repr__(self):
        """метод возвращает представление объекта PLVideo"""
        text = ""
        for dic in self.__dict__:
            text += dic + "=" + str(self.__dict__[dic]) + ", "
        return text[:-2]

    def __str__(self):
        """метод возвращает строку для печати для объекта PLVideo"""
        return f"{self.video_title} ({self.playlist_name})"
'''

#  это  в конце
# video_id = '9lO06Zxhu88'
# video_response = youtube.videos().list(part='snippet,statistics', id=video_id).execute()
# printj(video_response)
