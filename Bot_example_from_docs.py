# -*- coding: utf-8 -*-

import requests

import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType


def main():
    session = requests.Session()

    # Авторизация пользователя:
    """
    login, password = 'python@vk.com', 'mypassword'
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    """

    # Авторизация группы (для групп рекомендуется использовать VkBotLongPoll):
    # при передаче token вызывать vk_session.auth не нужно
    
    vk_session = vk_api.VkApi(token='ea8d297a72d3e516eab6f27152e1204cb4cdca86f5518622d7d49981363fd45e98fd0f2b0215954d854a0')
    

    vk = vk_session.get_api()

    upload = VkUpload(vk_session)  # Для загрузки изображений
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            print('id{}: "{}"'.format(event.user_id, event.text), end=' ')

            response = session.get(
                'http://api.duckduckgo.com/',
                params={
                    'q': event.text,
                    'format': 'json'
                }
            ).json()

            text = response.get('AbstractText')
            image_url = response.get('Image')

            if not text:
                vk.messages.send(
                    user_id=event.user_id,
                    message='No results'
                )
                print('no results')
                continue

            attachments = []

            if image_url:
                image = session.get(image_url, stream=True)
                photo = upload.photo_messages(photos=image.raw)[0]

                attachments.append(
                    'photo{}_{}'.format(photo['owner_id'], photo['id'])
                )

            vk.messages.send(
                user_id=event.user_id,
                attachment=','.join(attachments),
                message=text
            )
            print('ok')


if __name__ == '__main__':
    main()
