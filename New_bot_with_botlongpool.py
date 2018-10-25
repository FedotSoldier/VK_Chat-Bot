# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
from Constants import login, password, group_id1, token1, group_id2, token2 # scope=397381
from Funcs import getrates, getweather, forecast
import re
# https://gist.github.com/Zaur-Lumanov/0528f3b3ec4f5fe8f8d39449949dcc02 # errors list
# https://vk.com/topic-81349839_31476126  # 4, 5, 12, 15, 16 # мгновенный yandex поиск
def main():
	pattern = r'\s*[пП]огода\s+[+-]?\d+\s*'  # Шаблон для проверки правильного ввода запроса погоды(Например: ' Погода  10   ')

	keyboard = VkKeyboard(one_time=True)

	keyboard.add_button(label='Green', color='positive')
	keyboard.add_button(label='White', color='default')
	keyboard.add_line()
	keyboard.add_button(label='Red', color='negative')
	keyboard.add_button(label='Primary', color='primary')

	vk_session = vk_api.VkApi(login=login, 
							password=password,
							token=token1)
	vk_session.auth(token_only=True)
	user = vk_session.get_api()

	vk_community = vk_api.VkApi(token=token1)
	vk = vk_community.get_api()

	longpoll = VkBotLongPoll(vk_session, group_id1)

	for event in longpoll.listen():

		if event.type == VkBotEventType.MESSAGE_NEW:
			'''
			print('Новое сообщение:')
			print('Для меня от: ', end='')
			print(event.obj.from_id)
			print('Текст:', event.obj.text)
			'''

			mtext = event.obj.text.lower() # Текст сообщения в нижнем регистре(message text)

			if mtext == 'привет':
				vk.messages.send(
						user_id=event.obj.from_id,
						message='Не "Привет", а "Доброго времени суток, товарищ!"'
					)

			elif mtext == 'пришли клавиатуру':
				vk.messages.send(
						user_id=event.obj.from_id,
						message='Клавиатуру в студию!',
						keyboard=keyboard.get_keyboard()
					)

			elif mtext == 'wall.post':
				user.wall.post(
					owner_id=-group_id1,
					from_group=1,
					message='Наш бот научился публиковать посты с медиавложениями! (Это его запись)',
					attachments='photo223990687_456240130,'
					)

			elif mtext == 'wall.createcomment':
				user.wall.createComment(
					owner_id=-group_id1,
					post_id=4,
					from_group=group_id1,
					message='Он ещё и комментировать умеет'
					)

			elif mtext == 'likes.add':  # Поставить лайки всем комментариям записи с идентификатором (id) 4
				for post in user.wall.get(owner_id=-168296857)['items']:  # Все посты сообщества
					if post['id'] == 4:  # Лайкаем комментарии только четвертого поста
						for comment in user.wall.getComments(owner_id=-168296857, post_id=post['id'], need_likes=1)['items']:
							if comment['likes']['count'] == 0:
								user.likes.add(
									type='comment',  # https://vk.com/dev/likes.add
									owner_id=-168296857,
									item_id=comment['id']
									)

			elif mtext == '/getrates':
				vk.messages.send(
					user_id=event.obj.from_id,
					message=getrates()
					)

			elif mtext == '/getweather':
				vk.messages.send(
					user_id=event.obj.from_id,
					message=getweather()
					)

			elif re.match(pattern, mtext) != None:
				ch = int(re.findall(r'.\d+', mtext)[0])  # Количество дней, для которых нужен прогноз, начиная с сегодняшнего
				vk.messages.send(
					user_id=event.obj.from_id,
					message=forecast(ch)
					)
			
			elif re.match(r'\s*кто\s+я\s*[?]?\s*', mtext):  # 437991748
				user = vk.users.get(user_id=event.obj.from_id)
				# print(vk.users.get(user_ids='470863866, 493610009', fields='online, has_mobile, is_friend'))
				vk.messages.send(
					user_id=user[0]['id'],
					message='''Ваше имя: {}
							Ваша фамилия: {}
							Ваш id: {}'''.format(user[0]['first_name'], user[0]['last_name'], user[0]['id'])
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
			messages.send(
				user_id=event.obj.user_id,
				message='Поздравляем со вступлением в нашу группу!'
				)

		elif event.type == VkBotEventType.GROUP_LEAVE:
			'''
			print(event.obj.user_id, end=' ')
			print('Покинул группу!')
			'''
			messages.send(
				user_id=event.obj.user_id,
				message='Как вы могли бросить нас! Возвращайтесь быстрее'
				)

		else:
			# print(event.type)
			pass


if __name__ == '__main__':
	main() # Мне лень было комментировать, потом мне напишешь, я объясню
# vk-api version = 11.2.1
