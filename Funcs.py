import re
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup

def match(pattern, stroka):
	# Если строка, разделенная по шаблону, пустая
	# (То есть, если строка полностью соответствует шаблону)
	if ''.join(re.split(pattern, stroka, maxsplit=1)) == '':
		return True
	else:
		return False

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
	d_numbers = [re.findall(r'\d+', day)[0] for day in days]  # Номера всех дней, чтобы потом находить разницу(difference) между индексами дней в days,  
															  # а не самими числами(бывает, что сегодня 1-е, а вчера было 31-е)
	temps_night = [tag.getText() for tag in temps_night]
	temps_day   = [tag.getText() for tag in temps_day  ]
	curr_day    = re.findall(r'\d+', curr_day[0].getText())[0]  # Если это первый день месяца, то там кроме цифры еще и месяц написан
	first_day   = re.findall(r'\d+', first_day.getText())[0]
	difference  = d_numbers.index(curr_day) - d_numbers.index(first_day)  # Разница между текущим днём и первым в прогнозе

	days[difference] += ' (сегодня)'
	if difference + 2 <= len(days): days[difference + 1] += ' (завтра)'
	if difference + 3 <= len(days): days[difference + 2] += ' (послезавтра)'
	if difference >= 1 : days[difference - 1] += ' (вчера)'
	if difference >= 2 : days[difference - 2] += ' (позавчера)'

	if ch < 0:  # Если пользователю нужны прогнозы за старые дни:
		# Тогда ch становится положительным,
		# а все списки с данными - это списки в срезе от разницы между текущим днём и первым
		# до первого дня включительно(в обратной последовательности)
		ch = abs(ch)
		days = days[difference::-1]
		temps_day = temps_day[difference::-1]
		temps_night = temps_night[difference::-1]
	else:
		days = days[difference:]
		temps_day = temps_day[difference:]
		temps_night = temps_night[difference:]

	forecast = ''

	for day in range(ch + 1):
		try:
			forecast += days[day] + '\n'
			forecast += 'Днём  ' + temps_day   [day] + '°\n'
			forecast += 'Ночью ' + temps_night [day] + '°\n'
			forecast += '===' + '\n'
		except IndexError:
			break

	return forecast

def get_wall(wall):
	result = 'Всего найдено записей: {}\n'.format(str(wall['count']))
	wall = wall['items']
	# Укорачиваем список до 30 записей
	try:
		wall = wall[0:30]
	except IndexError:
		wall = wall[0:]

	for post in wall:
		try:
			try:
				imgs = post['copy_history'][0]['attachments'][0]['photo']['sizes']
				result += imgs[len(imgs) - 1]['url'] + '\n'
			# Вкладыши к посту(attachments) могут быть раньше
			except:
				imgs = post['attachments'][0]['photo']['sizes']
				result += imgs[len(imgs) - 1]['url'] + '\n'
		# Может либо не быть ячейки с фото, либо она может быть пустой
		except Exception as ErrMsg:
			# print(ErrMsg)
			# print(post)
			pass

	return result

def quick_request(stroka):
	url = 'https://yandex.ru/search/?text={}&lr=213'
	# Заменяем все кроме букв и цифр на обозначение пробела в яндекс-ссылке("%20")
	stroka = re.sub(r'\W+', '%20', stroka)
	url = url.format(stroka)  # Мы получили url запроса.
	''' Теперь парсим страницу с результатами поиска
		и если там есть окно с быстрым ответом: 
		получаем информацию из него '''
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	r = soup.select_one('.fact__description ')
	h = soup.select_one('.fact-answer')

	result = ''
	# Окна с быстрым ответом может не быть
	try:
		result += r.find_all('b')[0].text + '\n'
		result += r.text + '\n'
		result += h.find_all('a')[0].get('href')
	# Если soup.select_one('.class') - 'NoneType' object
	except AttributeError:
		result += 'Быстрый ответ не найден\n'
		result += 'Попробуйте поискать напрямую\n'
		result += url

	return result

class CityPlayer:
	def __init__(self):
		self.table = pd.read_csv('cities.csv',
								  encoding="windows-1251",
								  sep=',')
		self.cities = self.table['city']
		# Слово, которое компьютер отослал
		# игроку в последний раз
		self.last_word = None
		# Города, которые уже были использованы в игре
		# Если не будет какого-нибудь элемента, то при операции
		# "self.used_cities[self.used_cities == 'any_string']"
		# выскочит ошибка - TypeError: invalid type comparison
		self.used_cities = pd.Series(['Something'])
		# Показатель выигрыша компьютера
		self.comp_won = None
		# Список с буквами, на которые больше не осталось городов
		self.lost_letters = []
		# Список с буквами, на которые больше не осталось городов,
		# о которых еще не оповещен пользователь
		self.letters_to_notify = []

	def next_city(self, cur):
		# Ответ компьютера игроку
		answer = None
		# Проверяем, не хочет ли игрок остановиться:
		if cur == 'стоп':
			self.comp_won = True
			answer = 'Игра окончена. Спасибо за игру!'
		# Может игрок хочет получить подсказку:
		elif cur == 'подсказка':
			if self.last_word == None:
				self.cities.index = range(0, len(self.cities))
				city = self.cities[random.randint(0, len(self.cities) - 1)]
				answer = '''Ваш ход первый. Вы можете назвать
						  любой город, например: "{}" '''.format(city)
			else:
				cities = self.table[self.cities.str.startswith(self.last_word[-1])]['city']
				cities.index = range(0, len(cities))
				answer = cities[random.randint(0, len(cities) - 1)]
				answer = self.table[self.cities == answer]['city_to_output']
		# Пользователь хочет получить список букв, на которые нет городов:
		elif cur == '/nonused':
			if len(self.lost_letters) == 0:
				answer = 'Буквы, на которые нет городов, пока не найдены'
			else:
				answer = ''' Список букв, на которые
							 больше нет городов:\n{}'''.format('\n'.join(self.lost_letters))
		# Проверяем, не первый ли это ход(игрока)
		elif self.last_word is not None:
			# Если игрок назвал слово на последнюю
			# букву предыдущего города:
			if cur[0] == self.last_word[-1]:
				answer = self.get_city(cur)

			# Если игрок назвал город не на последнюю букву предыдущего города:
			elif cur[0] != self.last_word[-1]:
				answer = 'Вы должны назвать новый город на букву "{}"'.format(self.last_word[-1])

		# Если это первый ход(первым ходит игрок):
		elif self.last_word is None:
			answer = self.get_city(cur)

		return answer

	def get_city(self, cur):
		# Показатель того, что кроме города-ответа
		# в ответе присутствуют еще какие-либо объяснения и тп
		is_addition = False
		# Ответ пока пустой
		answer = ''
		# Если город есть в базе данных:
		if len(self.cities[self.cities == cur]) > 0:
			# Удаляем слово из базы данных
			self.remove_city(cur)
			# Сохраняем слово до обрезания
			cur_before = cur
			# Обрезаем слово, пока на его последнюю букву
			# не будут иметься города в таблице
			cur = self.prepare_city(cur)
			# Если остались слова на нужную букву:
			if cur != '':
				# Если слово было обрезано:
				if cur != cur_before:
					# Добавляем в ответ объяснение того, почему отправляем
					# слово не на последнюю букву слова пользователя
					answer += ''' Первая с конца буква вашего города, 
								  на которую остались города - {} '''.format(cur[-1])
					is_addition = True
				# Выбираем из бд все слова, которые начинаются
				# на последнюю букву слова, отправленного игроком
				the_right_words = self.table[self.cities.str.startswith(cur[-1])]['city']
				# Определяем новые индексы от нуля до конца, а то останутся
				# те же, которые были у этих городов в общей таблицы
				the_right_words.index = range(0, len(the_right_words))
				# Случайное слово, которое будем отправлять игроку
				cur_word = the_right_words[random.randint(0, len(the_right_words) - 1)]
				# Записываем этот случайный город(cur_word) в ответ
				# Пока что это город с маленьким регистром, с е замененными на ё и тд.
				city = cur_word
				# Выбираем соседнюю ячейку таблицы для этого города -
				# то же название, записанное более приятно для глаз(по правилам)
				city = self.table[self.cities == city]['city_to_output']
				# Настраиваем индексы для списка этих городов(city)
				city.index = range(len(city))
				# В конце добавим первый элемент из city
				# (а там всего один элемент) в ответ
				# answer += '\n' + city[0]
				# Сохраняем наш ответ до обрезания :)
				cur_before = cur_word
				# Удаляем город из базы
				self.remove_city(cur_word)
				# Доводим до нужной кондиции cur_word - может
				# не быть городов на его последнюю букву
				cur_word = self.prepare_city(cur_word)
				# Если появились новые буквы, на которые больше нет городов:
				if len(self.letters_to_notify) > 0:
					# Оповещаем об этом пользователя
					answer += '''\nБольше нет городов на букву(ы): {}'''.format(', '.join(self.letters_to_notify))
					self.letters_to_notify = []
					is_addition = True
				if cur_word != cur_before:
					if cur_word != '':
						answer += '''\nПервая с конца буква моего города("{}"), на которую остались города -
									   это "{}". Назовите город на неё. '''.format(city[0], cur_word[-1])
					# Если нет городов ни на одну из букв нашего города:
					elif cur_word == '':
						answer += '''\nК сожалению не осталось городов, ни на одну из букв
									   города "{}". К сожалению вы проиграли'''.format(city[0])
						self.comp_won = True
					is_addition = True
				# Добавляем в ответ город, выбранный компьютером(делаем это только сейчас,
				# чтобы ответ был в конце - так удобнее - не надо искать его где-то в середине)
				answer += '\n'
				# Если были какие-либо объяснения в ответе(информация кроме города-ответа):
				if is_addition:
					# То помимо перед городом-ответом вставляем информацию,
					# что именно это мой ответ - чтобы было сразу видно,
					# где объяснение, а где ответ
					answer += 'Мой город: '
				answer += city[0]
				# Последнее названное(компьютером) слово - это текущее слово
				self.last_word = cur_word

			else:
				answer = ''' Поздравляем. Больше не осталось городов, ни на одну
							 из букв вашего города. Вы выиграли!!! '''.format(cur[-1])
				self.comp_won = False

		# Если город есть в базе данных использованных городов:
		elif int(len(self.used_cities[self.used_cities == cur])) > 0:
			answer = '''Такой город уже был. Попробуйте еще.
						Назовите город на букву "{}" '''.format(self.last_word[-1])

		# Если же города, названного игроком, нет ни в одной в базе:
		else:
			answer = '''Такого города нет в базе. Попробуйте какой-нибудь другой.
						Назовите город на букву "{}" '''.format(self.last_word[-1])
		return answer

	def remove_city(self, word):
		self.table = self.table.loc[self.cities != word]
		self.cities = self.table['city']
		# Добавляем город в серию(pandas.Series) использованных городов
		self.used_cities.at[len(self.used_cities)] = word

	# Обрезаем название норода до тех пор, пока в таблице с
	# городами не будет городов на его последнюю букву
	def prepare_city(self, word):
		while len(self.table[self.cities.str.startswith(word[-1])]['city']) == 0:
			if word[-1] not in self.lost_letters:
				self.lost_letters.append(word[-1])
				self.letters_to_notify.append(word[-1])
			word = word[:-1]
			if word == '':
				return word
		return word

	def reboot(self):
		self.table = pd.read_csv('cities.csv',
								  encoding="windows-1251")
		self.cities = self.table['city']
		# Слово, которое компьютер отослал
		# игроку в последний раз
		self.last_word = None
		# Города, которые уже были использованы в игре
		self.used_cities = pd.Series(['Something'])
		# Показатель выигрыша компьютера
		self.comp_won = None

# При отсутствии городов на последнюю букву, компьютер переходит на предыдущую
# В сложном режиме компьютер выбирает слова, на конечеую букву которых осталось меньше городов в бд.
# Функция подсказать
