import os
import sys
import time
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

from good_heartst_project.settings import COUNT_OF_POSTS, PHOTO_SIZE, TIME_SLEEP

import psycopg2
import vk_api
from vk_api.execute import VkFunction
from dotenv import load_dotenv

load_dotenv()

logger: logging.Logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler_stream = logging.StreamHandler(stream=sys.stdout)
handler_file = RotatingFileHandler(
    'servise_logger',
    maxBytes=50000,
    backupCount=2
)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler_stream.setFormatter(formatter)
handler_file.setFormatter(formatter)
logger.addHandler(handler_stream)
logger.addHandler(handler_file)

vk_get_wall_posts = VkFunction(args=('values',), code='''
    return API.wall.get(%(values)s)['items'];
''')


class SendWallPost(object):
    """Отправляет пока текстовый пост в группу сообщества."""
    OWNER_ID = -215511557
    OWNER_ID_OUT = 215511557
    FROM_GROUP = 1

    def __init__(self, message, user_phone_number, access_token,
                 photo=None, publish_date=None, close_comments=0,
                 attachments=None):
        vk_session = vk_api.VkApi(login=user_phone_number,
                                  token=access_token)
        vk_session.auth(token_only=True)
        self.vk = vk_session
        self.message = message
        self.publish_date = publish_date
        self.close_comments = close_comments
        self.attachments = attachments
        self.photo = photo

    def _send_text_post(self):
        """Отправка поста на стену сообщества если пост чисто текстовый."""
        post_id = self.vk.method('wall.post', {'message': self.message,
                                               'owner_id': self.OWNER_ID})
        return post_id

    def _send_post_with_attachments(self, photo_id, owner_id):
        """Отправка поста на стену сообщесва
         если пост содержит объекты приложенные к записи."""
        attachment_str = f'photo{owner_id}_{photo_id}'
        post_id = self.vk.method('wall.post', {'message': self.message,
                                               'owner_id': self.OWNER_ID,
                                               'attachments': attachment_str})
        return post_id

    def _get_wall_upload_server(self):
        """Метод получения url адреса для загрузки фотографии на сервер."""
        upload = vk_api.VkUpload(self.vk)
        response = upload.photo_wall(self.photo, group_id=self.OWNER_ID_OUT)
        photo_id, owner_id = response[0]['id'], response[0]['owner_id']
        return photo_id, owner_id

    def send(self):
        """SO POOR EVENT LOOP."""
        if self.photo is None:
            return self._send_text_post()
        else:
            photo_id, owner_id = self._get_wall_upload_server()
            return self._send_post_with_attachments(photo_id, owner_id)


def get_posts_from_vk():
    """Взятие постов из vk group."""

    login, password = os.getenv('VK_LOGIN'), os.getenv('VK_PASSWORD')
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error:
        message = f'Vk connection error: {error}'
        logger.critical(message)
        return error
    vk = vk_session.get_api()
    data = vk_get_wall_posts(vk,
                             {'domain': os.getenv('DOMAIN'),
                              'count': COUNT_OF_POSTS,
                              }
                             )
    return data


def parser_attachments(some_dict):
    """Функция проходит по приложению поста."""
    for item in some_dict:
        return item['photo']['sizes'][PHOTO_SIZE]['url']


def parser_json(data):
    """Функция проходит по посту и забирает необходимые данные для бд."""
    result_list = list()
    for item in data:
        post_dict = dict()
        post_dict['id'] = item['id']
        post_dict['date'] = datetime.utcfromtimestamp(  # преобразование unix время в дату
            item['date']).strftime(
            '%Y-%m-%d %H:%M:%S')
        post_dict['text_post'] = item['text']
        try:
            post_dict['photo'] = parser_attachments(item['attachments'])
        except:
            post_dict['photo'] = ''
        result_list.append(post_dict)

    return result_list


def load_to_data_base(data):
    """Загруза данных из Vk в базу данных."""
    try:
        connect = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),)
        connect.autocommit = True
    except psycopg2.Error as error:
        message = f'Postgres connecntion error {error}'
        logger.critical(message)
        return error
    cursor = connect.cursor()  # Запуск курсора
    request_sql = """INSERT INTO vk_posts_vk_posts (id, date, text_post, photo)
                  VALUES (%s, %s, %s, %s)
                  ON CONFLICT (id) DO NOTHING;"""
    try:
        for element in data:
            cursor.execute(request_sql, (element['id'],
                                         element['date'],
                                         element['text_post'],
                                         element['photo'])
                           )
    except psycopg2.Error as e:
        message = f'Postgres error {e}'
        logger.critical(message)
        return e
    finally:
        connect.close()


def parse():
    while True:
        data = get_posts_from_vk()
        data = parser_json(data)
        load_to_data_base(data)
        time.sleep(TIME_SLEEP)
