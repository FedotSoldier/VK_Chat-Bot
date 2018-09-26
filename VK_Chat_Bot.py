import vk_api # curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py # pip installation
import time   # https://pikabu.ru/story/api_vkontakte_dlya_python_3961240
# https://github.com/python273/vk_api.git # git clone
import requests
from bs4 import BeautifulSoup

#vk=vk_api.VkApi(login='login', password='12345')
vk=vk_api.VkApi(token='ea8d297a72d3e516eab6f27152e1204cb4cdca86f5518622d7d49981363fd45e98fd0f2b0215954d854a0')
vk._auth_token()

values={'out':0, 'count':100, 'offset':0}
response=vk.method('messages.getConversations', values) # Чтобы нам отвечали, даже если мы написали в первый раз

def write_msg(user_id, s):
	vk.method('messages.send', {'user_id':user_id, 'message':s})

while True:
	response=vk.method('messages.getConversations', values)
	#print(response['items'])
	#print('-------------------------------------------------------------------')
	if response['items'] and response['items'][0]['last_message']['from_id']>0:	# response['items'][0]['conversation']['unanswered'] # Нет у бота
		#if len(response['items'][0])>1:
			#write_msg(response['items'][0]['conversation']['peer']['id'], 'Канцелярия не успевает. Пишите по одному сообщению, дожидаясь ответа')
			#print(str(response)+'\n' + 'K')
		response=response['items'][0]
		#values['last_message_id']=response['conversation']['last_message_id'] # Эту строчку можно оставить, но в методе 'messages.getConversations' ее нет.
		#print(response)
		if response['last_message']['text'].lower()=='привет':
			write_msg(response['conversation']['peer']['id'], 'Не "Привет", а доброго времени суток, товарищ!')
			#print('A')
		elif response['last_message']['text'].lower()=='/usd' or response['last_message']['text'].lower()=='/eur':
			page=requests.get('https://finance.rambler.ru/currencies/USD/')
			soup=BeautifulSoup(page.text, 'html.parser')
			v=soup.findAll('a')
			if response['last_message']['text'].lower().lower()=='/usd':
				write_msg(response['conversation']['peer']['id'], 'Гражданин СССР не может пользоваться иностранной валютой'+'\n'+'За вами уже выехали'+'\n' + '$ - '+ v[26].text[4:11])
				#print('D')
			else:
				write_msg(response['conversation']['peer']['id'], 'Гражданин СССР не может пользоваться иностранной валютой'+'\n'+'За вами уже выехали'+'\n' + '€ - '+v[27].text[4:11])
				#print('E')
		else:
			write_msg(response['conversation']['peer']['id'], 'Да здравствует коммунизм!')
			#print('B')
	time.sleep(0.5)