# -*- coding: utf-8 -*-
# vk_api==11.2.1
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
from Constants import *
from Funcs import *
import random
import re
# errors list
# https://gist.github.com/Zaur-Lumanov/0528f3b3ec4f5fe8f8d39449949dcc02
# мгновенный yandex поиск
# https://vk.com/topic-81349839_31476126  # 4, 5, 12, 15, 16


def main():
	# Шаблон для проверки правильного ввода запроса погоды(Например: ' Погода  10   ')
	pattern1 = r'\s*погода\s+[+-]?\d+\s*'
	# Шаблон на проверку соответствия запроса, для отправки данных о пользователе
	pattern2 = r'\s*кто\s+я\s*[?]?\s*'
	# Проверка того, что поль-ль хочет получить записи чьей-то стены
	# pattern3 = r'\s*[Сс]тена\s+(?:[-+]?\d+|[\w\s]+)\s*'
	pattern3 = r'\s*стена\s+[+-]?[\w\W]+'
	# Проверка - пользователь хочет совершить быстрый поиск
	pattern4 = r'яндекс\s+[\w\W]+'
	# Проверка того, что поль-ль хочет начать играть в города
	pattern5 = r'\s*играть\s+в\s+города\s*'
	# Проверка того, что поль-ль хочет получить случайные медиавложения
	pattern6 = r'пришли\s+(?:мемы|фильмы|фото)\s*\d*'

	# Объект игрока в города(см. Funcs.py)
	city_player = CityPlayer()
	# Показатель того, что игра в города в процессе
	city_game_is = False

	keyboard = VkKeyboard(one_time=True)  # Аргумент `one_time` отвечает за исчезновение после нажатия и отправки сообщения

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

			# Текст сообщения равен самому себе в нижнем регистре
			mtext = event.obj.text.lower()

			# Если в данный момент игра в города не в процессе:
			if not city_game_is:

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

				# Поставить лайки всем комментариям записи сообщества,
				# у которой идентификатор(id) равен 4
				elif mtext == 'likes.add':
					# Перебираем все посты сообщества
					for post in user.wall.get(owner_id=-168296857)['items']:
						if post['id'] == 4:  # Лайкаем комментарии только четвертого поста
							for comment in user.wall.getComments(owner_id=-168296857,
																	post_id=post['id'],
																	need_likes=1)['items']:
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

				# Функция из файла Funcs.py
				elif match(pattern1, mtext):
					# ch - это количество дней, для которых нужен прогноз, начиная с сегодняшнего
					ch = int(re.findall(r'.\d+', mtext)[0])
					vk.messages.send(
						user_id=event.obj.from_id,
						message=forecast(ch)
						)

				elif match(pattern2, mtext):
					user = vk.users.get(user_id=event.obj.from_id)
					vk.messages.send(
						user_id=user[0]['id'],
						message='''Ваше имя: {}
								Ваша фамилия: {}
								Ваш id: {}'''.format(user[0]['first_name'],
													user[0]['last_name'],
													user[0]['id'])
						)

				elif match(pattern3, mtext):
					# s = строка после ключевого слова "Стена"
					s = mtext[mtext.find('тена ') + 5:]
					# По умолчанию мы ищем id профиля, а не сообщества
					groupid = False
					try:
						# id пользователя - это s
						uid = int(s)
					# Если это текстовая строка:
					except ValueError:
						# Ищем пользователя вк по заданной строке(s)
						first_user = user.search.getHints(q=s, fields='id')
						try:
							uid = int(first_user['items'][0]['profile']['id'])
						# Если поиск не дал результатов
						except:
							try:
								uid = int(first_user['items'][0]['group']['id'])
								groupid = True
							except KeyError:
								uid = None
					# Если id получен
					if uid is not None:
						if not groupid:
							wall = user.wall.get(
											owner_id=uid
											)
						else:
							wall = user.wall.get(
											owner_id=-uid
											)

						vk.messages.send(
								user_id=event.obj.from_id,
								message=get_wall(wall))
					else:
						vk.messages.send(
								user_id=event.obj.from_id,
								message='[ X ] Поиск по запросу не дал результата!'
							)

				elif match(pattern4, mtext):
					stroka = mtext[mtext.find('ндекс ') + 6:]
					vk.messages.send(
						user_id=event.obj.from_id,
						message=quick_request(stroka)
						)

				elif match(pattern5, mtext):
					city_game_is = True
					vk.messages.send(
						user_id=event.obj.from_id,
						message='''Играем в города. Ваш ход. Назовите любой город.
								   Чтобы закончить игру отправьте "стоп"
								   Чтобы получить подсказку отправьте "подсказка"
								   Чтобы получить список букв, города на
								   которую закончились отправьте "/nonused" ''')

				elif match(pattern6, mtext):
					# Что нужно прислать - часть строки между 'пришли ' и цифрой-количеством
					substring = re.sub(r'(?:\s*пришли\s+|\s+\d+\s*)', '', mtext)
					# В каком количестве это нужно прислать - единственная цифра(если есть)
					count = int(re.search(r'\d+', mtext).group())
					if count > 10: count = 10

					# Если пользователь хочет мемы:
					if substring == 'мемы':
						# Список из строк, определяющих медиавложения
						attchmnt = []
						# Выбираем случайную группу из результатов поиска по запросу "мемы" и берем ее id
						group_id = user.groups.search(q='мемы', count=1000)['items'][random.randint(0,999)]['id'] * -1
						wall = user.wall.get(owner_id=group_id, count=count)
						for mem in wall['items']:
							attchmnt.append('wall{}_{}'.format(
								str(mem['owner_id']),
								str(mem['id'])
								))
						attchmnt = ','.join(attchmnt)
						print(attchmnt)

						vk.messages.send(
								message='Лови',
								user_id=event.obj.from_id,
								attachment=attchmnt)

					# Если пользователь хочет фильмы:
					elif substring == 'фильмы':
						pass

					# Если же пользователь хочет фото
					elif substring == 'фото':
						pass


				else:
					vk.messages.send(
							user_id=event.obj.from_id,
							message='Да здравствует коммунизм!'
						)
			# Если идет игра в города:
			elif city_game_is:
				mtext = mtext.lower().replace('ё', 'е').replace('-', '').replace(' ', '')
				vk.messages.send(
						user_id=event.obj.from_id,
						message=city_player.next_city(mtext)
					)
				# Если у кого-то появился статус победителя:
				if city_player.comp_won is not None:
					city_player.reboot()
					city_game_is = False

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
	main()  # Мне лень было комментировать, потом мне напишешь, я объясню
# vk-api version = 11.2.1
