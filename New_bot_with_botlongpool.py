# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
from Constants import login, password, group_id1, token1, group_id2, token2 # scope=397381
import requests
from bs4 import BeautifulSoup
import re
# https://gist.github.com/Zaur-Lumanov/0528f3b3ec4f5fe8f8d39449949dcc02 # errors list
def main():

	def getrates():
		page = requests.get('https://www.sberometer.ru/cbr/')
		soup = BeautifulSoup(page.text, 'html.parser')
		tags = soup.select('td > a')[0:3]  # Первые три тэга a, которые сразу после тэга td
		courses = [tag.getText() for tag in tags]
		currency_list = ['USD : ', 'EUR : ', 'GBP : ']
		for i in range(len(currency_list)):
			currency_list[i] += courses[i]
		return ' | '.join(currency_list)

	def getweather():
		page = requests.get('https://yandex.ru/search/?text=погода%20в%20москве%20на%203%20дня&lr=213&clid=2270455&win=334')
		soup = BeautifulSoup(page.text, 'html.parser')
		day_temp   = soup.select('.weather-forecast__tile-day')  # Список из тэгов с температурой на четыре дня
		night_temp = soup.select('.weather-forecast__tile-night')
		day_temp   = [temp.getText() for temp in day_temp]
		night_temp = [temp.getText() for temp in night_temp]
		answer = ''' Погода
					сегодня днём {}°,
					сегодня ночью {}°,
					завтра днём {}°,
					завтра ночью {}°,
					послезавтра днём {}°,
					послезавтра ночью {}°,
					через три дня днём {}°,
					через три дня ночью {}°
					'''.format(
							   day_temp[0],
							   night_temp[0],
							   day_temp[1],
							   night_temp[1],
							   day_temp[2],
							   night_temp[2],
							   day_temp[3],
							   night_temp[3],
							   )
		return answer

	def forecast(ch):
		page = requests.get('https://yandex.ru/pogoda/moscow/month')
		soup = BeautifulSoup(page.text, 'html.parser')
		
		days = soup.select('.climate-calendar-day__detailed-day')  # Все даты с прогнозами
		temps_night = soup.select('.climate-calendar-day__detailed-basic-temp-night .temp__value')  # Все ночные температуры
		temps_day   = soup.select('.climate-calendar-day__detailed-basic-temp-day .temp__value')    # Все дневные температуры
		first_day   = soup.select_one('.climate-calendar-day__day')  # Номер первого дня в прогнозе
		curr_day    = soup.select('.climate-calendar-day_current_day .climate-calendar-day__row .climate-calendar-day__day')  # Номер текущего дня месяца

		days = [tag.getText() for tag in days]
		temps_night = [tag.getText() for tag in temps_night]
		temps_day   = [tag.getText() for tag in temps_day  ]
		curr_day    =  curr_day[0].getText()
		first_day   = first_day.getText()
		difference  = int(curr_day) - int(first_day)  # Разница между текущим днём и первым в прогнозе

		if ch < 1: ch = 1  # Проверка на дурака-пользователя
		forecast = ''

		for day in range(ch):
			try:
				forecast += days[day + difference] + '\n'
				forecast += 'Днём  ' + temps_day   [day + difference] + '\n'
				forecast += 'Ночью ' + temps_night [day + difference] + '\n'
				forecast += '===' + '\n'
			except IndexError:
				break

		return forecast

	pattern = r'\s*[пП]огода\s*\d*\s*'  # Шаблон для проверки правильного ввода запроса погоды(Например: ' Погода  10   ')

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

			elif event.obj.text.lower() == 'wall.post':
				user.wall.post(
					owner_id=-group_id1,
					from_group=1,
					message='Наш бот научился публиковать посты с медиавложениями! (Это его запись)',
					attachments='photo223990687_456240130,'
					)

			elif event.obj.text.lower() == 'wall.createcomment':
				user.wall.createComment(
					owner_id=-group_id1,
					post_id=4,
					from_group=group_id1,
					message='Он ещё и комментировать умеет'
					)

			elif event.obj.text.lower() == 'likes.add':  # Поставить лайки всем комментариям записи с идентификатором (id) 4
				for post in user.wall.get(owner_id=-168296857)['items']:  # Все посты сообщества
					if post['id'] == 4:  # Лайкаем комментарии только четвертого поста
						for comment in user.wall.getComments(owner_id=-168296857, post_id=post['id'], need_likes=1)['items']:
							if comment['likes']['count'] == 0:
								user.likes.add(
									type='comment',  # https://vk.com/dev/likes.add
									owner_id=-168296857,
									item_id=comment['id']
									)

			elif event.obj.text.lower() == '/getrates':
				vk.messages.send(
					user_id=event.obj.from_id,
					message=getrates()
					)

			elif event.obj.text.lower() == '/getweather':
				vk.messages.send(
					user_id=event.obj.from_id,
					message=getweather()
					)

			elif re.match(pattern, event.obj.text.lower()) != None:
				ch = int(re.findall(r'\d+', event.obj.text.lower())[0])  # Количество дней, для которых нужен прогноз, начиная с сегодняшнего
				vk.messages.send(
					user_id=event.obj.from_id,
					message=forecast(ch)
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
