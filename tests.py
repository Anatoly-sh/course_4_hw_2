import pytest
import datetime
from youtube_ref import Video, Channel, PLVideo, PlayList


@pytest.fixture
def item_1():
    channel_id1 = 'UCMCgOm8GZkHp8zJ6l7_hIuA'  # вДудь
    item_1 = Channel(channel_id1)
    return item_1


@pytest.fixture
def item_2():
    channel_id2 = 'UC1eFXmJNkjITxPFWTy6RsWg'  # Редакция
    item_2 = Channel(channel_id2)
    return item_2


# 3
def test_str(item_1):
    assert item_1.__str__() == "Channel: вДудь"


def test_lt(item_1, item_2):
    assert item_1.__lt__(item_2) is True


def test_gt(item_1, item_2):
    assert item_1.__gt__(item_2) is False


def test_add(item_1, item_2):
    assert item_1 + item_2 >= 14010000


# 4
def test_video():
    video1 = Video('9lO06Zxhu88')
    assert str(video1) == 'Видео: Как устроена IT-столица мира / Russian Silicon Valley (English subs)'


def test_plvideo():
    video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
    assert str(video2) == "Видео: Пушкин: наше все? (Пл.лист: Литература)"


# 5
def test_play_list():
    pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
    assert pl.title == 'Редакция. АнтиТревел'
    assert pl.url == 'https://www.youtube.com/playlist?list=PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb'
    assert pl.total_duration == datetime.timedelta(seconds=13261)
    duration = pl.total_duration
    assert duration.total_seconds() == 13261
    assert pl.show_best_video() == 'Ссылка на самое популярное видео в плейлисте: https://youtu.be/9Bv2zltQKQA'


# 6
def test_wrong_id():
    """Ожидается инициализация только video_id - несуществующий id"""
    video = Video('broken_video_id')
    assert video.video_id == "broken_video_id"
    assert video.title is None
    assert video.like_count is None
    assert video.view_count is None
