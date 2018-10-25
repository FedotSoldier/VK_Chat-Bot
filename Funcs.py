import re
import requests
from bs4 import BeautifulSoup

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
