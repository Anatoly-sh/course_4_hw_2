import os
import json
from googleapiclient.discovery import build

"""
Файл .env в корне проекта  — это текстовый файл, содержащий пары “ключ/значение” 
всех переменных среды. Необходимо установить библиотеку python-dotenv. load_dotenv() 
— для поиска файла .env и загрузки из него переменных среды.
"""
from dotenv import load_dotenv

channel_id = 'UCMCgOm8GZkHp8zJ6l7_hIuA'  # вДудь
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
    Класс Video для работы с видеороликами youtube - получения статистики.
    Пример id видео: '26_i7vQmd-8' - из адреса https://www.youtube.com/watch?v=26_i7vQmd-8&ab_channel=....
    Атрибуты:
    - get_service() - метод класса для получения объекта build,
       через который осуществляется доступ к сервису youtube
    - __str__() - метод возвращает строку для печати для объекта Video"""

    def __init__(self, id_video):
        self.id_video = id_video
        # определенный ютубом метод доступа к информации о video
        self.video_data = self.get_service().videos().list(id=self.id_video, part='snippet, statistics').execute()
        self.video_info = json.dumps(self.video_data, indent=4)
        # требуемые атрибуты:
        # - название видео
        # - количество просмотров
        # - количество лайков
        self.video_name = self.video_data['items'][0]['snippet']['title']
        self.video_view_count = self.video_data['items'][0]['statistics']['viewCount']
        self.video_like_count = self.video_data['items'][0]['statistics']['likeCount']

    def __str__(self):
        """метод возвращает строку для печати для объекта Video"""
        return self.video_name

    @classmethod
    def get_service(cls):
        """метод класса, который возвращает объект для работы с API ютуба"""
        api_key: str = os.getenv('SKYPROAPIKEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


class PLVideo(Video):
    """
    Класс PLVideo для работы с видео и плейлистами youtube.
    Унаследован от Video.
    """
    def __init__(self, id_video, id_playlist):
        super().__init__(id_video)          # От класса Video
        self.id_playlist = id_playlist
        self.playlist_data = self.get_service().playlists()\
            .list(id=self.id_playlist, part='snippet, contentDetails').execute()
        self.playlist_info = json.dumps(self.playlist_data, indent=4)
        # требуемый дополнительный атрибут: название плейлиста
        self.playlist_name = self.playlist_data['items'][0]['snippet']['title']

    def __str__(self):
        """Возврат информации о плейлисте"""
        return f"Видео: '{self.video_name}' (Пл.лист: '{self.playlist_name}')"


if __name__ == '__main__':
    video1 = Video('9lO06Zxhu88')  # '9lO06Zxhu88' - это id видео из ютуб
    print(video1.video_data)
    print(video1.video_info)
    # print(video1)

    print(video1.video_name)
    print(video1.video_view_count)
    print(video1.video_like_count)
    # print(json.dumps(video1.video_data, indent=4))

    video1 = Video('9lO06Zxhu88')
    video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
    print(video1)
    print(video2)
