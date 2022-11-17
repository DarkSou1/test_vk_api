import os
import time

import django
from good_heartst_project.settings import COUNT_OF_POSTS, PHOTO_SIZE, TIME_SLEEP
from .models import Vk_posts

import psycopg2

import vk_api
from vk_api.execute import VkFunction
from dotenv import load_dotenv

load_dotenv()

vk_get_wall_posts = VkFunction(args=('values',), code='''
    return API.wall.get(%(values)s)['items'];
''')


def get_posts_from_vk():
    """Взятие постов из vk group."""
    login, password = os.getenv('VK_LOGIN'), os.getenv('VK_PASSWORD')
    """Необходимо вбивать строки с логином и паролем через .env не работает я разберусь."""
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error:
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
        post_dict['date'] = item['date']
        post_dict['text_post'] = item['text']
        try:
            post_dict['photo'] = parser_attachments(item['attachments'])
        except:
            post_dict['photo'] = ''
        result_list.append(post_dict)

    return result_list


def load_to_data_base(data):
    # for element in data:
    #     Vk_posts.objects.create(id=element['id'],
    #                             date=element['date'],
    #                             text_post=element['text_post'],
    #                             photo=element['photo'])
    # return None
    try:
        connect = psycopg2.connect(
            dbname=os.getenv('NAME'),
            user=os.getenv('USER'),
            password='postgres',
            host='localhost',
            port=os.getenv('PORT'), )
        connect.autocommit = True
        cursor = connect.cursor()
    except psycopg2.Error as e:
        return e
    with cursor:
        try:
            connect.cursor.execute("""CREATE TABLE test_vk
            (id INT PRIMARY KEY,
            date CHAR(10) NOT NULL,
            test_post TEXT NOT NULL,
            photo TEXT);""")
        except psycopg2.ProgrammingError:
            print('Allready exists')
    with cursor:
        request_sql = """INSERT INTO test_vk (id, date, test_post, photo)
                      VALUES (%s, %s, %s, %s)
                      ON CONFLICT (id) DO NOTHING;"""
        for element in data:
            try:
                cursor.execute(request_sql, (element['id'],
                                             element['date'],
                                             element['text_post'],
                                             element['photo'])
                               )
            except psycopg2.Error as e:
                return e
            finally:
                connect.close()


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'good_heartst_project.settings')
    django.setup()
    while True:
        data = get_posts_from_vk()
        data = parser_json(data)
        load_to_data_base(data)
        time.sleep(TIME_SLEEP)
