# -*- coding: utf-8 -*-

import vk_api
import json
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard

def main():

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

	longpoll = VkLongPoll(vk_session)

	keyboard = VkKeyboard(one_time=True)
	keyboard.add_button(label='White', color='default')

	for event in longpoll.listen():
		if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
			print('id{}: "{}"'.format(event.user_id, event.text), end=' ')

			if event.text.lower() == 'привет':
				vk.messages.send(
					user_id=event.user_id,
					message='Не "Привет", а "Доброго времени суток, товарищ!"'
				)
				print('message sent')

			elif event.text.lower() == 'gr':
				vk.messages.send(
					user_id=event.user_id,
					message='Клавиатуру в студию!',
					keyboard=keyboard.get_keyboard()  # После отправки клавы происходит ошибка
				)
				print('message sent')
				
			else:
				vk.messages.send(
					user_id=event.user_id,
					message='Да здравствует коммунизм!'
				)
				print('message sent')

			print('ok')


if __name__ == '__main__':
	main()
