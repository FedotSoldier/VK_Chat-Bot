# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard

def main():
	keyboard = VkKeyboard(one_time=True)

	keyboard.add_button(label='Green', color='positive')
	keyboard.add_button(label='White', color='default')
	keyboard.add_line()
	keyboard.add_button(label='Red', color='negative')
	keyboard.add_button(label='Primary', color='primary')

	token = 'ea8d297a72d3e516eab6f27152e1204cb4cdca86f5518622d7d49981363fd45e98fd0f2b0215954d854a0' # scope=397381

	vk_session = vk_api.VkApi(login='+79151472057', 
							password='010702777',
							token=token)
	vk_session.auth(token_only=True)

	vk_community = vk_api.VkApi(token=token)
	vk = vk_community.get_api()

	longpoll = VkBotLongPoll(vk_session, '168296857')

	for event in longpoll.listen():

		if event.type == VkBotEventType.MESSAGE_NEW:
			'''
			print('Новое сообщение:')
			print('Для меня от: ', end='')
			print(event.obj.from_id)
			print('Текст:', event.obj.text)
			'''
			if event.obj.text.lower() == 'привет':
				vk.messages.send(
						user_id=event.obj.from_id,
						message='Не "Привет", а "Доброго времени суток, товарищ!"'
					)

			elif event.obj.text.lower() == 'пришли клавиатуру':
				vk.messages.send(
						user_id=event.obj.from_id,
						message='Клавиатуру в студию!',
						keyboard=keyboard.get_keyboard()
					)

			else:
				vk.messages.send(
						user_id=event.obj.from_id,
						message='Да здравствует коммунизм!'
					)

		elif event.type == VkBotEventType.MESSAGE_REPLY:
			'''
			print('Новое сообщение:')
			print('От меня для: ', end='')
			print(event.obj.peer_id)
			print('Текст:', event.obj.text)
			'''
			pass

		elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
			'''
			print('Печатает ', end='')
			print(event.obj.from_id, end=' ')
			print('для ', end='')
			print(event.obj.to_id)
			'''
			pass

		elif event.type == VkBotEventType.GROUP_JOIN:
			'''
			print(event.obj.user_id, end=' ')
			print('Вступил в группу!')
			'''
			pass

		elif event.type == VkBotEventType.GROUP_LEAVE:
			'''
			print(event.obj.user_id, end=' ')
			print('Покинул группу!')
			'''
			pass

		else:
			# print(event.type)
			pass


if __name__ == '__main__':
	main() # Мне лень было комментировать, потом мне напишешь, я объясню
